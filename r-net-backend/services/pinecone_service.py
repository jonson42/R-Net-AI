import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import PineconeException

from config import settings
from services.embedding_service import embedding_service

logger = logging.getLogger(__name__)


class PineconeService:
    """Service for managing Pinecone vector database operations"""
    
    def __init__(self):
        self.pc = None
        self.index = None
        self._initialized = False
        
    def _initialize(self):
        """Initialize Pinecone connection and index"""
        if self._initialized:
            return
            
        try:
            if not settings.pinecone_api_key:
                logger.warning("Pinecone API key not configured - service disabled")
                return
            
            logger.info("Initializing Pinecone connection...")
            self.pc = Pinecone(api_key=settings.pinecone_api_key)
            
            # Check if index exists, create if not
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if settings.pinecone_index_name not in existing_indexes:
                logger.info(f"Creating Pinecone index: {settings.pinecone_index_name}")
                self.pc.create_index(
                    name=settings.pinecone_index_name,
                    dimension=settings.pinecone_dimension,
                    metric=settings.pinecone_metric,
                    spec=ServerlessSpec(
                        cloud='aws',
                        region=settings.pinecone_environment or 'us-east-1'
                    )
                )
                logger.info("✓ Pinecone index created successfully")
            else:
                logger.info(f"✓ Pinecone index '{settings.pinecone_index_name}' already exists")
            
            # Connect to index
            self.index = self.pc.Index(settings.pinecone_index_name)
            self._initialized = True
            logger.info("✓ Pinecone service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            self._initialized = False
            raise RuntimeError(f"Failed to initialize Pinecone: {e}")
    
    async def test_connection(self) -> bool:
        """Test Pinecone connection"""
        try:
            self._initialize()
            if not self.index:
                return False
                
            # Get index stats as connection test
            stats = self.index.describe_index_stats()
            logger.info(f"Pinecone connection test successful - {stats['total_vector_count']} vectors in index")
            return True
            
        except Exception as e:
            logger.error(f"Pinecone connection test failed: {e}")
            return False
    
    async def upsert_code_generation(
        self,
        generation_id: str,
        project_name: str,
        description: str,
        tech_stack: Dict[str, str],
        files: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store code generation result in Pinecone for semantic search
        
        Args:
            generation_id: Unique identifier for this generation
            project_name: Name of the project
            description: Project description
            tech_stack: Technology stack used
            files: List of generated files
            metadata: Additional metadata
            
        Returns:
            Dictionary with upsert results
        """
        try:
            self._initialize()
            
            # Create searchable text from generation
            search_text = f"{project_name}. {description}"
            
            # Add tech stack info
            tech_info = ", ".join([f"{k}: {v}" for k, v in tech_stack.items()])
            search_text += f" Tech stack: {tech_info}"
            
            # Add file summaries
            file_summary = ", ".join([f['path'] for f in files[:10]])  # First 10 files
            search_text += f" Files: {file_summary}"
            
            # Generate embedding
            embedding = await embedding_service.generate_embedding(search_text)
            
            # Prepare metadata
            vector_metadata = {
                "generation_id": generation_id,
                "project_name": project_name,
                "description": description,
                "tech_stack": tech_info,
                "file_count": len(files),
                "created_at": datetime.utcnow().isoformat(),
                **(metadata or {})
            }
            
            # Upsert to Pinecone
            self.index.upsert(
                vectors=[(generation_id, embedding, vector_metadata)],
                namespace="code_generations"
            )
            
            logger.info(f"Stored code generation in Pinecone: {generation_id}")
            
            return {
                "success": True,
                "generation_id": generation_id,
                "dimension": len(embedding),
                "metadata": vector_metadata
            }
            
        except Exception as e:
            logger.error(f"Failed to upsert to Pinecone: {e}")
            raise ValueError(f"Failed to store in Pinecone: {e}")
    
    async def search_similar_projects(
        self,
        query: str,
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar code generation projects
        
        Args:
            query: Search query text
            top_k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of similar projects with scores
        """
        try:
            self._initialize()
            
            # Generate query embedding
            query_embedding = await embedding_service.generate_embedding(query)
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                namespace="code_generations",
                filter=filter_dict
            )
            
            # Format results
            formatted_results = []
            for match in results['matches']:
                formatted_results.append({
                    "generation_id": match['id'],
                    "score": float(match['score']),
                    "metadata": match.get('metadata', {})
                })
            
            logger.info(f"Found {len(formatted_results)} similar projects for query: {query}")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search Pinecone: {e}")
            raise ValueError(f"Failed to search: {e}")
    
    async def upsert_code_snippet(
        self,
        snippet_id: str,
        code: str,
        language: str,
        description: str,
        tags: List[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store individual code snippet for reusability
        
        Args:
            snippet_id: Unique identifier for the snippet
            code: Code content
            language: Programming language
            description: Snippet description
            tags: List of tags
            metadata: Additional metadata
            
        Returns:
            Dictionary with upsert results
        """
        try:
            self._initialize()
            
            # Create searchable text
            search_text = f"{description}. Language: {language}. {code[:500]}"  # First 500 chars of code
            
            if tags:
                search_text += f" Tags: {', '.join(tags)}"
            
            # Generate embedding
            embedding = await embedding_service.generate_embedding(search_text)
            
            # Prepare metadata
            vector_metadata = {
                "snippet_id": snippet_id,
                "language": language,
                "description": description,
                "tags": tags or [],
                "code_length": len(code),
                "created_at": datetime.utcnow().isoformat(),
                **(metadata or {})
            }
            
            # Upsert to Pinecone
            self.index.upsert(
                vectors=[(snippet_id, embedding, vector_metadata)],
                namespace="code_snippets"
            )
            
            logger.info(f"Stored code snippet in Pinecone: {snippet_id}")
            
            return {
                "success": True,
                "snippet_id": snippet_id,
                "dimension": len(embedding),
                "metadata": vector_metadata
            }
            
        except Exception as e:
            logger.error(f"Failed to upsert snippet: {e}")
            raise ValueError(f"Failed to store snippet: {e}")
    
    async def search_code_snippets(
        self,
        query: str,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant code snippets
        
        Args:
            query: Search query
            language: Filter by programming language
            tags: Filter by tags
            top_k: Number of results
            
        Returns:
            List of matching snippets
        """
        try:
            self._initialize()
            
            # Generate query embedding
            query_embedding = await embedding_service.generate_embedding(query)
            
            # Build filter
            filter_dict = {}
            if language:
                filter_dict["language"] = {"$eq": language}
            if tags:
                filter_dict["tags"] = {"$in": tags}
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                namespace="code_snippets",
                filter=filter_dict if filter_dict else None
            )
            
            # Format results
            formatted_results = []
            for match in results['matches']:
                formatted_results.append({
                    "snippet_id": match['id'],
                    "score": float(match['score']),
                    "metadata": match.get('metadata', {})
                })
            
            logger.info(f"Found {len(formatted_results)} code snippets for query: {query}")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search snippets: {e}")
            raise ValueError(f"Failed to search snippets: {e}")
    
    async def delete_vector(self, vector_id: str, namespace: str = "code_generations") -> bool:
        """Delete a vector by ID"""
        try:
            self._initialize()
            self.index.delete(ids=[vector_id], namespace=namespace)
            logger.info(f"Deleted vector: {vector_id} from namespace: {namespace}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete vector: {e}")
            return False
    
    async def get_index_stats(self) -> Dict[str, Any]:
        """Get Pinecone index statistics"""
        try:
            self._initialize()
            stats = self.index.describe_index_stats()
            
            return {
                "total_vectors": stats.get('total_vector_count', 0),
                "dimension": stats.get('dimension', settings.pinecone_dimension),
                "index_fullness": stats.get('index_fullness', 0),
                "namespaces": stats.get('namespaces', {})
            }
        except Exception as e:
            logger.error(f"Failed to get index stats: {e}")
            return {"error": str(e)}
    
    async def clear_namespace(self, namespace: str) -> bool:
        """Clear all vectors from a namespace"""
        try:
            self._initialize()
            self.index.delete(delete_all=True, namespace=namespace)
            logger.info(f"Cleared namespace: {namespace}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear namespace: {e}")
            return False


# Global service instance
pinecone_service = PineconeService()
