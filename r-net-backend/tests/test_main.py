import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
import base64
import io
from PIL import Image
import openai

from main import app
from models import CodeGenerationRequest, TechStack, TechStackOptions
from services.openai_service import openai_service


class TestAPI:
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture
    def sample_image_data(self):
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode()
    
    @pytest.fixture
    def sample_request_data(self, sample_image_data):
        return {
            "image_data": sample_image_data,
            "description": "A simple task management application with CRUD operations",
            "tech_stack": {
                "frontend": "React",
                "backend": "FastAPI",
                "database": "PostgreSQL"
            },
            "project_name": "test-app"
        }
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "openai_connected" in data
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_generate_endpoint_missing_api_key(self, client, sample_request_data):
        """Test generation endpoint without API key"""
        with patch('config.settings.openai_api_key', ''):
            response = client.post("/generate", json=sample_request_data)
            assert response.status_code == 503
    
    def test_generate_endpoint_invalid_request(self, client):
        """Test generation endpoint with invalid request"""
        invalid_data = {
            "description": "short",  # Too short
            "tech_stack": {
                "frontend": "React"
                # Missing backend and database
            }
        }
        response = client.post("/generate", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    @patch('services.openai_service.openai_service.generate_code')
    def test_generate_endpoint_success(self, mock_generate, client, sample_request_data):
        """Test successful code generation"""
        # Mock successful generation
        mock_generate.return_value = {
            "project_structure": {"src/": ["app.py", "models.py"]},
            "files": [
                {
                    "path": "src/app.py",
                    "content": "print('Hello World')",
                    "description": "Main application file"
                }
            ],
            "dependencies": {"backend": ["fastapi", "uvicorn"]},
            "setup_instructions": ["pip install -r requirements.txt"]
        }
        
        with patch('config.settings.openai_api_key', 'test-key'):
            response = client.post("/generate", json=sample_request_data)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert len(data["files"]) == 1
            assert "project_structure" in data
    
    @patch('services.openai_service.openai_service.generate_code')
    def test_generate_endpoint_api_error(self, mock_generate, client, sample_request_data):
        """Test generation endpoint with API error"""
        mock_generate.side_effect = ValueError("API Error")
        
        with patch('config.settings.openai_api_key', 'test-key'):
            response = client.post("/generate", json=sample_request_data)
            assert response.status_code == 200  # Returns 200 but with success=False
            data = response.json()
            assert data["success"] is False
            assert "error_details" in data


class TestOpenAIService:
    @pytest.fixture
    def service(self):
        return openai_service
    
    @pytest.fixture
    def tech_stack(self):
        return TechStack(
            frontend=TechStackOptions.REACT,
            backend=TechStackOptions.FASTAPI,
            database=TechStackOptions.POSTGRESQL
        )
    
    @pytest.fixture
    def sample_image_data(self):
        img = Image.new('RGB', (100, 100), color='blue')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode()
    
    @pytest.mark.asyncio
    async def test_test_connection_no_key(self, service):
        """Test connection test without API key"""
        with patch('config.settings.openai_api_key', ''):
            result = await service.test_connection()
            assert result is False
    
    def test_validate_and_process_image_valid(self, service, sample_image_data):
        """Test image validation with valid image"""
        result = service._validate_and_process_image(sample_image_data)
        assert result.startswith("data:image/png;base64,")
    
    def test_validate_and_process_image_invalid(self, service):
        """Test image validation with invalid data"""
        with pytest.raises(ValueError):
            service._validate_and_process_image("invalid_base64")
    
    def test_validate_and_process_image_too_large(self, service):
        """Test image validation with oversized image"""
        # Create a large image that exceeds the limit
        with patch('config.settings.max_file_size', 100):  # Very small limit
            img = Image.new('RGB', (1000, 1000), color='red')
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            large_image_data = base64.b64encode(buffer.getvalue()).decode()
            
            with pytest.raises(ValueError, match="Image size exceeds"):
                service._validate_and_process_image(large_image_data)
    
    @pytest.mark.asyncio
    async def test_generate_code_validation_errors(self, service, tech_stack):
        """Test code generation with validation errors"""
        
        # Test empty image data
        with pytest.raises(ValueError, match="Image data is required"):
            await service.generate_code("", "Valid description", tech_stack)
        
        # Test short description
        with pytest.raises(ValueError, match="at least 10 characters"):
            await service.generate_code("valid_image_data", "short", tech_stack)
    
    @pytest.mark.asyncio
    @patch('services.openai_service.OpenAI')
    async def test_generate_code_openai_errors(self, mock_openai_client, service, tech_stack, sample_image_data):
        """Test code generation with various OpenAI errors"""
        
        # Test authentication error
        mock_client = Mock()
        mock_openai_client.return_value = mock_client
        mock_client.chat.completions.create.side_effect = openai.AuthenticationError("Invalid API key")
        
        with pytest.raises(ValueError, match="authentication failed"):
            await service.generate_code(sample_image_data, "Valid description", tech_stack)
        
        # Test rate limit error
        mock_client.chat.completions.create.side_effect = openai.RateLimitError("Rate limit exceeded")
        
        with pytest.raises(ValueError, match="rate limit exceeded"):
            await service.generate_code(sample_image_data, "Valid description", tech_stack)
    
    def test_create_system_prompt(self, service, tech_stack):
        """Test system prompt creation"""
        prompt = service._create_system_prompt(tech_stack, "test-project")
        assert "test-project" in prompt
        assert "React" in prompt
        assert "FastAPI" in prompt
        assert "PostgreSQL" in prompt
        assert "JSON" in prompt
    
    def test_create_user_prompt(self, service, tech_stack):
        """Test user prompt creation"""
        description = "A task management app with user authentication"
        prompt = service._create_user_prompt(description, tech_stack)
        assert description in prompt
        assert "React" in prompt
        assert "FastAPI" in prompt
        assert "PostgreSQL" in prompt
    
    def test_parse_generated_content_valid_json(self, service, tech_stack):
        """Test parsing valid JSON response"""
        valid_json_response = '''```json
{
  "project_structure": {"src/": ["app.py"]},
  "files": [
    {
      "path": "src/app.py",
      "content": "print('hello')",
      "description": "Main app"
    }
  ],
  "dependencies": {"backend": ["fastapi"]},
  "setup_instructions": ["pip install fastapi"]
}
```'''
        
        result = service._parse_generated_content(valid_json_response, tech_stack, "test-project")
        assert "project_structure" in result
        assert len(result["files"]) == 1
        assert result["files"][0].path == "src/app.py"
    
    def test_parse_generated_content_invalid_json(self, service, tech_stack):
        """Test parsing invalid JSON response (should fallback)"""
        invalid_response = "This is not JSON at all"
        
        result = service._parse_generated_content(invalid_response, tech_stack, "test-project")
        assert "project_structure" in result
        assert len(result["files"]) == 1  # Fallback file
        assert result["files"][0].path == "README.md"
    
    def test_create_fallback_response(self, service, tech_stack):
        """Test fallback response creation"""
        raw_content = "Some raw AI response"
        result = service._create_fallback_response(tech_stack, "test-project", raw_content)
        
        assert "project_structure" in result
        assert len(result["files"]) == 1
        assert result["files"][0].path == "README.md"
        assert raw_content in result["files"][0].content


class TestModels:
    def test_tech_stack_model(self):
        """Test TechStack model validation"""
        # Valid tech stack
        stack = TechStack(
            frontend=TechStackOptions.REACT,
            backend=TechStackOptions.FASTAPI,
            database=TechStackOptions.POSTGRESQL
        )
        assert stack.frontend == TechStackOptions.REACT
        assert stack.backend == TechStackOptions.FASTAPI
        assert stack.database == TechStackOptions.POSTGRESQL
    
    def test_code_generation_request_validation(self):
        """Test CodeGenerationRequest validation"""
        # Valid request
        request = CodeGenerationRequest(
            image_data="base64_data_here",
            description="A comprehensive task management application",
            tech_stack=TechStack(
                frontend=TechStackOptions.REACT,
                backend=TechStackOptions.FASTAPI,
                database=TechStackOptions.POSTGRESQL
            )
        )
        assert request.project_name == "generated-app"  # Default value
        
        # Test with custom project name
        request_custom = CodeGenerationRequest(
            image_data="base64_data_here",
            description="A comprehensive task management application",
            tech_stack=TechStack(
                frontend=TechStackOptions.REACT,
                backend=TechStackOptions.FASTAPI,
                database=TechStackOptions.POSTGRESQL
            ),
            project_name="custom-project"
        )
        assert request_custom.project_name == "custom-project"
    
    def test_code_generation_request_validation_short_description(self):
        """Test CodeGenerationRequest with short description"""
        with pytest.raises(ValueError):
            CodeGenerationRequest(
                image_data="base64_data_here",
                description="short",  # Too short (< 10 chars)
                tech_stack=TechStack(
                    frontend=TechStackOptions.REACT,
                    backend=TechStackOptions.FASTAPI,
                    database=TechStackOptions.POSTGRESQL
                )
            )


# Test fixtures and utilities
@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = '''```json
{
  "project_structure": {"src/": ["app.py", "models.py"]},
  "files": [
    {
      "path": "src/app.py",
      "content": "from fastapi import FastAPI\\n\\napp = FastAPI()\\n\\n@app.get('/')\\ndef read_root():\\n    return {'Hello': 'World'}",
      "description": "FastAPI main application"
    },
    {
      "path": "src/models.py",
      "content": "from pydantic import BaseModel\\n\\nclass Item(BaseModel):\\n    name: str\\n    description: str",
      "description": "Pydantic models"
    }
  ],
  "dependencies": {"backend": ["fastapi", "uvicorn"]},
  "setup_instructions": ["pip install -r requirements.txt", "uvicorn src.app:app --reload"]
}
```'''
    return mock_response


# Integration tests
class TestIntegration:
    @pytest.mark.asyncio
    @patch('services.openai_service.OpenAI')
    async def test_full_generation_flow(self, mock_openai_client, mock_openai_response):
        """Test the complete generation flow"""
        # Setup mock
        mock_client = Mock()
        mock_openai_client.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_openai_response
        
        # Create sample data
        img = Image.new('RGB', (100, 100), color='green')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        image_data = base64.b64encode(buffer.getvalue()).decode()
        
        tech_stack = TechStack(
            frontend=TechStackOptions.REACT,
            backend=TechStackOptions.FASTAPI,
            database=TechStackOptions.POSTGRESQL
        )
        
        # Test generation
        with patch('config.settings.openai_api_key', 'test-key'):
            result = await openai_service.generate_code(
                image_data=image_data,
                description="A comprehensive task management application with user authentication",
                tech_stack=tech_stack,
                project_name="integration-test"
            )
        
        # Verify results
        assert "project_structure" in result
        assert len(result["files"]) == 2
        assert result["files"][0].path == "src/app.py"
        assert "FastAPI" in result["files"][0].content
        assert result["dependencies"]["backend"] == ["fastapi", "uvicorn"]