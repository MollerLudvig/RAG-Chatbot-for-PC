import ollama
import chromadb
import os

def get_collection(db_location="db"):
    client = chromadb.PersistentClient(path=db_location)
    return client.get_or_create_collection(name="documents")

def embed_data(dir="C:/Users/molle/Desktop", file_types=[".txt"], collection=None):
    
    # Get already embedded filenames from db
    existing = collection.get()["ids"]
    
    for filename in os.listdir(dir):
        name, ext = os.path.splitext(filename)
        if ext in file_types and name != "AI Usage": # only consider specified file types
            if filename not in existing: # only embed if not already in db
                with open(os.path.join(dir, filename), "r") as f:
                    text = f.read()

                    text_to_embed = f"Filename: {filename}\nContent: {text}"
                    response = ollama.embed(model='qwen3-embedding:8b', input=text_to_embed)

                    collection.add(
                        ids=[filename],
                        embeddings=[response["embeddings"][0]],
                        documents=[text_to_embed],
                        metadatas=[{"filename": filename}]
                    )
                    print(f"Embedded: {filename}")
            else:
                print(f"Skipping {filename}, already in db")

# Embedd query and retrieve relevant docs
def retrieve(question, n=3, collection=None):
    response = ollama.embed(model='qwen3-embedding:8b', input=question)
    results = collection.query(
        query_embeddings=[response["embeddings"][0]],
        n_results=n
    )
    return results["documents"][0]