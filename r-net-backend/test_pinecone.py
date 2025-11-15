"""
Test script for Pinecone integration
Run this after setting up Pinecone credentials in .env
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.embedding_service import embedding_service
from services.pinecone_service import pinecone_service
from config import settings


async def test_embedding_service():
    """Test embedding generation"""
    print("\n" + "="*50)
    print("Testing Embedding Service")
    print("="*50)
    
    try:
        # Test single embedding
        print("\n1. Testing single text embedding...")
        text = "React authentication with JWT tokens"
        embedding = await embedding_service.generate_embedding(text)
        print(f"✓ Generated embedding with dimension: {len(embedding)}")
        print(f"  First 5 values: {embedding[:5]}")
        
        # Test batch embeddings
        print("\n2. Testing batch embeddings...")
        texts = [
            "FastAPI REST API with PostgreSQL",
            "React dashboard with charts",
            "Django authentication system"
        ]
        embeddings = await embedding_service.generate_embeddings_batch(texts)
        print(f"✓ Generated {len(embeddings)} embeddings")
        print(f"  Each with dimension: {len(embeddings[0])}")
        
        # Test similarity
        print("\n3. Testing similarity calculation...")
        text1 = "React authentication system"
        text2 = "React login with auth"
        similarity = await embedding_service.get_similarity(text1, text2)
        print(f"✓ Similarity between texts: {similarity:.4f}")
        print(f"  Text 1: '{text1}'")
        print(f"  Text 2: '{text2}'")
        
        # Get model info
        print("\n4. Getting model info...")
        info = embedding_service.get_model_info()
        print(f"✓ Model: {info['model_name']}")
        print(f"  Device: {info['device']}")
        print(f"  Dimension: {info['dimension']}")
        print(f"  Max sequence length: {info['max_seq_length']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Embedding test failed: {e}")
        return False


async def test_pinecone_service():
    """Test Pinecone operations"""
    print("\n" + "="*50)
    print("Testing Pinecone Service")
    print("="*50)
    
    if not settings.pinecone_api_key:
        print("⚠ Pinecone API key not configured - skipping Pinecone tests")
        return False
    
    try:
        # Test connection
        print("\n1. Testing Pinecone connection...")
        connected = await pinecone_service.test_connection()
        if connected:
            print("✓ Successfully connected to Pinecone")
        else:
            print("✗ Failed to connect to Pinecone")
            return False
        
        # Store a test code generation
        print("\n2. Testing code generation storage...")
        test_gen_id = "test_generation_001"
        result = await pinecone_service.upsert_code_generation(
            generation_id=test_gen_id,
            project_name="test-project",
            description="A test e-commerce application with shopping cart",
            tech_stack={
                "frontend": "React",
                "backend": "FastAPI",
                "database": "PostgreSQL"
            },
            files=[
                {"path": "frontend/App.js", "description": "Main React app"},
                {"path": "backend/main.py", "description": "FastAPI backend"}
            ],
            metadata={"test": True}
        )
        print(f"✓ Stored generation: {result['generation_id']}")
        
        # Search for similar projects
        print("\n3. Testing project search...")
        search_results = await pinecone_service.search_similar_projects(
            query="shopping cart application",
            top_k=3
        )
        print(f"✓ Found {len(search_results)} similar projects")
        for i, result in enumerate(search_results, 1):
            print(f"  {i}. {result['metadata'].get('project_name', 'Unknown')} "
                  f"(score: {result['score']:.4f})")
        
        # Store a test code snippet
        print("\n4. Testing code snippet storage...")
        test_snippet_id = "test_snippet_001"
        snippet_result = await pinecone_service.upsert_code_snippet(
            snippet_id=test_snippet_id,
            code="async def authenticate_user(token: str): return verify_jwt(token)",
            language="python",
            description="JWT authentication function for FastAPI",
            tags=["python", "fastapi", "authentication", "jwt"],
            metadata={"test": True}
        )
        print(f"✓ Stored snippet: {snippet_result['snippet_id']}")
        
        # Search for code snippets
        print("\n5. Testing snippet search...")
        snippet_results = await pinecone_service.search_code_snippets(
            query="authentication function",
            language="python",
            top_k=5
        )
        print(f"✓ Found {len(snippet_results)} snippets")
        for i, result in enumerate(snippet_results, 1):
            print(f"  {i}. {result['snippet_id']} (score: {result['score']:.4f})")
        
        # Get index stats
        print("\n6. Getting index statistics...")
        stats = await pinecone_service.get_index_stats()
        print(f"✓ Total vectors: {stats.get('total_vectors', 0)}")
        print(f"  Dimension: {stats.get('dimension', 0)}")
        namespaces = stats.get('namespaces', {})
        for ns, ns_stats in namespaces.items():
            print(f"  Namespace '{ns}': {ns_stats.get('vector_count', 0)} vectors")
        
        # Clean up test data
        print("\n7. Cleaning up test data...")
        await pinecone_service.delete_vector(test_gen_id, "code_generations")
        await pinecone_service.delete_vector(test_snippet_id, "code_snippets")
        print("✓ Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Pinecone test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("R-Net AI - Pinecone Integration Tests")
    print("="*50)
    
    print(f"\nConfiguration:")
    print(f"  Pinecone API Key: {'✓ Set' if settings.pinecone_api_key else '✗ Not set'}")
    print(f"  Pinecone Environment: {settings.pinecone_environment or 'Not set'}")
    print(f"  Pinecone Index: {settings.pinecone_index_name}")
    print(f"  Embedding Model: {settings.embedding_model_name}")
    print(f"  Embedding Dimension: {settings.pinecone_dimension}")
    
    # Test embedding service
    embedding_success = await test_embedding_service()
    
    # Test Pinecone service
    pinecone_success = await test_pinecone_service()
    
    # Summary
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    print(f"Embedding Service: {'✓ PASSED' if embedding_success else '✗ FAILED'}")
    print(f"Pinecone Service:  {'✓ PASSED' if pinecone_success else '✗ FAILED or SKIPPED'}")
    
    if embedding_success and (pinecone_success or not settings.pinecone_api_key):
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
