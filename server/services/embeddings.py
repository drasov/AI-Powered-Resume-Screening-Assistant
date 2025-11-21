# server/services/embeddings.py

from __future__ import annotations

from typing import Iterable, List

from sentence_transformers import SentenceTransformer
import torch

# Load the model once when the service module is imported
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def get_model() -> SentenceTransformer:
    # Return the shared SentenceTransformer model instance
    return _model


def embed_texts(texts: Iterable[str]) -> torch.Tensor:
    # Generate embeddings for a list of texts
    texts = [str(t) for t in texts]
    embeddings = _model.encode(
        texts,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )
    # Return tensor of shape [n_texts, embedding_dim]
    return embeddings
