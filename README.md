# 🚀 R-Net AI - Full-Stack Code Generation Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![VS Code Extension](https://img.shields.io/badge/VS%20Code-Extension-blue.svg)](https://marketplace.visualstudio.com/vscode)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4%20Vision-orange.svg)](https://openai.com/)

R-Net AI is a revolutionary **AI-powered full-stack code generation platform** that transforms UI mockups and natural language descriptions into production-ready applications. Built as a VS Code extension with a FastAPI backend, it leverages OpenAI's GPT-4 Vision to understand visual designs and generate complete application code.

## 🌟 Key Features

### 🎨 **Multimodal Input Processing**
- Upload UI mockups, sketches, or wireframes (PNG, JPG, WebP)
- Provide detailed natural language requirements
- AI analyzes both visual and textual inputs simultaneously

### 🛠️ **Complete Tech Stack Support**
- **Frontend**: React, Angular, Vue.js, HTML+Tailwind
- **Backend**: FastAPI, Flask, Express.js, ASP.NET Core
- **Database**: PostgreSQL, MySQL, MongoDB, SQLite

### 🏗️ **Production-Ready Code Generation**
- Full project structure with organized folders
- Complete application files with no placeholders
- Proper error handling and validation
- Responsive design implementation
- API documentation and tests

### � **Seamless VS Code Integration**
- Native extension with intuitive UI
- Configurable settings and preferences
- Real-time status updates and progress tracking
- Integrated error handling and suggestions

### 🔒 **Enterprise-Ready Features**
- Comprehensive error handling and logging
- Configurable API endpoints and timeouts
- Secure API key management
- Extensive testing framework

---

## 🚀 Quick Start

### Prerequisites

- **VS Code** 1.80.0 or later
- **Python** 3.10+ (for backend)
- **Node.js** 16+ (for extension development)
- **OpenAI API Key** ([Get yours here](https://platform.openai.com/api-keys))

### 1. Backend Setup

```bash
# Navigate to backend directory
cd r-net-backend

# Run the setup script (creates venv, installs dependencies)
./start.sh

# Or manual setup:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key

# Start the service
python main.py
```

### 2. VS Code Extension Setup

```bash
# Navigate to extension directory
cd r-net-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Open in VS Code and press F5 to launch extension development host
```

### 3. Configure the Extension

1. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Run `GHC: Configure Settings`
3. Set backend URL (default: `http://127.0.0.1:8000`)
4. Test connection with `GHC: Test Backend Connection`

---

## 📖 Usage Guide

### Step 1: Open the Generator
- Command Palette → `GHC: Open AI Full-Stack Generator`
- Or use the command `ghc.openGeneratorPanel`

### Step 2: Upload Your Design
- Drag & drop or click to upload your UI mockup
- Supported formats: PNG, JPG, WebP (max 5MB)
- The AI will analyze the visual design elements

### Step 3: Describe Your Requirements
```
Example prompt:
"This is a task management application with the following features:
- User authentication with login/register
- Dashboard showing task statistics
- CRUD operations for tasks with categories
- Real-time updates using WebSockets
- Search and filtering capabilities
- Responsive design for mobile and desktop
- RESTful API with proper error handling
- Database schema with relationships
- Unit tests for critical functions"
```

### Step 4: Select Technology Stack
- **Frontend**: Choose your preferred framework
- **Backend**: Select API framework
- **Database**: Pick your database solution

### Step 5: Generate Code
- Click "Generate Full-Stack Code"
- Wait 15-45 seconds for AI processing
- Review generated files in your workspace

---

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   VS Code       │    │   FastAPI       │    │   OpenAI        │
│   Extension     │◄──►│   Backend       │◄──►│   GPT-4 Vision  │
│                 │    │                 │    │                 │
│ • UI/UX         │    │ • Image Proc.   │    │ • Code Gen.     │
│ • Config Mgmt   │    │ • API Routes    │    │ • Vision API    │
│ • File Ops      │    │ • Error Handle  │    │ • Chat API      │
│ • Error Handle  │    │ • Validation    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Extension Components
- **ConfigurationService**: Manages settings and preferences
- **ApiService**: Handles HTTP communication with backend
- **ErrorHandler**: Comprehensive error management
- **WebView**: Modern UI with real-time updates

### Backend Components
- **FastAPI Application**: RESTful API with async support
- **OpenAI Service**: Image processing and code generation
- **Configuration Management**: Environment-based settings
- **Comprehensive Testing**: Unit and integration tests

---

## 🛡️ Error Handling & Troubleshooting

### Common Issues

#### Backend Connection Failed
```bash
# Check if backend is running
curl http://127.0.0.1:8000/health

# Restart backend service
cd r-net-backend
./start.sh
```

#### OpenAI API Issues
- Verify API key in `.env` file
- Check API usage limits and billing
- Ensure you have access to GPT-4 Vision

#### File Generation Issues
- Ensure workspace folder is open in VS Code
- Check file permissions in workspace
- Verify sufficient disk space

### Debug Mode
Enable detailed logging:
```bash
# Backend
LOG_LEVEL=DEBUG python main.py

# Extension
# Open VS Code Developer Tools (Help → Toggle Developer Tools)
```

---

## 🧪 Testing

### Backend Tests
```bash
cd r-net-backend
./test.sh
# or manually:
pytest tests/ -v --cov=. --cov-report=html
```

### Extension Tests
```bash
cd r-net-extension
npm test
```

---

## ⚙️ Configuration

### Backend Configuration (`.env`)
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4-vision-preview

# Server Settings
HOST=127.0.0.1
PORT=8000
DEBUG=True

# File Upload Limits
MAX_FILE_SIZE=5242880  # 5MB
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,webp
```

### Extension Settings
Access via VS Code Settings (`Ctrl+,`) → Search "R-Net AI"

- `rnet-ai.backend.url`: Backend service URL
- `rnet-ai.backend.timeout`: Request timeout (ms)
- `rnet-ai.generation.autoOpen`: Auto-open generated files
- `rnet-ai.generation.createFolder`: Create project folder
- `rnet-ai.ui.theme`: UI theme preference

---

## 📝 Examples

### Generated Project Structure
```
my-task-app/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   ├── public/
│   └── package.json
├── backend/
│   ├── src/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
├── database/
│   ├── migrations/
│   └── schema.sql
└── README.md
```

### Sample Generated Code Quality
- ✅ Complete functional components
- ✅ Proper TypeScript/Python typing
- ✅ Error handling and validation
- ✅ Responsive design patterns
- ✅ API documentation
- ✅ Basic unit tests

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Standards
- **Python**: Black formatting, type hints, docstrings
- **TypeScript**: ESLint rules, proper typing
- **Testing**: Minimum 80% coverage
- **Documentation**: Update relevant docs

---

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT-4 Vision API
- **VS Code Extension API** for the robust extension framework
- **FastAPI** for the high-performance backend framework
- **The Open Source Community** for continuous inspiration

---

## 📞 Support

- 📧 **Email**: support@r-net-ai.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/jonson42/R-Net-AI/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/jonson42/R-Net-AI/discussions)
- 📖 **Documentation**: [Wiki](https://github.com/jonson42/R-Net-AI/wiki)

---

<div align="center">

**⭐ Star this repo if R-Net AI helps you build faster! ⭐**

</div>

