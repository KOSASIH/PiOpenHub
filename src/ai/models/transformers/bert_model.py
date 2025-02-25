import torch
from transformers import BertModel, BertTokenizer, BertForSequenceClassification
from typing import List, Dict, Any

class BERTModel:
    def __init__(self, model_name: str = 'bert-base-uncased', num_labels: int = 2):
        """Initialize the BERT model and tokenizer."""
        self.model_name = model_name
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

    def encode_input(self, texts: List[str], max_length: int = 512) -> Dict[str, Any]:
        """Encode input texts for the BERT model."""
        return self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors='pt'
        )

    def predict(self, texts: List[str]) -> List[int]:
        """Perform inference on the input texts."""
        self.model.eval()  # Set the model to evaluation mode
        with torch.no_grad():
            inputs = self.encode_input(texts)
            outputs = self.model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
            return predictions.tolist()

    def fine_tune(self, train_dataloader, optimizer, num_epochs: int = 3) -> None:
        """Fine-tune the BERT model on a specific task."""
        self.model.train()  # Set the model to training mode
        for epoch in range(num_epochs):
            for batch in train_dataloader:
                optimizer.zero_grad()
                inputs = self.encode_input(batch['texts'])
                labels = batch['labels']
                outputs = self.model(**inputs, labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
            print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}")

# Example usage
if __name__ == "__main__":
    # Initialize the BERT model
    bert_model = BERTModel(num_labels=2)

    # Example texts for prediction
    texts = ["I love programming!", "I hate bugs."]
    predictions = bert_model.predict(texts)
    print("Predictions:", predictions)

    # Fine-tuning would require a DataLoader and optimizer setup, which is not included here.
