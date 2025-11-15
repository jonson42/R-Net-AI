import logging
import asyncio
from typing import List, Dict, Any, Union
from sentence_transformers import SentenceTransformer
import torch
import numpy as np

from config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings from text using sentence transformers"""
    
    def __init__(self):
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = settings.embedding_model_name
        self.batch_size = settings.embedding_batch_size
        
    def _load_model(self):
        """Lazy load the embedding model"""
        if self.model is None:
            logger.info(f"Loading embedding model: {self.model_name} on {self.device}")
            try:
                self.model = SentenceTransformer(self.model_name, device=self.device)
                logger.info(f"✓ Embedding model loaded successfully (dimension: {self.model.get_sentence_embedding_dimension()})")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise RuntimeError(f"Failed to load embedding model: {e}")
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for a single text
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            self._load_model()
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(
                None,
                lambda: self.model.encode(text, convert_to_numpy=True)
            )
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise ValueError(f"Failed to generate embedding: {e}")
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embedding vectors for multiple texts in batch
        
        Args:
            texts: List of input texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            self._load_model()
            
            if not texts:
                return []
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None,
                lambda: self.model.encode(
                    texts,
                    batch_size=self.batch_size,
                    convert_to_numpy=True,
                    show_progress_bar=len(texts) > 10
                )
            )
            
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise ValueError(f"Failed to generate batch embeddings: {e}")
    
    async def get_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            embeddings = await self.generate_embeddings_batch([text1, text2])
            
            # Calculate cosine similarity
            emb1 = np.array(embeddings[0])
            emb2 = np.array(embeddings[1])
            
            similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Failed to calculate similarity: {e}")
            raise ValueError(f"Failed to calculate similarity: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current embedding model"""
        try:
            self._load_model()
            
            return {
                "model_name": self.model_name,
                "device": self.device,
                "dimension": self.model.get_sentence_embedding_dimension(),
                "max_seq_length": self.model.max_seq_length,
                "batch_size": self.batch_size
            }
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            return {
                "model_name": self.model_name,
                "device": self.device,
                "error": str(e)
            }


# Global service instance
embedding_service = EmbeddingService()
