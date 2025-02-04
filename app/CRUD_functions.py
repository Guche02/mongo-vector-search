from connect import users_collection
from embedding_functions import generate_embedding
from bson import ObjectId  

def insert_user(name, email, age, review):
    """
    Inserts a new user into the database and automatically generates their embedding.
    """
    user_data = {
        "name": name,
        "email": email,
        "age": age,
        "review": review,
        "embedding_user": generate_embedding({"name": name, "email": email, "age": age, "review": review})
    }
    
    result = users_collection.insert_one(user_data)
    print(f"New user added with ID {result.inserted_id}")

def update_user(user_id, name=None, email=None, age=None, review=None):
    """
    Updates the details of a user and regenerates their embedding.
    """
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)  
    
    updated_data = {}
    
    if name:
        updated_data["name"] = name
    if email:
        updated_data["email"] = email
    if age:
        updated_data["age"] = age
    if review:
        updated_data["review"] = review
    
    result = users_collection.update_one(
        {"_id": user_id},
        {"$set": updated_data}
    )
    
    if result.modified_count > 0:
        print(f"User {user_id} updated successfully.")

        user_data = users_collection.find_one({"_id": user_id})
        embedding = generate_embedding(user_data)

        users_collection.update_one(
            {"_id": user_id},
            {"$set": {"embedding_user": embedding}}
        )
        print(f"Embedding regenerated for user {user_id}.")
    else:
        print(f"No updates were made for user {user_id}. Check if the user ID exists.")

