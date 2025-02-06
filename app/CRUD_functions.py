from connect import papers_collection
from embedding_functions import generate_embedding
from bson import ObjectId  

def insert_paper(title, abstract, keywords):
    """
    Inserts a new research paper into the database and automatically generates its embedding.
    """
    paper_data = {
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "embedding_paper": generate_embedding({"title": title, "abstract": abstract, "keywords": keywords})
    }
    
    result = papers_collection.insert_one(paper_data)
    print(f"New research paper added with ID {result.inserted_id}")

def update_paper(paper_id, title=None, abstract=None, keywords=None):
    """
    Updates the details of a research paper and regenerates its embedding.
    """
    if isinstance(paper_id, str):
        paper_id = ObjectId(paper_id)  
    
    updated_data = {}
    
    if title:
        updated_data["title"] = title
    if abstract:
        updated_data["abstract"] = abstract
    if keywords:
        updated_data["keywords"] = keywords
    
    result = papers_collection.update_one(
        {"_id": paper_id},
        {"$set": updated_data}
    )
    
    if result.modified_count > 0:
        print(f"Research paper {paper_id} updated successfully.")

        paper_data = papers_collection.find_one({"_id": paper_id})
        embedding = generate_embedding(paper_data)

        papers_collection.update_one(
            {"_id": paper_id},
            {"$set": {"embedding_paper": embedding}}
        )
        print(f"Embedding regenerated for research paper {paper_id}.")
    else:
        print(f"No updates were made for research paper {paper_id}. Check if the paper ID exists.")
