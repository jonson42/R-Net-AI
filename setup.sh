#!/bin/bash

# R-Net AI Development Setup Script
# This script sets up the complete development environment

set -e

echo "🚀 R-Net AI Development Setup"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed."
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is required but not installed."
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is required but not installed."
        exit 1
    fi
    
    # Check Docker (optional)
    if ! command -v docker &> /dev/null; then
        print_warning "Docker is not installed. Some features may not be available."
    fi
    
    print_success "Prerequisites check completed"
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd r-net-backend
    
    # Create virtual environment
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Setup environment file
    if [ ! -f .env ]; then
        print_status "Creating .env file..."
        cp .env.example .env
        print_warning "Please edit r-net-backend/.env and add your OpenAI API key"
    fi
    
    # Create necessary directories
    mkdir -p logs uploads
    
    print_success "Backend setup completed"
    
    cd ..
}

# Setup extension
setup_extension() {
    print_status "Setting up VS Code extension..."
    
    cd r-net-extension
    
    # Install npm dependencies
    print_status "Installing npm dependencies..."
    npm install
    
    # Compile TypeScript
    print_status "Compiling TypeScript..."
    npm run compile
    
    print_success "Extension setup completed"
    
    cd ..
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    # Backend tests
    print_status "Running backend tests..."
    cd r-net-backend
    source venv/bin/activate
    python -m pytest tests/ -v --tb=short || print_warning "Some backend tests failed"
    cd ..
    
    # Extension tests
    print_status "Running extension tests..."
    cd r-net-extension
    npm test || print_warning "Some extension tests failed"
    cd ..
    
    print_success "Tests completed"
}

# Start services
start_services() {
    print_status "Starting services..."
    
    # Start backend
    print_status "Starting backend service..."
    cd r-net-backend
    source venv/bin/activate
    python main.py &
    BACKEND_PID=$!
    print_success "Backend started (PID: $BACKEND_PID)"
    cd ..
    
    # Wait a moment for backend to start
    sleep 3
    
    # Test backend health
    if curl -f http://127.0.0.1:8000/health > /dev/null 2>&1; then
        print_success "Backend is healthy and responding"
    else
        print_warning "Backend may not be fully ready yet"
    fi
    
    print_status "Backend service is running at http://127.0.0.1:8000"
    print_status "API documentation available at http://127.0.0.1:8000/docs"
    print_success "Setup completed! You can now open VS Code and run the extension."
}

# Docker setup (optional)
setup_docker() {
    if command -v docker &> /dev/null; then
        print_status "Setting up Docker environment..."
        
        # Copy environment file for Docker
        if [ ! -f .env ]; then
            cp .env.example .env
            print_warning "Please edit .env and add your OpenAI API key for Docker setup"
        fi
        
        # Build and start services
        print_status "Building Docker images..."
        docker-compose build
        
        print_status "Starting services with Docker..."
        docker-compose up -d
        
        print_success "Docker setup completed"
        print_status "Services available at:"
        print_status "  - Backend: http://localhost:8000"
        print_status "  - API Docs: http://localhost:8000/docs"
    fi
}

# Main execution
main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --docker)
                USE_DOCKER=true
                shift
                ;;
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --no-start)
                NO_START=true
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [OPTIONS]"
                echo "Options:"
                echo "  --docker      Use Docker for setup"
                echo "  --skip-tests  Skip running tests"
                echo "  --no-start    Don't start services after setup"
                echo "  -h, --help    Show this help message"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Run setup steps
    check_prerequisites
    
    if [ "$USE_DOCKER" = true ]; then
        setup_docker
    else
        setup_backend
        setup_extension
        
        if [ "$SKIP_TESTS" != true ]; then
            run_tests
        fi
        
        if [ "$NO_START" != true ]; then
            start_services
        fi
    fi
    
    echo ""
    echo "🎉 R-Net AI development environment is ready!"
    echo ""
    echo "Next steps:"
    echo "1. Edit r-net-backend/.env and add your OpenAI API key"
    echo "2. Open VS Code in this directory"
    echo "3. Install the R-Net AI extension (F5 for dev mode)"
    echo "4. Use Command Palette -> 'GHC: Open AI Full-Stack Generator'"
    echo ""
    echo "Documentation:"
    echo "- README.md - Main documentation"
    echo "- docs/API.md - API documentation"
    echo "- docs/DEPLOYMENT.md - Deployment guide"
    echo "- docs/EXAMPLES.md - Usage examples"
    echo ""
}

# Run main function
main "$@"