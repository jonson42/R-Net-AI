# VS Code Extension Debug Issues - Troubleshooting Guide

## Common Issues Why Extension Doesn't Call Backend in Debug Mode

### 1. **Backend Not Running**
- The most common issue is that the backend service isn't running
- Check if backend is running: `lsof -i :8000`
- Start backend: `cd r-net-backend && python3 main.py`

### 2. **Extension Not Properly Compiled**
- Extension needs to be compiled before debugging
- Run: `npm run compile` in the extension directory
- Check that `dist/extension.js` exists and is recent

### 3. **Configuration Issues**
- Default backend URL: `http://127.0.0.1:8000`
- Check VS Code settings: `rnet-ai.backend.url`
- Verify timeout settings: `rnet-ai.backend.timeout`

### 4. **Debug Launch Configuration**
Your launch.json should point to the compiled files:
```json
{
  "outFiles": ["${workspaceFolder}/dist/**/*.js"]
}
```

### 5. **Network/CORS Issues**
- Backend allows all origins by default: `allow_origins=["*"]`
- Check if localhost/127.0.0.1 resolution works
- Try both `localhost:8000` and `127.0.0.1:8000`

## Debug Steps

### Step 1: Verify Backend
```bash
cd r-net-backend
python3 main.py
# In another terminal:
curl http://127.0.0.1:8000/health
```

### Step 2: Compile Extension
```bash
cd r-net-extension
npm run compile
```

### Step 3: Check Extension Logs
- Open VS Code Developer Tools: `Help > Toggle Developer Tools`
- Check Console for errors
- Look for network requests to backend

### Step 4: Test Extension Commands
- Open Command Palette: `Cmd+Shift+P`
- Run: `R-Net AI: Test Backend Connection`
- Run: `R-Net AI: Test API Call`

### Step 5: Debug Extension Code
- Set breakpoints in `src/services/apiService.ts`
- Check if requests are being made
- Verify configuration values

## Extension Commands for Testing
- `ghc.testConnection` - Test backend connection
- `ghc.testAPI` - Test full API call
- `ghc.configure` - Configure settings
- `ghc.openGeneratorPanel` - Open main UI

## Logs to Check
1. **Extension Output**: View > Output > R-Net AI
2. **Backend Logs**: Console where backend is running
3. **VS Code Console**: Help > Toggle Developer Tools

## Common Error Messages
- "ECONNREFUSED": Backend not running
- "ENOTFOUND": Wrong URL configuration
- "timeout": Backend is slow or overloaded
- "401/403": API key issues (OpenAI)