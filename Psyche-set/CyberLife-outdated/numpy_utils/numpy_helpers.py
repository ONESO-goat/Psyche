# numpy_helpers.py

import numpy as np
import base64
from typing import Optional
import json

def serialize_numpy(arr: np.ndarray) -> dict:
    """Convert numpy array to JSON-serializable format."""
    return {
        "__numpy__": base64.b64encode(arr.tobytes()).decode('utf-8'),
        "dtype": str(arr.dtype),
        "shape": list(arr.shape)
    }

def deserialize_numpy(data: dict):
    """Convert JSON format back to numpy array."""
    if "__numpy__" not in data:
        raise KeyError("")
    
    # Decode base64
    buffer = base64.b64decode(data["__numpy__"])
    
    # Reconstruct array
    arr = np.frombuffer(buffer, dtype=data["dtype"])
    
    # Reshape
    return arr.reshape(data["shape"])


def encode_memory(memory_dict: dict) -> dict:
    """
    Recursively convert all numpy arrays in memory to JSON format.
    """
    encoded = {}
    
    for key, value in memory_dict.items():
        if isinstance(value, np.ndarray):
            encoded[key] = serialize_numpy(value)
        elif isinstance(value, dict):
            encoded[key] = encode_memory(value)  # Recursive
        else:
            encoded[key] = value
    
    return encoded


def decode_memory(memory_dict: dict) -> dict:
    """
    Recursively convert JSON numpy format back to actual numpy arrays.
    """
    decoded = {}
    
    for key, value in memory_dict.items():
        if isinstance(value, dict):
            # Check if it's a numpy array
            if "__numpy__" in value:
                decoded[key] = deserialize_numpy(value)
            else:
                decoded[key] = decode_memory(value)  # Recursive
        else:
            decoded[key] = value
    
    return decoded