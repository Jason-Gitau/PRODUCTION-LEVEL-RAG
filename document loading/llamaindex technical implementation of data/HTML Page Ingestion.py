from llama_index.readers.web import SimpleWebPageReader
from llama_index.readers.web import BeautifulSoupWebReader
import requests
from bs4 import BeautifulSoup

def load_html_pages(urls):
    """Load HTML pages from URLs"""
    # Simple approach
    reader = SimpleWebPageReader()
    documents = reader.load_data(urls)
    
    # Add metadata
    for i, doc in enumerate(documents):
        doc.metadata['source_type'] = 'html'
        doc.metadata['url'] = urls[i]
    
    return documents

def load_html_with_custom_parsing(urls, selectors=None):
    """Load HTML with custom parsing using BeautifulSoup"""
    reader = BeautifulSoupWebReader()
    documents = reader.load_data(urls, custom_hostname='example.com')
    
    # Add metadata
    for i, doc in enumerate(documents):
        doc.metadata['source_type'] = 'html'
        doc.metadata['url'] = urls[i]
    
    return documents
