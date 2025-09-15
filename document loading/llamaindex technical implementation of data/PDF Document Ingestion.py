from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader
import os

# Load PDF documents
def load_pdfs(pdf_paths):
    """Load PDF documents from file paths"""
    reader = PDFReader()
    documents = []
    
    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            docs = reader.load_data(file_path=pdf_path)
            # Add source metadata
            for doc in docs:
                doc.metadata['source_type'] = 'pdf'
                doc.metadata['source_path'] = pdf_path
            documents.extend(docs)
    
    return documents

# Alternative: Load from directory
def load_pdfs_from_directory(directory_path):
    """Load all PDFs from a directory"""
    reader = SimpleDirectoryReader(
        input_dir=directory_path,
        required_exts=[".pdf"],
        recursive=True
    )
    documents = reader.load_data()
    
    # Add metadata
    for doc in documents:
        doc.metadata['source_type'] = 'pdf'
    
    return documents
