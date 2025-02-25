import torch
from models.model_loader import ModelLoader
from inference.preprocess import preprocess_input
from inference.postprocess import postprocess_output

def run_inference(model_name: str, input_texts: list):
    """Run inference on the input texts using the specified model."""
    model_loader = ModelLoader(model_name=model_name)
    model = model_loader.get_model()
    tokenizer = model_loader.get_tokenizer()
    model.eval()  # Set the model to evaluation mode

    with torch.no_grad():
        # Preprocess the input texts
        inputs = preprocess_input(input_texts, tokenizer)
        outputs = model(**inputs)
        
        # Postprocess the outputs
        predictions = postprocess_output(outputs)
        
    return predictions

if __name__ == "__main__":
    # Example input texts for inference
    input_texts = [
        "I love programming!",
        "The weather is terrible today."
    ]
    
    predictions = run_inference(model_name='bert', input_texts=input_texts)
    print("Predictions:", predictions)
