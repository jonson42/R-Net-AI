import base64
import io
import logging
import asyncio
from typing import Dict, List, Optional
from PIL import Image
import openai
from openai import OpenAI

from config import settings
from models import TechStack, GeneratedFile

logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base
        )
        
    async def test_connection(self) -> bool:
        """Test OpenAI API connection"""
        try:
            response = self.client.models.list()
            return bool(response.data)
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            return False
    
    def _validate_and_process_image(self, image_data: str) -> str:
        """Validate and process base64 image data"""
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            
            # Validate image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Check file size
            if len(image_bytes) > settings.max_file_size:
                raise ValueError(f"Image size exceeds {settings.max_file_size} bytes")
            
            # Convert to RGB if necessary
            if image.mode not in ['RGB', 'RGBA']:
                image = image.convert('RGB')
            
            # Resize if too large (max 2048x2048 for OpenAI)
            max_size = 2048
            if image.width > max_size or image.height > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Convert back to base64
                buffer = io.BytesIO()
                image.save(buffer, format='PNG')
                image_data = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{image_data}"
            
        except Exception as e:
            logger.error(f"Image processing failed: {e}")
            raise ValueError(f"Invalid image data: {e}")
    
    async def generate_code(
        self, 
        image_data: str, 
        description: str, 
        tech_stack: TechStack,
        project_name: str = "generated-app"
    ) -> Dict:
        """Generate full-stack code using OpenAI Vision API"""
        try:
            logger.info(f"Starting code generation for project: {project_name}")
            
            # Validate inputs
            if not image_data:
                raise ValueError("Image data is required")
            if not description or len(description.strip()) < 10:
                raise ValueError("Description must be at least 10 characters long")
            
            # Process image
            processed_image = self._validate_and_process_image(image_data)
            logger.info("Image processed successfully")
            
            # Create system prompt
            system_prompt = self._create_system_prompt(tech_stack, project_name)
            
            # Create user prompt
            user_prompt = self._create_user_prompt(description, tech_stack)
            
            logger.info("Sending request to OpenAI API")
            
            # Call OpenAI API with retry logic
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    response = self.client.chat.completions.create(
                        model=settings.model_name,
                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": user_prompt
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": processed_image
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=settings.max_tokens,
                        temperature=settings.temperature
                    )
                    break
                    
                except openai.RateLimitError as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        logger.error(f"Rate limit exceeded after {max_retries} retries")
                        raise ValueError("OpenAI API rate limit exceeded. Please try again later.")
                    
                    wait_time = 2 ** retry_count  # Exponential backoff
                    logger.warning(f"Rate limit hit, waiting {wait_time}s before retry {retry_count}/{max_retries}")
                    await asyncio.sleep(wait_time)
                    
                except openai.APIError as e:
                    logger.error(f"OpenAI API error: {e}")
                    raise ValueError(f"OpenAI API error: {str(e)}")
                    
                except Exception as e:
                    logger.error(f"Unexpected API error: {e}")
                    raise ValueError(f"Failed to generate code: {str(e)}")
            
            # Validate response
            if not response or not response.choices:
                raise ValueError("No response received from OpenAI API")
                
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from OpenAI API")
            
            logger.info("OpenAI API response received, parsing content")
            
            # Parse response
            result = self._parse_generated_content(content, tech_stack, project_name)
            
            logger.info(f"Code generation completed successfully - {len(result['files'])} files generated")
            return result
            
        except ValueError as e:
            # Re-raise validation errors as-is
            logger.error(f"Validation error: {e}")
            raise
            
        except openai.AuthenticationError as e:
            logger.error(f"OpenAI authentication failed: {e}")
            raise ValueError("OpenAI API authentication failed. Please check your API key.")
            
        except openai.PermissionDeniedError as e:
            logger.error(f"OpenAI permission denied: {e}")
            raise ValueError("OpenAI API access denied. Please check your API key permissions.")
            
        except Exception as e:
            logger.error(f"Code generation failed: {e}", exc_info=True)
            raise ValueError(f"Code generation failed: {str(e)}")
    
    def _create_system_prompt(self, tech_stack: TechStack, project_name: str) -> str:
        """Create system prompt for code generation"""
        return f"""You are an expert full-stack developer and architect. Your task is to analyze a UI mockup image and generate a complete, production-ready application based on the provided requirements.

**Project Details:**
- Project Name: {project_name}
- Frontend: {tech_stack.frontend.value}
- Backend: {tech_stack.backend.value}
- Database: {tech_stack.database.value}

**Your Response Format:**
Please structure your response as a JSON object with the following format:

```json
{{
  "project_structure": {{
    "frontend/": ["src/", "public/", "package.json"],
    "backend/": ["src/", "requirements.txt", "main.py"],
    "database/": ["schema.sql", "migrations/"]
  }},
  "files": [
    {{
      "path": "frontend/src/App.js",
      "content": "// Complete file content here",
      "description": "Main React application component"
    }}
  ],
  "dependencies": {{
    "frontend": ["react", "react-dom", "@mui/material"],
    "backend": ["fastapi", "sqlalchemy", "psycopg2"],
    "database": []
  }},
  "setup_instructions": [
    "1. Install Node.js and Python",
    "2. Run npm install in frontend/",
    "3. Install backend dependencies: pip install -r requirements.txt"
  ]
}}
```

**Requirements:**
1. Generate COMPLETE, functional code - no placeholders or TODOs
2. Include proper error handling and validation
3. Add authentication if the UI suggests user accounts
4. Include responsive design and modern UI patterns
5. Add proper database models and API endpoints
6. Include configuration files and environment setup
7. Add basic tests where appropriate
8. Follow best practices for the chosen tech stack"""

    def _create_user_prompt(self, description: str, tech_stack: TechStack) -> str:
        """Create user prompt for code generation"""
        return f"""Analyze the provided UI mockup image and generate a complete {tech_stack.frontend.value}/{tech_stack.backend.value}/{tech_stack.database.value} application.

**Requirements:**
{description}

**Technical Specifications:**
- Frontend: {tech_stack.frontend.value} with modern styling (Tailwind CSS or Material-UI)
- Backend: {tech_stack.backend.value} with RESTful API design
- Database: {tech_stack.database.value} with proper schema design
- Include authentication and authorization if the UI shows login/user features
- Add form validation and error handling
- Implement responsive design
- Include API documentation
- Add basic unit tests

Please analyze the UI mockup carefully and create a fully functional application that matches the design and fulfills all the requirements. Generate complete, production-ready code with no placeholders."""

    def _parse_generated_content(self, content: str, tech_stack: TechStack, project_name: str) -> Dict:
        """Parse the generated content from OpenAI response"""
        try:
            import json
            import re
            
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                json_content = json_match.group(1)
            else:
                # Try to find JSON without code blocks
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_content = json_match.group(0)
                else:
                    raise ValueError("No valid JSON found in response")
            
            # Parse JSON
            parsed_data = json.loads(json_content)
            
            # Validate and structure the response
            return {
                "project_structure": parsed_data.get("project_structure", {}),
                "files": [
                    GeneratedFile(**file_data) for file_data in parsed_data.get("files", [])
                ],
                "dependencies": parsed_data.get("dependencies", {}),
                "setup_instructions": parsed_data.get("setup_instructions", [])
            }
            
        except Exception as e:
            logger.error(f"Failed to parse generated content: {e}")
            # Return a basic fallback structure
            return self._create_fallback_response(tech_stack, project_name, content)
    
    def _create_fallback_response(self, tech_stack: TechStack, project_name: str, raw_content: str) -> Dict:
        """Create a fallback response when parsing fails"""
        return {
            "project_structure": {
                "frontend/": ["src/", "public/", "package.json"],
                "backend/": ["src/", "main.py", "requirements.txt"],
                "README.md": []
            },
            "files": [
                GeneratedFile(
                    path="README.md",
                    content=f"# {project_name}\n\nGenerated with R-Net AI\n\n**Tech Stack:**\n- Frontend: {tech_stack.frontend}\n- Backend: {tech_stack.backend}\n- Database: {tech_stack.database}\n\n**Raw AI Response:**\n{raw_content}",
                    description="Project README with AI response"
                )
            ],
            "dependencies": {
                "frontend": [],
                "backend": [],
                "database": []
            },
            "setup_instructions": [
                "1. Review the generated files",
                "2. Install dependencies for your tech stack",
                "3. Configure database connection",
                "4. Run the application"
            ]
        }


# Global service instance
openai_service = OpenAIService()