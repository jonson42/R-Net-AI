"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.apiService = exports.ApiService = void 0;
const vscode = __importStar(require("vscode"));
const axios_1 = __importDefault(require("axios"));
const configurationService_1 = require("./configurationService");
class ApiService {
    client;
    constructor() {
        this.updateClient();
    }
    /**
     * Update the HTTP client with current configuration
     */
    updateClient() {
        const config = configurationService_1.ConfigurationService.getConfiguration();
        this.client = axios_1.default.create({
            baseURL: config.backend.url,
            timeout: config.backend.timeout,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        // Add request interceptor for logging
        this.client.interceptors.request.use((config) => {
            const timestamp = new Date().toISOString();
            console.log(`[${timestamp}] API Request:`, {
                method: config.method?.toUpperCase(),
                url: `${config.baseURL}${config.url}`,
                headers: config.headers,
                dataSize: config.data ? JSON.stringify(config.data).length : 0
            });
            // Log to VS Code output if available
            if (typeof vscode !== 'undefined') {
                const outputChannel = vscode.window.createOutputChannel('R-Net AI API');
                outputChannel.appendLine(`[${timestamp}] === API REQUEST ===`);
                outputChannel.appendLine(`${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
                outputChannel.appendLine(`Data size: ${config.data ? JSON.stringify(config.data).length : 0} bytes`);
                outputChannel.show();
            }
            return config;
        }, (error) => {
            console.error('API Request Error:', error);
            return Promise.reject(error);
        });
        // Add response interceptor for logging
        this.client.interceptors.response.use((response) => {
            const timestamp = new Date().toISOString();
            console.log(`[${timestamp}] API Response:`, {
                status: response.status,
                statusText: response.statusText,
                dataSize: response.data ? JSON.stringify(response.data).length : 0,
                duration: response.config.metadata?.duration || 'unknown'
            });
            // Log to VS Code output if available
            if (typeof vscode !== 'undefined') {
                const outputChannel = vscode.window.createOutputChannel('R-Net AI API');
                outputChannel.appendLine(`[${timestamp}] === API RESPONSE ===`);
                outputChannel.appendLine(`Status: ${response.status} ${response.statusText}`);
                outputChannel.appendLine(`Response size: ${response.data ? JSON.stringify(response.data).length : 0} bytes`);
                if (response.data?.success !== undefined) {
                    outputChannel.appendLine(`Success: ${response.data.success}`);
                    if (response.data.files) {
                        outputChannel.appendLine(`Generated files: ${response.data.files.length}`);
                    }
                }
                outputChannel.show();
            }
            return response;
        }, (error) => {
            const timestamp = new Date().toISOString();
            console.error(`[${timestamp}] API Response Error:`, error);
            // Log to VS Code output if available
            if (typeof vscode !== 'undefined') {
                const outputChannel = vscode.window.createOutputChannel('R-Net AI API');
                outputChannel.appendLine(`[${timestamp}] === API ERROR ===`);
                outputChannel.appendLine(`Error: ${error.message}`);
                if (error.response) {
                    outputChannel.appendLine(`Status: ${error.response.status}`);
                    outputChannel.appendLine(`Data: ${JSON.stringify(error.response.data)}`);
                }
                outputChannel.show();
            }
            return Promise.reject(error);
        });
    }
    /**
     * Check backend service health
     */
    async checkHealth() {
        try {
            const response = await this.client.get('/health');
            return response.data;
        }
        catch (error) {
            throw this.handleError(error, 'Failed to check backend service health');
        }
    }
    /**
     * Generate code using the backend service
     */
    async generateCode(request) {
        try {
            console.log('=== STARTING CODE GENERATION ===');
            console.log('Request details:', {
                project_name: request.project_name,
                description_length: request.description.length,
                has_image: !!request.image_data,
                tech_stack: request.tech_stack
            });
            const startTime = Date.now();
            const response = await this.client.post('/generate', request);
            const duration = Date.now() - startTime;
            console.log(`=== CODE GENERATION COMPLETED (${duration}ms) ===`);
            console.log('Response summary:', {
                success: response.data.success,
                files_count: response.data.files?.length || 0,
                message: response.data.message
            });
            return response.data;
        }
        catch (error) {
            throw this.handleError(error, 'Code generation failed');
        }
    }
    /**
     * Test the backend connection
     */
    async testConnection() {
        try {
            console.log('=== TESTING BACKEND CONNECTION ===');
            const health = await this.checkHealth();
            console.log('Health check result:', health);
            const result = {
                success: health.status === 'healthy',
                error: health.status !== 'healthy' ? 'Backend service is not healthy' : undefined
            };
            console.log('Connection test result:', result);
            return result;
        }
        catch (error) {
            console.error('Connection test failed:', error);
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error'
            };
        }
    }
    /**
     * Handle API errors with user-friendly messages
     */
    handleError(error, defaultMessage) {
        if (axios_1.default.isAxiosError(error)) {
            const axiosError = error;
            // Handle different error scenarios
            if (axiosError.code === 'ECONNREFUSED') {
                return new Error('Backend service is not running. Please start the backend service first.');
            }
            if (axiosError.code === 'ENOTFOUND') {
                return new Error('Cannot connect to backend service. Please check the backend URL in settings.');
            }
            if (axiosError.response) {
                // Server responded with error status
                const status = axiosError.response.status;
                const data = axiosError.response.data;
                switch (status) {
                    case 400:
                        return new Error(data?.detail || 'Invalid request. Please check your input.');
                    case 401:
                        return new Error('Authentication failed. Please check your API key.');
                    case 403:
                        return new Error('Access denied. Please check your permissions.');
                    case 404:
                        return new Error('Backend service endpoint not found.');
                    case 429:
                        return new Error('Rate limit exceeded. Please try again later.');
                    case 500:
                        return new Error(data?.detail || 'Backend service error. Please try again.');
                    case 503:
                        return new Error('Backend service is temporarily unavailable.');
                    default:
                        return new Error(data?.detail || `Server error (${status})`);
                }
            }
            if (axiosError.request) {
                // Request was made but no response received
                return new Error('No response from backend service. Please check your connection.');
            }
        }
        // Generic error handling
        if (error instanceof Error) {
            return new Error(`${defaultMessage}: ${error.message}`);
        }
        return new Error(defaultMessage);
    }
    /**
     * Show user-friendly error messages
     */
    static showErrorMessage(error) {
        const message = error.message;
        // Show different types of notifications based on error
        if (message.includes('not running') || message.includes('ECONNREFUSED')) {
            vscode.window.showErrorMessage(message, 'Open Backend Setup Guide').then((selection) => {
                if (selection === 'Open Backend Setup Guide') {
                    vscode.env.openExternal(vscode.Uri.parse('https://github.com/jonson42/R-Net-AI#backend-setup'));
                }
            });
        }
        else if (message.includes('API key')) {
            vscode.window.showErrorMessage(message, 'Configure Settings').then((selection) => {
                if (selection === 'Configure Settings') {
                    vscode.commands.executeCommand('workbench.action.openSettings', 'rnet-ai');
                }
            });
        }
        else {
            vscode.window.showErrorMessage(message);
        }
    }
}
exports.ApiService = ApiService;
// Global service instance
exports.apiService = new ApiService();
//# sourceMappingURL=apiService.js.map