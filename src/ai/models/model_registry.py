from typing import Any, Dict
from models.model_loader import ModelLoader

class ModelRegistry:
    def __init__(self):
        self.models: Dict[str, ModelLoader] = {}

    def register_model(self, model_name: str, framework: str = 'pytorch') -> None:
        """Register a new model in the registry."""
        if model_name in self.models:
            raise ValueError(f"Model '{model_name}' is already registered.")
        
        model_loader = ModelLoader(model_name=model_name, framework=framework)
        self.models[model_name] = model_loader
        print(f"Model '{model_name}' registered successfully.")

    def get_model(self, model_name: str) -> Any:
        """Retrieve a model from the registry."""
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' is not registered.")
        
        return self.models[model_name].get_model()

    def get_tokenizer(self, model_name: str) -> Any:
        """Retrieve the tokenizer for a registered model."""
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' is not registered.")
        
        return self.models[model_name].get_tokenizer()

    def list_models(self) -> None:
        """List all registered models."""
        if not self.models:
            print("No models registered.")
        else:
            print("Registered Models:")
            for model_name in self.models:
                print(f"- {model_name}")

# Example usage
if __name__ == "__main__":
    registry = ModelRegistry()
    
    # Register models
    registry.register_model(model_name='bert', framework='pytorch')
    registry.register_model(model_name='gpt', framework='pytorch')

    # List registered models
    registry.list_models()

    # Retrieve a model and its tokenizer
    bert_model = registry.get_model('bert')
    bert_tokenizer = registry.get_tokenizer('bert')
    print("Retrieved BERT Model:", bert_model)
    print("Retrieved BERT Tokenizer:", bert_tokenizer)
