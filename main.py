from tkinter.messagebox import YES

import ollama
import vector_embedder

import tools
import speech2text

def chat(messages: list, model: str = "llama3.1:8b", provider: str = "ollama") -> str:
    if provider == "ollama":
        response = ollama.chat(model=model, messages=messages, tools=tools.tool_registry)
        return response["message"]
    
        # # httpx version - llama expects pretty much just a dict with the same entires as the .chat method

        # payload = {"model": model, "messages": messages, "tools": tools.tool_registry, "stream": False}
        # response = httpx.post("http://localhost:11434/api/chat", json=payload)
        # return response.json()["message"]

        # # Then just parse the resulting dict and its "content" and "tool_calls" entries
    
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
    system = """You are a helpful personal assistant with access to the user's documents and tools.
    - For casual conversation, respond naturally. Never mention JSON, tools, documents, or functions in your responses unless directly asked about them.
    - For document questions, summarize relevant documents and reference the filename
    - For tool requests, use the available tools
    - Keep responses concise
    
    For tools:
    - When I listen to music I do so on spotify
    - When I need to take notes quickly I do so in notepad
    - When using the press_key_combination tool, respond with JSON and with the keys in a string separated by commas
    - When i say "italian" you should press keycombination "alt i" 
    - When i say "normal" you should press keycombination "alt y" """
    
    chat_history = []
    collection = vector_embedder.get_collection()
    vector_embedder.embed_data(collection=collection)

    while True:
        # Threading to check both for voice input and text input?
        print("\n\n-------------------------------")
        # question = speech2text.speech2text()
        question = input("Ask your question (q to quit): ")
        print("\n\n")
        if question == "q":
            break

        relevant_docs = vector_embedder.retrieve(question, collection=collection)
        
        if relevant_docs:
            docs_string = "\n\n".join(relevant_docs)
            user_content = f"Here are some relevant documents:\n{docs_string}\n\nQuestion: {question}"
        else:
            user_content = question

        messages = [
            {"role": "system", "content": system},
            *chat_history,
            {"role": "user", "content": user_content}
        ]

        response = chat(messages)

        # check if tool call or normal response
        if response.get("tool_calls"):
            for tool_call in response["tool_calls"]:
                name = tool_call["function"]["name"]
                args = tool_call["function"].get("arguments", {})
                tools.tool_functions[name](**args)
                print(f"Executed tool: {name}")

        else:
            result = response["content"]
            chat_history.append({"role": "user", "content": question})
            chat_history.append({"role": "assistant", "content": result})
            print(result)

if __name__ == "__main__":
    main()
