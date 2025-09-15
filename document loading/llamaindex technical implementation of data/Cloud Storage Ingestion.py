# S3 Ingestion
def load_from_s3(bucket_name, prefix="", aws_access_key_id=None, aws_secret_access_key=None):
    """Load documents from AWS S3"""
    from llama_index.readers.s3 import S3Reader
    
    loader = S3Reader(
        bucket=bucket_name,
        key=prefix,
        aws_access_id=aws_access_key_id,
        aws_access_secret=aws_secret_access_key
    )
    
    documents = loader.load_data()
    
    # Add metadata
    for doc in documents:
        doc.metadata['source_type'] = 's3'
        doc.metadata['bucket'] = bucket_name
    
    return documents

# Google Cloud Storage Ingestion
def load_from_gcs(bucket_name, prefix=""):
    """Load documents from Google Cloud Storage"""
    from llama_index.readers.gcs import GCSReader
    
    loader = GCSReader(
        bucket=bucket_name,
        key=prefix
    )
    
    documents = loader.load_data()
    
    # Add metadata
    for doc in documents:
        doc.metadata['source_type'] = 'gcs'
        doc.metadata['bucket'] = bucket_name
    
    return documents
