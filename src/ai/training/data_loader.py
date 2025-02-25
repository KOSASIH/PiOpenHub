import pandas as pd
from torch.utils.data import Dataset

class TextDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return {
            'texts': self.texts[idx],
            'labels': self.labels[idx]
        }

def load_data(file_path: str = 'data/train.csv') -> TextDataset:
    """Load data from a CSV file and return a TextDataset."""
    df = pd.read_csv(file_path)
    texts = df['text'].tolist()
    labels = df['label'].tolist()
    return TextDataset(texts, labels)
