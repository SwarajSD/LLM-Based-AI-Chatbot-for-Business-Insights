import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os


def load_model(model_dir="./model1"):
    """Loads a pre-trained LLM model and tokenizer."""
    try:
        if not os.path.exists(model_dir):
            raise FileNotFoundError(
                f"Model directory {model_dir} not found. Please download the model.")

        print("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        print("Tokenizer loaded!")

        print("Loading model...")
        model = AutoModelForCausalLM.from_pretrained(
            model_dir, device_map="auto", trust_remote_code=True)
        print("Model loaded successfully!")

        return model, tokenizer
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None
