from pymongo.operations import SearchIndexModel
from connect import users_collection
from embedding_functions import query_embedding
import time

index_name = "new"

# Check if the index already exists
existing_indexes = list(users_collection.list_search_indexes())
index_exists = any(index['name'] == index_name for index in existing_indexes)

if not index_exists:
    # Create the new search index if it doesn't exist
    search_index_model = SearchIndexModel(
        {
  "mappings": {
    "dynamic": True,
    "fields": {
      "user_embedding": {
        "dimensions": 384,
        "similarity": "cosine",
        "type": "knnVector"
      }
    }
  }
}
    )

    users_collection.create_search_index(model=search_index_model)
    print(f"Index '{index_name}' created successfully.")
else:
    print(f"Index '{index_name}' already exists, using the existing index.")

# Polling to check if the index is ready. This may take up to a minute.
print("Polling to check if the index is ready. This may take up to a minute.")
predicate = lambda index: index.get("queryable") is True

while True:
    indices = list(users_collection.list_search_indexes(index_name))
    if len(indices) and predicate(indices[0]):
        break
    time.sleep(5)

print(index_name + " is ready for querying.")

def get_query_results(query):
    """Gets results from a vector search query."""
    # Generate the embedding for the query using the new query_embedding function
    query_embed = query_embedding(query)
    
    # Define the aggregation pipeline for the vector search
    pipeline = [
  {
    "$search": {
      "index": "new",
      "text": {
        "query": query,
        "path": {
          "wildcard": "*",
        },
      },
    },
  },
  {
            "$project": {
                "_id": 0,  # Exclude the _id field
                "name": 1,  # You can also include other fields like name, email, etc.
                "email": 1,
                "age": 1,  # Include the 'text' field (or any other fields you want to keep)
                "review": 1,  # Include the 'text' field (or any other fields you want to keep)
            }
        }
]
    
    # Execute the aggregation pipeline on the users collection
    results = users_collection.aggregate(pipeline)
    
    # Collect and return the results
    array_of_results = []
    for doc in results:
        array_of_results.append(doc)
    
    return array_of_results
