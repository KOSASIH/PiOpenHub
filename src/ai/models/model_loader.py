import torch
from transformers import BertModel, GPT2Model, BertTokenizer, GPT2Tokenizer
from typing import Any, Dict

class ModelLoader:
    def __init__(self, model_name: str, framework: str = 'pytorch'):
        self.model_name = model_name
        self.framework = framework
        self.model = self.load_model()
        self.tokenizer = self.load_tokenizer()

    def load_model(self) -> Any:
        """Load the specified pre-trained model."""
        if self.framework == 'pytorch':
            if self.model_name == 'bert':
                return BertModel.from_pretrained('bert-base-uncased')
            elif self.model_name == 'gpt':
                return GPT2Model.from_pretrained('gpt2')
            else:
                raise ValueError(f"Model '{self.model_name}' is not recognized for PyTorch.")
        elif self.framework == 'tensorflow':
            # Placeholder for TensorFlow model loading
            raise NotImplementedError("TensorFlow model loading is not implemented yet.")
        else:
            raise ValueError(f"Framework '{self.framework}' is not supported.")

    def load_tokenizer(self) -> Any:
        """Load the tokenizer corresponding to the model."""
        if self.model_name == 'bert':
            return BertTokenizer.from_pretrained('bert-base-uncased')
        elif self.model_name == 'gpt':
            return GPT2Tokenizer.from_pretrained('gpt2')
        else:
            raise ValueError(f"Tokenizer for model '{self.model_name}' is not recognized.")

    def get_model(self) -> Any:
        """Return the loaded model."""
        return self.model

    def get_tokenizer(self) -> Any:
        """Return the loaded tokenizer."""
        return self.tokenizer

    def encode_input(self, text: str, max_length: int = 512) -> Dict[str, Any]:
        """Encode input text for the model."""
        return self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt' if self.framework == 'pytorch' else 'tf'
        )

# Example usage
if __name__ == "__main__":
    model_loader = ModelLoader(model_name='bert', framework='pytorch')
    model = model_loader.get_model()
    tokenizer = model_loader.get_tokenizer()

    # Example text for encoding
    text = "Hello, this is a test input for the BERT model."
    encoded_input = model_loader.encode_input(text)
    print("Encoded Input:", encoded_input)
