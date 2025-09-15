import requests
import json

def load_from_api(api_url, headers=None, params=None, json_path=None):
    """Load data from API response"""
    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()
    
    try:
        data = response.json()
    except json.JSONDecodeError:
        # If not JSON, treat as text
        data = {'content': response.text}
    
    documents = []
    
    # Extract content based on JSON path or use entire response
    if json_path:
        # Simple JSON path extraction (you might want to use jsonpath-ng for complex paths)
        content = data
        for key in json_path.split('.'):
            if isinstance(content, dict) and key in content:
                content = content[key]
            else:
                content = str(data)
                break
    else:
        content = str(data)
    
    doc = Document(
        text=str(content),
        metadata={
            'source_type': 'api',
            'url': api_url,
            'status_code': response.status_code
        }
    )
    documents.append(doc)
    
    return documents
