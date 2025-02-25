from transformers import BertTokenizer
from typing import List, Dict, Any

def preprocess_input(texts: List[str], tokenizer: BertTokenizer, max_length: int = 512) -> Dict[str, Any]:
    """Preprocess the input texts for the model."""
    return tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors='pt'
    )
