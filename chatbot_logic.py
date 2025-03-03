from faiss_manager import FAISSManager
from model_loader import load_model
import torch

# Initialize FAISS manager
db_manager = FAISSManager()

# Load LLM model
model, tokenizer = load_model()


def retrieve_business_insights(user_query):
    """Retrieve relevant business insights from FAISS."""
    retrieved_docs = db_manager.retrieve_similar_docs(user_query, top_k=2)
    return "\n".join(retrieved_docs) if retrieved_docs else "No relevant insights found."


def generate_llm_response(user_query, insights):
    """Generate an AI response using the LLM model with prompt engineering."""
    try:
        prompt_template = (
            "You are a helpful AI assistant that provides business insights.\n"
            "When relevant information is available, summarize it concisely before answering the question.\n"
            "If no relevant insights are found, provide a general business recommendation.\n"
            "Use professional and concise language.\n\n"
            "### User Query:\n{query}\n\n"
            "### Relevant Business Insights:\n{insights}\n\n"
            "### AI Response:\n"
        )

        context = prompt_template.format(
            query=user_query, insights=insights if insights else "No insights available."
        )
        inputs = tokenizer(context, return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=150,
                temperature=0.7,
                top_p=0.9
            )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response if response else "I couldn't generate a response."
    except Exception as e:
        print(f"Error during response generation: {e}")
        return "An error occurred while generating the response."


def chat_with_bot(user_query):
    """Handles chatbot responses by combining retrieval and LLM generation."""
    insights = retrieve_business_insights(user_query)
    response = generate_llm_response(user_query, insights)

    return f"📊 Relevant Insights:\n{insights}\n\n🤖 AI Response:\n{response}"
