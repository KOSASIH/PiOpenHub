# src/ai/llm_integration.py

import os
import logging
from typing import List, Dict, Any, Optional, Union
import requests
import json

class LLMIntegration:
    """
    Integration with Large Language Models (LLMs) for advanced AI capabilities.
    
    This class provides methods to interact with various LLM providers,
    including OpenAI, Hugging Face, and local models.
    """
    
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        """
        Initialize the LLM integration.
        
        Args:
            provider (str): LLM provider ("openai", "huggingface", or "local")
            api_key (str, optional): API key for the provider
        """
        self.provider = provider.lower()
        self.api_key = api_key or os.environ.get(f"{provider.upper()}_API_KEY")
        self.logger = logging.getLogger(__name__)
        
        # Validate provider
        valid_providers = ["openai", "huggingface", "local"]
        if self.provider not in valid_providers:
            raise ValueError(f"Invalid provider: {provider}. Must be one of {valid_providers}")
            
        # Validate API key
        if self.provider != "local" and not self.api_key:
            self.logger.warning(f"No API key provided for {provider}. Set the {provider.upper()}_API_KEY environment variable.")
            
    def generate_text(
        self, 
        prompt: str, 
        max_tokens: int = 100,
        temperature: float = 0.7,
        model: Optional[str] = None
    ) -> str:
        """
        Generate text using the configured LLM provider.
        
        Args:
            prompt (str): Input prompt
            max_tokens (int): Maximum number of tokens to generate
            temperature (float): Sampling temperature (0.0 to 1.0)
            model (str, optional): Model to use (provider-specific)
            
        Returns:
            str: Generated text
        """
        if self.provider == "openai":
            return self._generate_openai(prompt, max_tokens, temperature, model or "gpt-3.5-turbo")
        elif self.provider == "huggingface":
            return self._generate_huggingface(prompt, max_tokens, temperature, model or "gpt2")
        elif self.provider == "local":
            return self._generate_local(prompt, max_tokens, temperature, model)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
            
    def _generate_openai(
        self, 
        prompt: str, 
        max_tokens: int,
        temperature: float,
        model: str
    ) -> str:
        """Generate text using OpenAI API."""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            else:
                self.logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return f"Error: {response.status_code}"
        except Exception as e:
            self.logger.error(f"Error generating text with OpenAI: {e}")
            return f"Error: {str(e)}"
            
    def _generate_huggingface(
        self, 
        prompt: str, 
        max_tokens: int,
        temperature: float,
        model: str
    ) -> str:
        """Generate text using Hugging Face API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{model}",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()[0]["generated_text"].strip()
            else:
                self.logger.error(f"Hugging Face API error: {response.status_code} - {response.text}")
                return f"Error: {response.status_code}"
        except Exception as e:
            self.logger.error(f"Error generating text with Hugging Face: {e}")
            return f"Error: {str(e)}"
            
    def _generate_local(
        self, 
        prompt: str, 
        max_tokens: int,
        temperature: float,
        model: Optional[str]
    ) -> str:
        """Generate text using a local model."""
        # This would typically involve loading a local model
        # For demonstration, return a placeholder
        self.logger.warning("Local model generation not implemented. Returning placeholder.")
        return f"[Local model would generate text based on: {prompt[:30]}...]"
        
    def embed_text(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Generate embeddings for the given text.
        
        Args:
            text (str): Text to embed
            model (str, optional): Model to use for embeddings
            
        Returns:
            list: Vector embedding
        """
        if self.provider == "openai":
            return self._embed_openai(text, model or "text-embedding-ada-002")
        elif self.provider == "huggingface":
            return self._embed_huggingface(text, model or "sentence-transformers/all-MiniLM-L6-v2")
        else:
            raise ValueError(f"Embeddings not supported for provider: {self.provider}")
            
    def _embed_openai(self, text: str, model: str) -> List[float]:
        """Generate embeddings using OpenAI API."""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": model,
                "input": text
            }
            
            response = requests.post(
                "https://api.openai.com/v1/embeddings",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()["data"][0]["embedding"]
            else:
                self.logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            self.logger.error(f"Error generating embeddings with OpenAI: {e}")
            return []
            
    def _embed_huggingface(self, text: str, model: str) -> List[float]:
        """Generate embeddings using Hugging Face API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "inputs": text
            }
            
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{model}",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                # Hugging Face returns a list of lists for batched inputs
                # We're only sending one input, so we take the first list
                return response.json()[0]
            else:
                self.logger.error(f"Hugging Face API error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            self.logger.error(f"Error generating embeddings with Hugging Face: {e}")
            return []
            
    def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 100
    ) -> Dict[str, Any]:
        """
        Create a chat completion using the configured LLM provider.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content'
            model (str, optional): Model to use
            temperature (float): Sampling temperature
            max_tokens (int): Maximum number of tokens to generate
            
        Returns:
            dict: Chat completion response
        """
        if self.provider != "openai":
            self.logger.warning(f"Chat completions are best supported by OpenAI. Using {self.provider} may give unexpected results.")
            
            # Convert chat format to text prompt for non-OpenAI providers
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            text = self.generate_text(prompt, max_tokens, temperature, model)
            
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": text
                        }
                    }
                ]
            }
            
        # OpenAI chat completion
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": model or "gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code}"}
        except Exception as e:
            self.logger.error(f"Error creating chat completion: {e}")
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Initialize LLM integration with OpenAI
    llm = LLMIntegration(provider="openai")
    
    # Generate text
    prompt = "Explain quantum computing in simple terms."
    response = llm.generate_text(prompt, max_tokens=150)
    print(f"Generated text: {response}")
    
    # Create chat completion
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What are the benefits of edge computing?"}
    ]
    chat_response = llm.create_chat_completion(messages)
    print(f"Chat response: {chat_response['choices'][0]['message']['content']}")
    
    # Generate embeddings
    text = "This is a sample text for embedding."
    embeddings = llm.embed_text(text)
    print(f"Embedding dimension: {len(embeddings)}")