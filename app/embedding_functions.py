from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  

def generate_embedding(paper):
    """
    Generates an embedding for a given research paper using its title, abstract, and keywords.
    """
    paper_text = f"{paper.get('title', '')} {paper.get('abstract', '')} {paper.get('keywords', '')}"
    return model.encode(paper_text).tolist()


def query_embedding(query):
    """
    Creates an embedding for the query string using the SentenceTransformer model.
    The query is treated as a single input string.
    """
    return model.encode(query).tolist()  