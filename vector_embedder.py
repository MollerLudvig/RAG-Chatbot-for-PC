import ollama
import chromadb
import os

def get_collection(db_location="db"):
    client = chromadb.PersistentClient(path=db_location)
    return client.get_or_create_collection(name="documents")

def embed_data(dir="C:/Users/Ludvig/Desktop", file_types=[".txt"], files_not_included=["AI Usage", "AI master prompts"], collection=None):
    
    # Get already embedded filenames from db
    existing = collection.get()["ids"]
    
    for filename in os.listdir(dir):
        name, ext = os.path.splitext(filename)
        if ext in file_types and name not in files_not_included: # only consider specified file types
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
def retrieve(question, n=3, collection=None, threshold=1.0):
    response = ollama.embed(model='qwen3-embedding:8b', input=question)
    results = collection.query(
        query_embeddings=[response["embeddings"][0]],
        n_results=n
    )
    for doc, dist in zip(results["documents"][0], results["distances"][0]):
        print(f"Distance: {dist:.4f} | Doc: {doc[:50]}...")
    
    docs = [doc for doc, dist in zip(results["documents"][0], results["distances"][0])
            if dist < threshold]
    return docs