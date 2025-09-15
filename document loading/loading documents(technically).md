## Technical Data Ingestion in RAG Systems with LangChain

### 1. **Database Ingestion (SQL/NoSQL)**

#### **SQL Databases**
```python
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from sqlalchemy import create_engine

# Connect to SQL database
engine = create_engine("postgresql://user:password@localhost:5432/mydb")
db = SQLDatabase(engine)

# Load data using custom queries
from langchain.document_loaders import SQLDatabaseLoader

loader = SQLDatabaseLoader(
    connection_string="postgresql://user:password@localhost:5432/mydb",
    query="SELECT id, title, content FROM articles WHERE updated_at > '2023-01-01'"
)

documents = loader.load()
```

#### **NoSQL Databases (MongoDB Example)**
```python
from langchain.document_loaders import PyMongoLoader

# Load from MongoDB
loader = PyMongoLoader(
    connection_string="mongodb://localhost:27017/",
    db_name="knowledge_base",
    collection_name="documents",
    filter_criteria={"status": "published"}
)

documents = loader.load()
```

### 2. **Cloud Storage Ingestion**

#### **Amazon S3**
```python
from langchain.document_loaders import S3FileLoader, S3DirectoryLoader

# Load single file from S3
loader = S3FileLoader(
    bucket="my-company-docs",
    key="documents/annual_report.pdf",
    aws_access_key_id="YOUR_ACCESS_KEY",
    aws_secret_access_key="YOUR_SECRET_KEY"
)

# Load entire directory
directory_loader = S3DirectoryLoader(
    bucket="my-company-docs",
    prefix="knowledge_base/",
    aws_access_key_id="YOUR_ACCESS_KEY",
    aws_secret_access_key="YOUR_SECRET_KEY"
)

documents = directory_loader.load()
```

#### **Google Cloud Storage**
```python
from langchain.document_loaders import GCSDirectoryLoader, GCSFileLoader

# Load from GCS
loader = GCSDirectoryLoader(
    project_name="my-gcp-project",
    bucket="company-knowledge-bucket",
    prefix="documents/"
)

documents = loader.load()
```

### 3. **API Data Ingestion**

#### **REST APIs**
```python
from langchain.document_loaders import APILoader
import requests

# Custom API loader
class CustomAPILoader:
    def __init__(self, api_url, headers=None):
        self.api_url = api_url
        self.headers = headers or {}
    
    def load(self):
        response = requests.get(self.api_url, headers=self.headers)
        data = response.json()
        
        documents = []
        for item in data:
            doc = Document(
                page_content=item.get('content', ''),
                metadata={
                    'source': self.api_url,
                    'id': item.get('id'),
                    'timestamp': item.get('created_at')
                }
            )
            documents.append(doc)
        
        return documents

# Usage
loader = CustomAPILoader(
    api_url="https://api.company.com/v1/articles",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

documents = loader.load()
```

### 4. **Web Scraping**

#### **Web Page Scraping**
```python
from langchain.document_loaders import WebBaseLoader, AsyncChromiumLoader
from langchain.document_loaders.parsers import BS4Parser

# Simple web scraping
loader = WebBaseLoader([
    "https://example.com/article1",
    "https://example.com/article2"
])

documents = loader.load()

# Advanced scraping with parsing
loader = AsyncChromiumLoader([
    "https://example.com/dynamic-content"
])

html_docs = loader.load()
parser = BS4Parser()
parsed_docs = parser.parse(html_docs)
```

### 5. **Real-Time Data Streams**

#### **Kafka Integration**
```python
from langchain.document_loaders import KafkaLoader
from kafka import KafkaConsumer
import json

# Custom Kafka loader for streaming data
class StreamingKafkaLoader:
    def __init__(self, bootstrap_servers, topic, group_id):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
    
    def load_stream(self, max_documents=100):
        documents = []
        count = 0
        
        for message in self.consumer:
            if count >= max_documents:
                break
                
            data = message.value
            doc = Document(
                page_content=data.get('content', ''),
                metadata={
                    'source': 'kafka',
                    'timestamp': data.get('timestamp'),
                    'topic': message.topic
                }
            )
            documents.append(doc)
            count += 1
            
        return documents

# Usage
loader = StreamingKafkaLoader(
    bootstrap_servers=['localhost:9092'],
    topic='document-stream',
    group_id='rag-ingestion'
)

streaming_docs = loader.load_stream(max_documents=50)
```

### 6. **File System Ingestion**

#### **Local File Systems**
```python
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load multiple file types from directory
def load_directory(path):
    loader = DirectoryLoader(
        path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    
    documents = loader.load()
    
    # Also load text files
    txt_loader = DirectoryLoader(
        path,
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    
    txt_documents = txt_loader.load()
    documents.extend(txt_documents)
    
    return documents

documents = load_directory("/path/to/documents")
```

