from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  

def generate_embedding(user):
    """
    Generates an embedding for a given user using their name, email, and review.
    """
    user_text = f"{user.get('name', '')} {user.get('email', '')} {user.get('age', '')} {user.get('review', '')}"
    return model.encode(user_text).tolist()  


def query_embedding(query):
    """
    Creates an embedding for the query string using the SentenceTransformer model.
    The query is treated as a single input string.
    """
    # Generate embedding for the query text
    return model.encode(query).tolist()  # Return the embedding as a list