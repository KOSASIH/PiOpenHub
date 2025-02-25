import torch
from torch.utils.data import DataLoader
from transformers import AdamW
from models.model_loader import ModelLoader
from training.data_loader import load_data
from training.callbacks import EarlyStopping

def train(model_name: str, epochs: int, batch_size: int, learning_rate: float):
    # Load data
    train_data = load_data()
    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

    # Load model
    model_loader = ModelLoader(model_name=model_name)
    model = model_loader.get_model()
    model.train()

    # Set up optimizer
    optimizer = AdamW(model.parameters(), lr=learning_rate)

    # Set up early stopping
    early_stopping = EarlyStopping(patience=3, verbose=True)

    for epoch in range(epochs):
        total_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()
            inputs = model_loader.encode_input(batch['texts'])
            labels = batch['labels']
            outputs = model(**inputs, labels=labels)
            loss = outputs.loss
            total_loss += loss.item()
            loss.backward()
            optimizer.step()

        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch + 1}/{epochs}, Average Loss: {avg_loss:.4f}")

        # Check for early stopping
        early_stopping(avg_loss, model)

        if early_stopping.early_stop:
            print("Early stopping triggered.")
            break

if __name__ == "__main__":
    train(model_name='bert', epochs=10, batch_size=32, learning_rate=5e-5)
