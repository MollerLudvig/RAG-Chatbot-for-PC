from tkinter.messagebox import YES

import ollama
import vector_embedder


def chat(messages: list, model: str = "llama3.1:8b", provider: str = "ollama") -> str:
    if provider == "ollama":
        response = ollama.chat(model=model, messages=messages)
        return response["message"]["content"]
    
    elif provider == "anthropic":
        pass
    
    elif provider == "openai":
        pass

def needs_retrieval(question):
    response = ollama.chat(model="llama3.1:8b", messages=[
        {"role": "system", "content": "You are a classifier. You must respond with ONLY the word YES or NO. Nothing else."},
        {"role": "user", "content": f"""Question: {question}

        Does answering this require looking up personal documents or files?
        Think: does this question ask about something personal, specific to the user, or stored in their files?
        Answer YES or NO."""}
        ])
    return "YES" in response["message"]["content"].upper()

def main():
    # System prompt that currently instructs to reference and answer only about the retrieved documents
    # Can be modified to act more as a helpful assistant rather than just a document retriever and summarizer
    
    system = """You are a personal document assistant. Your job is to help the user find and summarize information from their personal files.

    RULES:
    - When answering from documents, always reference the exact filename you got the information from
    - Summarize what is in the document concisely, do not elaborate beyond what is written
    - Do not add information that is not in the provided documents
    - If no documents are provided or relevant, answer briefly from general knowledge
    - If you don't know, say so directly without padding"""

    chat_history = []

    collection = vector_embedder.get_collection()
    vector_embedder.embed_data(collection=collection)

    while True:

        # Ask user for prompt
        print("\n\n-------------------------------")
        question = input("Ask your question (q to quit): ")
        print("\n\n")
        if question == "q":
            break

        # Get and use relevant documents if needed
        relevant_docs = vector_embedder.retrieve(question, n=3, collection=collection)
        user_content = f"Here are some relevant documents:\n{relevant_docs}\n\nQuestion: {question}"

        messages = [
                {"role": "system", "content": system},
                *chat_history,
                {"role": "user", "content": user_content}
            ]
        result = chat(messages)

        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": result})

        print(result)

if __name__ == "__main__":
    main()
