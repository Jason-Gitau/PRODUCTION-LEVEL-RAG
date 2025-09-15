import re
from typing import List
from llama_index.core import Document

class DataPreprocessor:
    def __init__(self):
        self.cleaning_patterns = [
            (r'\s+', ' '),  # Multiple whitespace to single space
            (r'\n+', '\n'),  # Multiple newlines to single newline
            (r'[^\x00-\x7F]+', ''),  # Remove non-ASCII characters
        ]
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Apply cleaning patterns
        for pattern, replacement in self.cleaning_patterns:
            text = re.sub(pattern, replacement, text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def remove_noise(self, text: str) -> str:
        """Remove common noise patterns"""
        # Remove excessive punctuation
        text = re.sub(r'[!]{3,}', '!', text)
        text = re.sub(r'[?]{3,}', '?', text)
        text = re.sub(r'[,]{2,}', ',', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        return text
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for consistency"""
        # Convert to lowercase
        text = text.lower()
        
        # Normalize quotes
        text = re.sub(r'[""`´]', '"', text)
        text = re.sub(r"[']+", "'", text)
        
        # Normalize hyphens
        text = re.sub(r'[-‐‑‒–—―]', '-', text)
        
        return text
    
    def preprocess_documents(self, documents: List[Document]) -> List[Document]:
        """Preprocess a list of documents"""
        processed_docs = []
        
        for doc in documents:
            # Clean text
            cleaned_text = self.clean_text(doc.text)
            
            # Remove noise
            denoised_text = self.remove_noise(cleaned_text)
            
            # Normalize
            normalized_text = self.normalize_text(denoised_text)
            
            # Create new document with processed text
            processed_doc = Document(
                text=normalized_text,
                metadata=doc.metadata
            )
            
            # Preserve original length for quality metrics
            processed_doc.metadata['original_length'] = len(doc.text)
            processed_doc.metadata['processed_length'] = len(normalized_text)
            
            processed_docs.append(processed_doc)
        
        return processed_docs
    
    def filter_low_quality_documents(self, documents: List[Document], min_length=50, max_length=10000) -> List[Document]:
        """Filter out documents that are too short or too long"""
        filtered_docs = []
        
        for doc in documents:
            text_length = len(doc.text)
            
            # Check if document meets quality criteria
            if min_length <= text_length <= max_length:
                # Add quality score to metadata
                doc.metadata['quality_score'] = self.calculate_quality_score(doc.text)
                filtered_docs.append(doc)
        
        return filtered_docs
    
    def calculate_quality_score(self, text: str) -> float:
        """Calculate a simple quality score based on text characteristics"""
        if len(text) == 0:
            return 0.0
        
        # Simple heuristics for quality
        word_count = len(text.split())
        sentence_count = len(re.split(r'[.!?]+', text))
        
        # Avoid division by zero
        if sentence_count == 0:
            return 0.0
        
        avg_words_per_sentence = word_count / sentence_count
        
        # Quality factors (adjust weights as needed)
        length_score = min(len(text) / 1000, 1.0)  # Prefer longer documents
        coherence_score = 1.0 if 5 <= avg_words_per_sentence <= 25 else 0.5  # Prefer coherent sentences
        
        quality_score = (length_score * 0.7) + (coherence_score * 0.3)
        return quality_score
