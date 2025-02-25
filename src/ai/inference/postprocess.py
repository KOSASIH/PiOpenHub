import torch

def postprocess_output(outputs) -> list:
    """Postprocess the model outputs to extract predictions."""
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)
    return predictions.tolist()
