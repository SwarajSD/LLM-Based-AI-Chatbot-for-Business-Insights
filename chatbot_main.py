from chatbot_logic import chat_with_bot

if __name__ == "__main__":
    print("🤖 Business Insights Chatbot: Type 'exit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = chat_with_bot(user_input)
        print("AI Chatbot:", response)
