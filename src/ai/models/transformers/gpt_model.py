import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from typing import List, Dict, Any

class GPTModel:
    def __init__(self, model_name: str = 'gpt2'):
        """Initialize the GPT model and tokenizer."""
        self.model_name = model_name
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)

    def encode_input(self, prompt: str, max_length: int = 50) -> Dict[str, Any]:
        """Encode the input prompt for the GPT model."""
        return self.tokenizer.encode(prompt, return_tensors='pt', max_length=max_length, truncation=True)

    def generate_text(self, prompt: str, max_length: int = 50, num_return_sequences: int = 1) -> List[str]:
        """Generate text based on the input prompt."""
        self.model.eval()  # Set the model to evaluation mode
        with torch.no_grad():
            input_ids = self.encode_input(prompt)
            outputs = self.model.generate(
                input_ids,
                max_length=max_length,
                num_return_sequences=num_return_sequences,
                no_repeat_ngram_size=2,
                early_stopping=True
            )
            return [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

# Example usage
if __name__ == "__main__":
    # Initialize the GPT model
    gpt_model = GPTModel()

    # Example prompt for text generation
    prompt = "Once upon a time in a land far, far away"
    generated_texts = gpt_model.generate_text(prompt, max_length=100, num_return_sequences=3)

    print("Generated Texts:")
    for i, text in enumerate(generated_texts):
        print(f"Text {i + 1}: {text}")
