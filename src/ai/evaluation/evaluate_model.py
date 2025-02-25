import torch
from torch.utils.data import DataLoader
from models.model_loader import ModelLoader
from evaluation.metrics import calculate_accuracy, calculate_f1_score
from evaluation.visualization import plot_metrics
from training.data_loader import load_data  # Assuming you have a data loader

def evaluate(model_name: str, test_data_path: str):
    """Evaluate the model on the test dataset."""
    # Load test data
    test_data = load_data(file_path=test_data_path)
    test_loader = DataLoader(test_data, batch_size=32, shuffle=False)

    # Load model
    model_loader = ModelLoader(model_name=model_name)
    model = model_loader.get_model()
    model.eval()  # Set the model to evaluation mode

    all_predictions = []
    all_labels = []

    with torch.no_grad():
        for batch in test_loader:
            inputs = model_loader.encode_input(batch['texts'])
            labels = batch['labels']
            outputs = model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)

            all_predictions.extend(predictions.tolist())
            all_labels.extend(labels.tolist())

    # Calculate metrics
    accuracy = calculate_accuracy(all_labels, all_predictions)
    f1 = calculate_f1_score(all_labels, all_predictions)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")

    # Visualize metrics
    plot_metrics(all_labels, all_predictions)

if __name__ == "__main__":
    evaluate(model_name='bert', test_data_path='data/test.csv')
