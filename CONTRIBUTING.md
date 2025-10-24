# Contributing to R-Net AI

Thank you for your interest in contributing to R-Net AI! This document provides guidelines and instructions for contributing to this project.

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ for backend development
- Node.js 16+ for extension development  
- VS Code for testing the extension
- Git for version control

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/R-Net-AI.git
   cd R-Net-AI
   ```

2. **Backend Setup**
   ```bash
   cd r-net-backend
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

3. **Extension Setup**
   ```bash
   cd r-net-extension
   npm install
   npm run compile
   ```

4. **Run Tests**
   ```bash
   # Backend tests
   cd r-net-backend
   ./test.sh

   # Extension tests
   cd r-net-extension
   npm test
   ```

## 📋 How to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please:
1. Check the existing issues to avoid duplicates
2. Use the latest version of the software
3. Provide detailed reproduction steps

**Bug Report Template:**
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g. macOS 14.0]
- VS Code Version: [e.g. 1.85.0]
- Extension Version: [e.g. 1.0.0]
- Python Version: [e.g. 3.11.0]

**Additional Context**
Any other relevant information
```

### 💡 Suggesting Features

Feature requests are welcome! Please:
1. Check existing feature requests first
2. Clearly describe the use case
3. Explain why this feature would be valuable
4. Consider implementation complexity

**Feature Request Template:**
```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Any alternative approaches?

**Additional Context**
Mockups, examples, etc.
```

### 🔧 Code Contributions

1. **Choose an Issue**
   - Look for issues labeled `good first issue` for beginners
   - Comment on the issue to let others know you're working on it

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make Changes**
   - Follow the coding standards (see below)
   - Write tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   # Run all tests
   cd r-net-backend && ./test.sh
   cd r-net-extension && npm test
   
   # Test the extension manually
   # Open r-net-extension in VS Code and press F5
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Use the PR template
   - Link related issues
   - Provide clear description of changes

## 📝 Coding Standards

### Python (Backend)

**Code Style:**
```python
# Use Black for formatting
black .

# Use type hints
def process_image(image_data: str) -> dict:
    """Process base64 image data and return metadata."""
    pass

# Use docstrings for functions and classes
class CodeGenerator:
    """Handles AI-powered code generation."""
    
    def generate(self, prompt: str) -> str:
        """Generate code from natural language prompt.
        
        Args:
            prompt: Natural language description
            
        Returns:
            Generated code as string
        """
        pass
```

**Testing:**
```python
# Use pytest for testing
import pytest
from unittest.mock import Mock, patch

class TestCodeGenerator:
    def test_generate_valid_input(self):
        """Test code generation with valid input."""
        # Arrange
        generator = CodeGenerator()
        prompt = "Create a REST API"
        
        # Act
        result = generator.generate(prompt)
        
        # Assert
        assert result is not None
        assert "def" in result
```

### TypeScript (Extension)

**Code Style:**
```typescript
// Use proper typing
interface GenerationRequest {
    imageData: string;
    description: string;
    techStack: TechStack;
}

// Use async/await for promises
async function generateCode(request: GenerationRequest): Promise<GenerationResponse> {
    try {
        const response = await apiService.generate(request);
        return response;
    } catch (error) {
        await ErrorHandler.handleError(error, 'Code Generation');
        throw error;
    }
}

// Use JSDoc for documentation
/**
 * Validates user input before sending to API
 * @param request - The generation request to validate
 * @returns True if valid, throws error otherwise
 */
function validateRequest(request: GenerationRequest): boolean {
    // Implementation
}
```

**Testing:**
```typescript
import * as assert from 'assert';
import * as sinon from 'sinon';

suite('ConfigurationService', () => {
    test('should return default configuration', () => {
        const config = ConfigurationService.getConfiguration();
        assert.strictEqual(config.backend.url, 'http://127.0.0.1:8000');
    });
});
```

## 🧪 Testing Guidelines

### Backend Testing
- Write unit tests for all functions
- Use integration tests for API endpoints
- Mock external dependencies (OpenAI API)
- Aim for 80%+ code coverage

### Extension Testing
- Test configuration management
- Test API communication
- Test error handling scenarios
- Test user input validation

### Test Organization
```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
└── fixtures/      # Test data and mocks
```

## 📚 Documentation

### Code Documentation
- Use docstrings/JSDoc for all public functions
- Include parameter descriptions and return types
- Provide usage examples for complex functions

### User Documentation
- Update README.md for new features
- Add examples to the examples/ directory
- Update configuration documentation

### API Documentation
- FastAPI automatically generates OpenAPI docs
- Ensure all endpoints have proper descriptions
- Include example requests/responses

## 🔄 Pull Request Process

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages follow convention

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
```

### Review Process
1. Automated checks must pass (tests, linting)
2. At least one maintainer review required
3. Address review feedback
4. Squash commits before merge

## 🏷️ Commit Message Convention

Use conventional commits:
```
feat: add new code generation template
fix: resolve image upload validation issue
docs: update API documentation
test: add unit tests for error handler
refactor: improve code organization
style: fix formatting issues
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🚀 Release Process

### Version Numbers
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Release Checklist
1. Update version numbers
2. Update CHANGELOG.md
3. Test thoroughly
4. Create release tag
5. Build and publish extension
6. Update documentation

## 💬 Communication

### Questions
- GitHub Discussions for general questions
- GitHub Issues for bug reports and feature requests
- Email maintainers for sensitive issues

### Response Times
- We aim to respond to issues within 48 hours
- PRs are typically reviewed within a week
- Emergency fixes get priority attention

## 🎯 Areas for Contribution

### High Priority
- [ ] Additional tech stack templates
- [ ] Improved error messages
- [ ] Performance optimizations
- [ ] UI/UX improvements

### Medium Priority
- [ ] Additional file format support
- [ ] Configuration presets
- [ ] Integration with other AI models
- [ ] Internationalization

### Documentation
- [ ] Video tutorials
- [ ] More usage examples
- [ ] API reference improvements
- [ ] Troubleshooting guides

## 🙏 Recognition

Contributors will be:
- Added to the CONTRIBUTORS.md file
- Mentioned in release notes
- Given appropriate GitHub repository permissions

Thank you for contributing to R-Net AI! 🚀