from sqlalchemy import create_engine, text
from llama_index.core import Document
import pymongo

# SQL Database Ingestion
def load_from_sql(connection_string, query):
    """Load data from SQL database"""
    engine = create_engine(connection_string)
    
    with engine.connect() as connection:
        result = connection.execute(text(query))
        rows = result.fetchall()
        
        documents = []
        for row in rows:
            # Convert row to document
            content = " ".join([str(value) for value in row])
            doc = Document(
                text=content,
                metadata={
                    'source_type': 'sql',
                    'table': query.split('FROM')[1].split()[0] if 'FROM' in query else 'unknown'
                }
            )
            documents.append(doc)
    
    return documents

# MongoDB Ingestion
def load_from_mongodb(connection_string, database, collection, filter_query=None):
    """Load data from MongoDB"""
    client = pymongo.MongoClient(connection_string)
    db = client[database]
    collection = db[collection]
    
    # Apply filter if provided
    cursor = collection.find(filter_query or {})
    
    documents = []
    for doc in cursor:
        # Convert MongoDB document to LlamaIndex Document
        content = str(doc)  # Or extract specific fields
        llama_doc = Document(
            text=content,
            metadata={
                'source_type': 'mongodb',
                'database': database,
                'collection': collection.name,
                '_id': str(doc.get('_id'))
            }
        )
        documents.append(llama_doc)
    
    client.close()
    return documents
