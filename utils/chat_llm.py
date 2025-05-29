from src.llm_class import LLMClient  

def chat_loop():
    client = LLMClient()

    print("\n🤖 LLM Terminal Chat")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Optional: You could allow a default prompt or load one from config
        prompt = "Respond as a helpful assistant."

        response = client.send_chat_request(user_input, prompt)
        print(f"LLM: {response}\n")


if __name__ == "__main__":
    chat_loop()
