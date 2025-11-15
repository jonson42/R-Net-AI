# Pinecone Integration Guide

## Overview

R-Net AI now includes **Pinecone vector database integration** for semantic code search and intelligent code snippet management. This feature enables:

- 🔍 **Semantic Search** - Find similar projects using natural language queries
- 📚 **Code Snippet Library** - Store and retrieve reusable code patterns
- 🤖 **Automatic Indexing** - Generated code is automatically stored for future reference
- 🎯 **Smart Recommendations** - Get relevant code suggestions based on context

## Features

### 1. **Automatic Project Storage**
Every code generation is automatically stored in Pinecone with:
- Project description and metadata
- Technology stack information
- File structure and descriptions
- Timestamp and validation status

### 2. **Semantic Project Search**
Search for similar projects using natural language:
```bash
curl -X POST http://localhost:8000/pinecone/search/projects \
  -H "Content-Type: application/json" \
  -d '{
    "query": "e-commerce shopping cart with payment",
    "top_k": 5
  }'
```

### 3. **Code Snippet Management**
Store reusable code snippets:
```bash
curl -X POST http://localhost:8000/pinecone/snippets/store \
  -H "Content-Type: application/json" \
  -d '{
    "snippet_id": "jwt-auth-middleware",
    "code": "async def verify_token(token: str): ...",
    "language": "python",
    "description": "JWT authentication middleware",
    "tags": ["authentication", "jwt", "security"]
  }'
```

Search for snippets:
```bash
curl -X POST http://localhost:8000/pinecone/snippets/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "authentication middleware",
    "language": "python",
    "top_k": 10
  }'
```

## Setup Instructions

### 1. Get Pinecone API Key

1. Sign up at [Pinecone.io](https://www.pinecone.io/)
2. Create a new project
3. Copy your API key from the dashboard
4. Note your environment (e.g., `us-east-1`)

### 2. Configure Environment Variables

Add to your `.env` file:

```bash
# Pinecone Configuration
PINECONE_API_KEY=your_api_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=rnet-ai-embeddings
PINECONE_DIMENSION=384
PINECONE_METRIC=cosine

# Embedding Model Configuration
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
EMBEDDING_BATCH_SIZE=32
```

### 3. Install Dependencies

```bash
cd r-net-backend
pip install -r requirements.txt
```

This installs:
- `pinecone-client` - Pinecone SDK
- `sentence-transformers` - Text embedding models
- `torch` - PyTorch for ML models
- `transformers` - Hugging Face transformers

### 4. Start the Server

```bash
python main.py
```

The server will:
- Test Pinecone connection on startup
- Create index if it doesn't exist
- Load the embedding model (first run downloads ~90MB)

## API Endpoints

### Health Check
```bash
GET /health
```

Returns Pinecone connection status:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "openai_connected": true,
  "pinecone_connected": true
}
```

### Search Similar Projects
```bash
POST /pinecone/search/projects
```

Request:
```json
{
  "query": "real-time chat application with websockets",
  "top_k": 5,
  "tech_stack_filter": {
    "frontend": "React"
  }
}
```

Response:
```json
{
  "success": true,
  "query": "real-time chat application with websockets",
  "results": [
    {
      "generation_id": "gen_abc123",
      "score": 0.89,
      "metadata": {
        "project_name": "chat-app",
        "description": "Real-time messaging app",
        "tech_stack": "frontend: React, backend: FastAPI",
        "file_count": 15,
        "created_at": "2025-11-08T10:30:00Z"
      }
    }
  ],
  "count": 1
}
```

### Store Code Snippet
```bash
POST /pinecone/snippets/store
```

Request:
```json
{
  "snippet_id": "react-custom-hook",
  "code": "function useLocalStorage(key, initialValue) { ... }",
  "language": "javascript",
  "description": "Custom React hook for localStorage",
  "tags": ["react", "hooks", "storage"],
  "metadata": {
    "author": "user123",
    "version": "1.0"
  }
}
```

### Search Code Snippets
```bash
POST /pinecone/snippets/search
```

Request:
```json
{
  "query": "custom hook for localStorage",
  "language": "javascript",
  "tags": ["react"],
  "top_k": 10
}
```

### Get Index Statistics
```bash
GET /pinecone/stats
```

Response:
```json
{
  "total_vectors": 250,
  "dimension": 384,
  "index_fullness": 0.05,
  "namespaces": {
    "code_generations": {
      "vector_count": 150
    },
    "code_snippets": {
      "vector_count": 100
    }
  }
}
```

### Delete Vector
```bash
DELETE /pinecone/vectors/{vector_id}?namespace=code_generations
```

### Clear Namespace
```bash
DELETE /pinecone/namespace/{namespace}
```

⚠️ **USE WITH CAUTION** - This deletes all vectors in the namespace!

### Get Embedding Model Info
```bash
GET /embedding/info
```

Response:
```json
{
  "model_name": "all-MiniLM-L6-v2",
  "device": "cpu",
  "dimension": 384,
  "max_seq_length": 256,
  "batch_size": 32
}
```

## Architecture

### Components

1. **EmbeddingService** (`services/embedding_service.py`)
   - Converts text to vector embeddings
   - Uses sentence-transformers models
   - Supports batch processing
   - GPU acceleration when available

2. **PineconeService** (`services/pinecone_service.py`)
   - Manages Pinecone connections
   - Handles vector upsert/query operations
   - Automatic index creation
   - Namespace management

3. **Namespaces**
   - `code_generations` - Auto-stored project generations
   - `code_snippets` - User-stored reusable snippets

### Vector Storage

Each code generation stores:
```python
{
  "id": "gen_abc123",
  "vector": [0.123, -0.456, ...],  # 384 dimensions
  "metadata": {
    "generation_id": "gen_abc123",
    "project_name": "my-app",
    "description": "Full description",
    "tech_stack": "frontend: React, backend: FastAPI",
    "file_count": 12,
    "created_at": "2025-11-08T10:30:00Z"
  }
}
```

## Embedding Model

**Default Model**: `all-MiniLM-L6-v2`

Characteristics:
- **Dimension**: 384
- **Speed**: Very fast
- **Quality**: High quality for semantic search
- **Size**: ~90MB download on first use
- **Multilingual**: English optimized

### Alternative Models

You can change the model in `.env`:

```bash
# Larger, more accurate
EMBEDDING_MODEL_NAME=all-mpnet-base-v2
PINECONE_DIMENSION=768

