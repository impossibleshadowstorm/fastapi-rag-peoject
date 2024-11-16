from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://elasticsearch:9200"])  # Change to your ES instance


def index_document(document_id, content):
    es.index(index="documents", id=document_id, body={"content": content})


def search_document_content(document_id, query):
    """
    Search for relevant content in Elasticsearch based on document_id and query.
    """
    body = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"_id": str(document_id)}},  # Match specific document ID
                    {"match": {"content": query}},  # Search query in content
                ]
            }
        }
    }

    result = es.search(index="documents", body=body)
    hits = result.get("hits", {}).get("hits", [])

    # Concatenate relevant content from the hits
    return " ".join(hit["_source"]["content"] for hit in hits) if hits else ""
