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
            // Log request for debugging
            return config;
        }, (error) => {
            return Promise.reject(error);
        });
        // Add response interceptor for logging
        this.client.interceptors.response.use((response) => {
            // Log response for debugging
            return response;
        }, (error) => {
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
            const response = await this.client.post('/generate', request);
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
            const health = await this.checkHealth();
            return {
                success: health.status === 'healthy',
                error: health.status !== 'healthy' ? 'Backend service is not healthy' : undefined
            };
        }
        catch (error) {
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