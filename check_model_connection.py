import ollama

MODEL_NAME = "qwen2.5:3b"

if __name__ == "__main__":
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": "Explain RAG in three short sentences."}],
    )
    print(response.message.content)
