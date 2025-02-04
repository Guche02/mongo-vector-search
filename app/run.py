from CRUD_functions import update_user, insert_user
from search_operation import get_query_results
from connect import users_collection

# # For inserting the users
# insert_user("Arnab M", "A@example.com", 28, "Worst product! Very negative experience")

# # For updating the users
# update_user("insert_user_id_here", name="Updated Name", review="Updated review.")

# For search operations
# Example query string you want to search for in your users' embeddings

query = "negative"

# Call the get_query_results function to get the search results
results = get_query_results(query)
print("Search results for query:", query)
for result in results:
    print(result)

# # List all existing indexes
# indices = list(users_collection.list_search_indexes())
# print(indices)

# # # Drop a specific index (if no longer needed)
# # users_collection.drop_search_index("your_index_name")
