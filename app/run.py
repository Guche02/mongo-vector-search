from CRUD_functions import update_user, insert_user
from search_operation import get_query_results

# # For inserting the users
# insert_user("Looza Subedy", "looza@example.com", 28, "Great product! Highly recommended.")

# # For updating the users
# update_user("insert_user_id_here", name="Updated Name", review="Updated review.")

# For search operations
# Example query string you want to search for in your users' embeddings

query = "Looza"

# Call the get_query_results function to get the search results
results = get_query_results(query)
print("Search results for query:", query)
print(results)
for result in results:
    print(result)

# # List all existing indexes
# indices = list(users_collection.list_search_indexes())
# print(indices)

# # # Drop a specific index (if no longer needed)
# # users_collection.drop_search_index("your_index_name")
