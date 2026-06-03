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

def main():
    system = "You are a helpful assistant. If you don't know the answer, say you don't know."
    chat_history = []

    collection = vector_embedder.get_collection()
    vector_embedder.embed_data(collection=collection)

    while True:

        print("\n\n-------------------------------")
        question = input("Ask your question (q to quit): ")
        print("\n\n")
        if question == "q":
            break

        relevant_docs = vector_embedder.retrieve(question, n=3, collection=collection)
        messages = [
                {"role": "system", "content": system},
                *chat_history,
                {"role": "user", "content": f"Here are some relevant documents: {relevant_docs}\nQuestion: {question}"}
            ]

        result = chat(messages)
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": result})

        print(result)

if __name__ == "__main__":
    main()
