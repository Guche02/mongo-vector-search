from pymongo.operations import SearchIndexModel
from connect import papers_collection
from embedding_functions import query_embedding
import time

index_name = "default"
existing_indexes = list(papers_collection.list_search_indexes())
index_exists = any(index['name'] == index_name for index in existing_indexes)

if not index_exists:
    search_index_model = SearchIndexModel(
        {
  "mappings": {
    "dynamic": True,
    "fields": {
      "embedding_paper": {
        "dimensions": 384,
        "similarity": "cosine",
        "type": "knnVector"
      }
    }
  }
}
    )

    papers_collection.create_search_index(model=search_index_model)
    print(f"Index '{index_name}' created successfully.")
else:
    print(f"Index '{index_name}' already exists, using the existing index.")

print("Polling to check if the index is ready. This may take up to a minute.")
predicate = lambda index: index.get("queryable") is True

while True:
    indices = list(papers_collection.list_search_indexes(index_name))
    if len(indices) and predicate(indices[0]):
        break
    time.sleep(5)

print(index_name + " is ready for querying.")

def get_query_results(query):
    """Gets results from a vector search query."""
    
    query_embed = query_embedding(query)
    
    pipeline = [
        {
            "$search": {
                "index": "default",
                "knnBeta": {
                    "vector": query_embed,
                    "path": "embedding_paper",
                    "k": 5  # Number of closest results to return
                }
            }
        },
        {
            "$project": {
                "_id": 0,  
                "title":1,
                "abstract":1,
                "keywords":1,
                 "Similarity Score": { "$meta": "searchScore" }
            }
        }
    ]
    
    results = list(papers_collection.aggregate(pipeline))  # Ensure results are a list
    return results