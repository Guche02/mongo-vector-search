from CRUD_functions import update_paper, insert_paper
from search_operation import get_query_results
# from connect import papers_collection

# # For inserting the research papers  
# insert_paper("Deep Learning for Image Recognition",  
#     "This paper explores the use of deep learning models for image recognition. "
#     "We discuss architectures like CNNs, ResNets, and transformers, highlighting their effectiveness in various tasks, "
#     "from object detection to medical imaging.",  
#     "Machine Learning, CNN, AI")  

# # For updating the users
# update_user("insert_user_id_here", name="Updated Name", review="Updated review.")

# For search operations
# Example query string you want to search for in your users' embeddings

query = "AI Deep Learning"

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