# Multilingual
EMBEDDING_MODEL_NAME=paraphrase-multilingual-MiniLM-L12-v2
PINECONE_DIMENSION=384

# Fastest (lower quality)
EMBEDDING_MODEL_NAME=all-MiniLM-L12-v2
PINECONE_DIMENSION=384
```

⚠️ **Important**: Changing the model requires recreating the Pinecone index with the new dimension!

## Use Cases

### 1. Find Similar Projects
Before starting a new project, search for similar past generations:

```bash
POST /pinecone/search/projects
{
  "query": "todo app with user authentication and real-time updates",
  "top_k": 3
}
```

### 2. Build Code Snippet Library
Store commonly used patterns:

```bash
# Store authentication middleware
POST /pinecone/snippets/store
{
  "snippet_id": "fastapi-auth",
  "code": "async def verify_token(token: str): ...",
  "language": "python",
  "description": "FastAPI JWT authentication",
  "tags": ["fastapi", "auth", "jwt"]
}

# Search when needed
POST /pinecone/snippets/search
{
  "query": "authentication for FastAPI",
  "language": "python"
}
```

### 3. Technology Stack Filtering
Find projects using specific technologies:

```bash
POST /pinecone/search/projects
{
  "query": "dashboard application",
  "tech_stack_filter": {
    "frontend": "React",
    "backend": "FastAPI"
  }
}
```

## Performance

### Embedding Generation
- Single text: ~50ms (CPU) / ~10ms (GPU)
- Batch (32 texts): ~200ms (CPU) / ~30ms (GPU)

### Pinecone Queries
- Search latency: ~50-100ms
- Throughput: 10,000+ queries/second

### Index Size
- 384-dimensional vectors: ~1.5KB per vector
- 10,000 vectors ≈ 15MB storage

## Best Practices

1. **Descriptive IDs**: Use meaningful IDs for snippets
   ```python
   "snippet_id": "react-custom-hook-localstorage"  # Good
   "snippet_id": "snippet1"  # Bad
   ```

2. **Good Descriptions**: Write clear descriptions for better search
   ```python
   "description": "Custom React hook for localStorage with SSR support"  # Good
   "description": "hook"  # Bad
   ```

3. **Tag Consistently**: Use consistent tagging scheme
   ```python
   "tags": ["react", "hooks", "storage", "ssr"]  # Good
   "tags": ["React Hooks", "localstorage"]  # Inconsistent
   ```

4. **Monitor Usage**: Check index stats regularly
   ```bash
   GET /pinecone/stats
   ```

5. **Clean Old Data**: Periodically remove obsolete entries
   ```bash
   DELETE /pinecone/vectors/{old_generation_id}
   ```

## Troubleshooting

### Issue: "Pinecone not configured"
**Solution**: Add `PINECONE_API_KEY` to `.env` file

### Issue: Model download fails
**Solution**: Check internet connection, PyTorch needs ~90MB on first run

### Issue: CUDA out of memory
**Solution**: Model will automatically fall back to CPU

### Issue: "Index already exists" error
**Solution**: This is normal - the service reuses existing indexes

### Issue: No search results
**Solution**: 
- Ensure vectors are stored first
- Check namespace is correct
- Try broader search queries

## Security Considerations

1. **API Keys**: Keep Pinecone API key secret
2. **Input Validation**: All inputs are sanitized
3. **Namespace Isolation**: Use separate namespaces for different data types
4. **Rate Limiting**: Consider adding rate limits for production

## Future Enhancements

Planned features:
- [ ] Automatic code similarity detection
- [ ] Smart code suggestions during generation
- [ ] Project template recommendations
- [ ] Code quality scoring
- [ ] Multi-modal search (code + images)

## Support

For issues or questions:
1. Check server logs: `r-net-backend/logs/app.log`
2. Review Pinecone dashboard for index status
3. Test embedding model: `GET /embedding/info`
4. Check health: `GET /health`

## References

- [Pinecone Documentation](https://docs.pinecone.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Version**: 1.0.0  
**Last Updated**: November 8, 2025  
**Requires**: Python 3.8+, Pinecone account
