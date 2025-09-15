class AdvancedPreprocessor(DataPreprocessor):
    def __init__(self):
        super().__init__()
        self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    
    def extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from text"""
        words = text.lower().split()
        # Simple term extraction (you might want to use NLP libraries like spaCy)
        key_terms = [word for word in words if len(word) > 3 and word not in self.stop_words]
        return list(set(key_terms))[:10]  # Return top 10 unique terms
    
    def detect_language(self, text: str) -> str:
        """Detect language of text (simplified version)"""
        # In production, use libraries like langdetect
        return 'en'  # Default to English
    
    def enhanced_preprocessing(self, documents: List[Document]) -> List[Document]:
        """Apply enhanced preprocessing with metadata enrichment"""
        processed_docs = self.preprocess_documents(documents)
        
        for doc in processed_docs:
            # Add enhanced metadata
            doc.metadata['key_terms'] = self.extract_key_terms(doc.text)
            doc.metadata['language'] = self.detect_language(doc.text)
            doc.metadata['processing_timestamp'] = datetime.now().isoformat()
            
            # Calculate additional quality metrics
            doc.metadata['word_count'] = len(doc.text.split())
            doc.metadata['sentence_count'] = len(re.split(r'[.!?]+', doc.text))
        
        return processed_docs
