# Deployment Guide for R-Net AI

This guide covers different deployment scenarios for the R-Net AI platform.

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [VS Code Extension Publishing](#vs-code-extension-publishing)

## Local Development

### Backend Setup
```bash
cd r-net-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env file with your OpenAI API key

# Start development server
python main.py
```

### Extension Development
```bash
cd r-net-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Open in VS Code and press F5 for development host
```

## Docker Deployment

### Single Container (Backend Only)
```bash
# Build the backend image
cd r-net-backend
docker build -t rnet-ai-backend .

# Run the container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key_here \
  -v $(pwd)/logs:/app/logs \
  rnet-ai-backend
```

### Full Stack with Docker Compose
```bash
# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Docker Compose
```yaml
version: '3.8'
services:
  backend:
    image: ghcr.io/jonson42/r-net-ai/backend:latest
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEBUG=False
      - LOG_LEVEL=WARNING
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
    restart: unless-stopped
```

## Cloud Deployment

### AWS Deployment

#### Using AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_URI
docker build -t rnet-ai-backend .
docker tag rnet-ai-backend:latest YOUR_ECR_URI/rnet-ai-backend:latest
docker push YOUR_ECR_URI/rnet-ai-backend:latest

# Deploy using ECS CLI or AWS Console
```

#### Using AWS Lambda (Serverless)
```bash
# Install serverless framework
npm install -g serverless

# Deploy backend as Lambda function
serverless deploy --stage production
```

### Google Cloud Platform

#### Using Cloud Run
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/rnet-ai-backend

# Deploy to Cloud Run
gcloud run deploy rnet-ai-backend \
  --image gcr.io/PROJECT_ID/rnet-ai-backend \
  --port 8000 \
  --set-env-vars OPENAI_API_KEY=your_key_here \
  --allow-unauthenticated
```

### Microsoft Azure

#### Using Container Instances
```bash
# Create resource group
az group create --name rnet-ai-rg --location eastus

# Deploy container
az container create \
  --resource-group rnet-ai-rg \
  --name rnet-ai-backend \
  --image ghcr.io/jonson42/r-net-ai/backend:latest \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=your_key_here \
  --restart-policy Always
```

### Heroku Deployment
```bash
# Install Heroku CLI and login
heroku login

# Create application
heroku create rnet-ai-backend

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key_here

# Deploy
git push heroku main
```

## VS Code Extension Publishing

### Prepare for Publishing
```bash
cd r-net-extension

# Install vsce (Visual Studio Code Extension manager)
npm install -g @vscode/vsce

# Update package.json with proper metadata
# - Update version number
# - Add publisher name
# - Add repository, homepage URLs
# - Add proper description and keywords

# Build extension package
npm run package
```

### Publish to Marketplace
```bash
# Login to Visual Studio Marketplace
vsce login YOUR_PUBLISHER_NAME

# Publish extension
vsce publish

# Or publish specific version
vsce publish 1.0.0

# Publish pre-release version
vsce publish --pre-release
```

### Alternative: Manual Upload
1. Build extension package: `vsce package`
2. Go to [Visual Studio Marketplace](https://marketplace.visualstudio.com/manage)
3. Upload the `.vsix` file manually

## Environment Configuration

### Production Environment Variables
```bash
# Backend Configuration
OPENAI_API_KEY=your_production_api_key
OPENAI_API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4-vision-preview
DEBUG=False
LOG_LEVEL=WARNING

# Security
SECRET_KEY=your-strong-secret-key
CORS_ORIGINS=https://your-domain.com

# Performance
MAX_TOKENS=4096
TEMPERATURE=0.7
MAX_FILE_SIZE=5242880

# Monitoring
SENTRY_DSN=your_sentry_dsn_for_error_tracking
LOG_FILE=/var/log/rnet-ai/app.log
```

### Nginx Configuration
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        client_max_body_size 10M;

        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        location /health {
            proxy_pass http://backend/health;
            access_log off;
        }
    }
}
```

## SSL/TLS Configuration

### Using Let's Encrypt with Certbot
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Manual SSL Certificate
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # ... rest of configuration
}
```

## Monitoring and Logging

### Health Checks
```bash
# Backend health check
curl http://localhost:8000/health

# Docker container health check
docker ps  # Shows health status

# Kubernetes health check
kubectl get pods -l app=rnet-ai-backend
```

### Log Management
```bash
# View application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f backend

# Structured logging with ELK Stack
# Configure Elasticsearch, Logstash, and Kibana for log aggregation
```

### Performance Monitoring
```bash
# Install monitoring tools
pip install prometheus-client
pip install grafana-api

# Configure metrics endpoint
# Add /metrics endpoint to FastAPI app
```

## Scaling and Performance

### Horizontal Scaling
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rnet-ai-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rnet-ai-backend
  template:
    metadata:
      labels:
        app: rnet-ai-backend
    spec:
      containers:
      - name: backend
        image: ghcr.io/jonson42/r-net-ai/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: rnet-ai-secrets
              key: openai-api-key
```

### Load Balancing
```bash
# Using HAProxy
backend rnet-ai-backend
    balance roundrobin
    server backend1 backend1:8000 check
    server backend2 backend2:8000 check
    server backend3 backend3:8000 check
```

## Backup and Recovery

### Database Backup (if using PostgreSQL)
```bash
# Backup database
pg_dump -h localhost -U rnetai rnetai > backup.sql

# Restore database
psql -h localhost -U rnetai rnetai < backup.sql
```

### File Backup
```bash
# Backup uploads and logs
tar -czf backup-$(date +%Y%m%d).tar.gz logs/ uploads/

# Restore
tar -xzf backup-20241224.tar.gz
```

## Troubleshooting

### Common Issues

#### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Common fixes:
# 1. Check OpenAI API key
# 2. Check port availability
# 3. Check file permissions
```

#### Extension not connecting
```bash
# Check backend URL in VS Code settings
# Test backend connection manually
curl http://localhost:8000/health
```

#### Memory issues
```bash
# Monitor memory usage
docker stats

# Increase memory limits in docker-compose.yml
```

## Security Considerations

### API Security
- Use HTTPS in production
- Implement rate limiting
- Validate all inputs
- Keep dependencies updated
- Use secrets management for API keys

### Container Security
- Use non-root user in containers
- Scan images for vulnerabilities
- Keep base images updated
- Use minimal base images

### Network Security
- Configure firewalls properly
- Use VPC/private networks
- Implement WAF for web traffic

For more deployment options and detailed configurations, see the [Wiki](https://github.com/jonson42/R-Net-AI/wiki/Deployment).