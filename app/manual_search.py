from sklearn.metrics.pairwise import cosine_similarity
from bson import ObjectId
from embedding_functions import query_embedding
from connect import papers_collection
import numpy as np

def get_cosine_similarity(query, paper_id):
    """
    Compares the query embedding with the paper's embedding using cosine similarity.
    """
    # Generate the query embedding
    query_embed = query_embedding(query)
    
    # Ensure the query_embed is a numpy array (if it is a list)
    query_embed = np.array(query_embed)
    
    # Fetch the paper's embedding from the database
    paper_data = papers_collection.find_one({"_id": ObjectId(paper_id)})
    
    if not paper_data:
        print(f"Paper with ID {paper_id} not found.")
        return None
    
    paper_embed = np.array(paper_data.get("embedding_paper"))
    
    if paper_embed is None:
        print(f"Embedding for paper {paper_id} is missing.")
        return None
    
    # Reshape the embeddings for cosine similarity calculation
    query_embed = query_embed.reshape(1, -1)
    paper_embed = paper_embed.reshape(1, -1)
    
    # Calculate cosine similarity
    similarity_score = cosine_similarity(query_embed, paper_embed)[0][0]
    
    return similarity_score

def search_similar_papers(query, top_k=5):
    """
    Searches for papers based on cosine similarity of the embeddings.
    """
    # List to store similarity results
    similarity_results = []
    
    # Iterate over papers in the collection and compare embeddings
    for paper in papers_collection.find():
        paper_id = paper['_id']
        similarity_score = get_cosine_similarity(query, paper_id)
        
        if similarity_score is not None:
            similarity_results.append({
                "paper_id": paper_id,
                "title": paper.get("title"),
                "abstract": paper.get("abstract"),  # Include the abstract
                "similarity_score": similarity_score
            })
    
    # Sort by similarity score in descending order
    similarity_results = sorted(similarity_results, key=lambda x: x['similarity_score'], reverse=True)
    
    # Return top_k similar papers
    return similarity_results[:top_k]

query = "AI Deep Learning"
results = search_similar_papers(query)

print(f"Top {len(results)} most similar papers to the query:")
for result in results:
    print(f"Paper ID: {result['paper_id']}, Title: {result['title']}, Similarity Score: {result['similarity_score']}")
    print(f"Abstract: {result['abstract']}\n")  # Print the abstract as well