### 7. **Production-Level Orchestration with LangChain**

#### **Unified Ingestion Pipeline**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import asyncio
from concurrent.futures import ThreadPoolExecutor

class MultiSourceIngestionPipeline:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
    async def ingest_from_source(self, source_config):
        """Ingest from a single source"""
        source_type = source_config['type']
        
        if source_type == 's3':
            loader = S3DirectoryLoader(
                bucket=source_config['bucket'],
                prefix=source_config.get('prefix', ''),
                aws_access_key_id=source_config.get('access_key'),
                aws_secret_access_key=source_config.get('secret_key')
            )
        elif source_type == 'sql':
            loader = SQLDatabaseLoader(
                connection_string=source_config['connection_string'],
                query=source_config['query']
            )
        elif source_type == 'api':
            loader = CustomAPILoader(
                api_url=source_config['url'],
                headers=source_config.get('headers', {})
            )
        # Add more source types as needed
        
        # Load documents
        documents = loader.load()
        
        # Process documents
        processed_docs = self.process_documents(documents, source_config)
        
        return processed_docs
    
    def process_documents(self, documents, source_config):
        """Process documents: split, add metadata, etc."""
        # Add source-specific metadata
        for doc in documents:
            doc.metadata.update({
                'source_type': source_config['type'],
                'ingestion_timestamp': datetime.now().isoformat(),
                'source_id': source_config.get('source_id', 'unknown')
            })
        
        # Split documents
        chunks = self.text_splitter.split_documents(documents)
        return chunks
    
    async def run_pipeline(self, sources):
        """Run ingestion pipeline for multiple sources"""
        tasks = [self.ingest_from_source(source) for source in sources]
        results = await asyncio.gather(*tasks)
        
        # Flatten results
        all_chunks = []
        for chunks in results:
            all_chunks.extend(chunks)
        
        return all_chunks

# Usage
pipeline = MultiSourceIngestionPipeline()

sources = [
    {
        'type': 's3',
        'bucket': 'company-docs',
        'prefix': 'reports/',
        'access_key': 'YOUR_KEY',
        'secret_key': 'YOUR_SECRET',
        'source_id': 'quarterly_reports'
    },
    {
        'type': 'sql',
        'connection_string': 'postgresql://...',
        'query': 'SELECT * FROM articles WHERE published_date > NOW() - INTERVAL 30 DAYS',
        'source_id': 'recent_articles'
    },
    {
        'type': 'api',
        'url': 'https://api.company.com/documents',
        'headers': {'Authorization': 'Bearer TOKEN'},
        'source_id': 'external_docs'
    }
]

# Run the pipeline
chunks = asyncio.run(pipeline.run_pipeline(sources))
```

### 8. **Change Detection and Incremental Updates**

```python
class IncrementalIngestionManager:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.last_processed = {}
    
    def detect_changes(self, source_config):
        """Detect what has changed since last ingestion"""
        source_id = source_config['source_id']
        last_run = self.last_processed.get(source_id, datetime.min)
        
        # Implementation depends on source type
        if source_config['type'] == 'sql':
            # Check for updated records
            updated_query = f"{source_config['query']} AND updated_at > '{last_run}'"
            source_config['query'] = updated_query
        
        return source_config
    
    async def incremental_ingest(self, sources):
        """Perform incremental ingestion"""
        updated_sources = [self.detect_changes(source) for source in sources]
        pipeline = MultiSourceIngestionPipeline()
        new_chunks = await pipeline.run_pipeline(updated_sources)
        
        # Update last processed timestamps
        for source in sources:
            self.last_processed[source['source_id']] = datetime.now()
        
        return new_chunks
```

### 9. **Production Considerations**

#### **Error Handling and Retry Logic**
```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator

# Apply to ingestion methods
@retry_on_failure(max_retries=3, delay=2)
async def ingest_from_source(self, source_config):
    # Implementation here
    pass
```

#### **Monitoring and Logging**
```python
import logging
from datetime import datetime

class IngestionMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def log_ingestion_stats(self, source_id, documents_count, chunks_count, duration):
        self.logger.info(f"Ingestion completed for {source_id}: "
                        f"{documents_count} documents, "
                        f"{chunks_count} chunks, "
                        f"in {duration} seconds")
    
    def log_error(self, source_id, error):
        self.logger.error(f"Ingestion failed for {source_id}: {error}")
```

This technical implementation shows how LangChain orchestrates ingestion from diverse sources in production RAG systems, handling complexity, scalability, and reliability requirements.
