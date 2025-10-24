# AI Full-Stack Generator (GHC) - VS Code Extension

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/jonson42/R-Net-AI)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

Transform your UI mockups into production-ready full-stack applications using the power of AI. This VS Code extension leverages OpenAI's GPT-4 Vision to analyze your designs and generate complete application code.

## ✨ Features

### 🎨 **Visual Code Generation**
- Upload UI mockups, sketches, or wireframes
- AI analyzes visual elements and layout
- Generates corresponding frontend components

### 🛠️ **Multi-Technology Support**
- **Frontend**: React, Angular, Vue.js, HTML+Tailwind
- **Backend**: FastAPI, Flask, Express.js, ASP.NET Core  
- **Database**: PostgreSQL, MySQL, MongoDB, SQLite

### 🏗️ **Complete Project Generation**
- Full project structure with organized folders
- Production-ready code with no placeholders
- Comprehensive error handling and validation
- Responsive design implementation
- API documentation and basic tests

### ⚙️ **Seamless Integration**
- Native VS Code integration with intuitive UI
- Real-time progress tracking
- Configurable settings and preferences
- Smart error handling with actionable suggestions

## 🚀 Quick Start

### 1. Prerequisites
- **Backend Service**: Set up the R-Net AI backend service
- **OpenAI API Key**: Required for AI code generation

### 2. Installation
1. Install the extension from VS Code Marketplace
2. Configure the backend URL in settings (`Ctrl+,` → Search "R-Net AI")
3. Test the connection using Command Palette → `GHC: Test Backend Connection`

### 3. Usage
1. Open Command Palette (`Ctrl+Shift+P`)
2. Run `GHC: Open AI Full-Stack Generator`
3. Upload your UI mockup
4. Describe your requirements
5. Select technology stack
6. Generate your application!

## 📋 Commands

| Command | Description |
|---------|-------------|
| `GHC: Open AI Full-Stack Generator` | Open the main generator interface |
| `GHC: Configure Settings` | Configure extension settings |
| `GHC: Test Backend Connection` | Test connection to backend service |

## ⚙️ Extension Settings

This extension contributes the following settings:

* `rnet-ai.backend.url`: Backend service URL (default: `http://127.0.0.1:8000`)
* `rnet-ai.backend.timeout`: Request timeout in milliseconds (default: `60000`)
* `rnet-ai.generation.autoOpen`: Automatically open generated files (default: `true`)
* `rnet-ai.generation.createFolder`: Create project folder for generated files (default: `true`)
* `rnet-ai.ui.theme`: UI theme preference (default: `auto`)

## 🔧 Requirements

### Backend Service
The extension requires the R-Net AI backend service to be running:

```bash
# Start the backend service
cd r-net-backend
python main.py
```

### Dependencies
- VS Code 1.80.0 or later
- R-Net AI backend service
- OpenAI API key (configured in backend)

## 🎯 Usage Examples

### Task Management App
```
Upload: Mockup showing task list, add button, user profile
Description: "Create a task management app with user authentication, 
CRUD operations, categories, and real-time updates"
Tech Stack: React + FastAPI + PostgreSQL
```

### E-commerce Platform
```
Upload: Product grid, shopping cart, checkout form
Description: "Build an e-commerce platform with product catalog, 
shopping cart, payment integration, and admin panel"
Tech Stack: Angular + Express + MongoDB
```

## 🐛 Known Issues

- Large images (>5MB) may cause timeouts - compress before upload
- Complex UI designs may require additional refinement
- Generation time varies (15-45 seconds) based on complexity

## 🚀 Release Notes

### 1.0.0
- Initial release with full-stack code generation
- Support for multiple technology stacks
- Complete project structure generation
- Real-time progress tracking
- Comprehensive error handling

## 📚 Documentation

- [Main Documentation](https://github.com/jonson42/R-Net-AI/blob/main/README.md)
- [API Documentation](https://github.com/jonson42/R-Net-AI/blob/main/docs/API.md)
- [Examples](https://github.com/jonson42/R-Net-AI/blob/main/docs/EXAMPLES.md)
- [Deployment Guide](https://github.com/jonson42/R-Net-AI/blob/main/docs/DEPLOYMENT.md)

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](https://github.com/jonson42/R-Net-AI/blob/main/CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/jonson42/R-Net-AI/blob/main/LICENSE) file for details.

## 🙏 Support

- 🐛 [Report Issues](https://github.com/jonson42/R-Net-AI/issues)
- 💬 [Discussions](https://github.com/jonson42/R-Net-AI/discussions)
- 📖 [Documentation](https://github.com/jonson42/R-Net-AI/wiki)

---

**Enjoy building amazing applications with AI! 🚀**
