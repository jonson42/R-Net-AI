import * as vscode from 'vscode';
import axios, { AxiosInstance, AxiosError } from 'axios';
import { ConfigurationService } from './configurationService';

export interface GenerationRequest {
    image_data: string;
    description: string;
    tech_stack: {
        frontend: string;
        backend: string;
        database: string;
    };
    project_name?: string;
}

export interface GeneratedFile {
    path: string;
    content: string;
    description: string;
}

export interface GenerationResponse {
    success: boolean;
    message: string;
    project_structure: Record<string, any>;
    files: GeneratedFile[];
    dependencies: Record<string, string[]>;
    setup_instructions: string[];
    error_details?: string;
}

export interface HealthResponse {
    status: string;
    version: string;
    openai_connected: boolean;
}

export class ApiService {
    private client!: AxiosInstance;
    
    constructor() {
        this.updateClient();
    }
    
    /**
     * Update the HTTP client with current configuration
     */
    updateClient(): void {
        const config = ConfigurationService.getConfiguration();
        
        this.client = axios.create({
            baseURL: config.backend.url,
            timeout: config.backend.timeout,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        // Add request interceptor for logging
        this.client.interceptors.request.use(
            (config: any) => {
                // Log request for debugging
                return config;
            },
            (error: any) => {
                return Promise.reject(error);
            }
        );
        
        // Add response interceptor for logging
        this.client.interceptors.response.use(
            (response: any) => {
                // Log response for debugging
                return response;
            },
            (error: any) => {
                return Promise.reject(error);
            }
        );
    }
    
    /**
     * Check backend service health
     */
    async checkHealth(): Promise<HealthResponse> {
        try {
            const response = await this.client.get<HealthResponse>('/health');
            return response.data;
        } catch (error) {
            throw this.handleError(error, 'Failed to check backend service health');
        }
    }
    
    /**
     * Generate code using the backend service
     */
    async generateCode(request: GenerationRequest): Promise<GenerationResponse> {
        try {
            const response = await this.client.post<GenerationResponse>('/generate', request);
            return response.data;
        } catch (error) {
            throw this.handleError(error, 'Code generation failed');
        }
    }
    
    /**
     * Test the backend connection
     */
    async testConnection(): Promise<{ success: boolean; error?: string }> {
        try {
            const health = await this.checkHealth();
            return { 
                success: health.status === 'healthy',
                error: health.status !== 'healthy' ? 'Backend service is not healthy' : undefined
            };
        } catch (error) {
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error'
            };
        }
    }
    
    /**
     * Handle API errors with user-friendly messages
     */
    private handleError(error: unknown, defaultMessage: string): Error {
        if (axios.isAxiosError(error)) {
            const axiosError = error as AxiosError;
            
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
                const data = axiosError.response.data as any;
                
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
    static showErrorMessage(error: Error): void {
        const message = error.message;
        
        // Show different types of notifications based on error
        if (message.includes('not running') || message.includes('ECONNREFUSED')) {
            vscode.window.showErrorMessage(
                message,
                'Open Backend Setup Guide'
            ).then((selection: string | undefined) => {
                if (selection === 'Open Backend Setup Guide') {
                    vscode.env.openExternal(vscode.Uri.parse('https://github.com/jonson42/R-Net-AI#backend-setup'));
                }
            });
        } else if (message.includes('API key')) {
            vscode.window.showErrorMessage(
                message,
                'Configure Settings'
            ).then((selection: string | undefined) => {
                if (selection === 'Configure Settings') {
                    vscode.commands.executeCommand('workbench.action.openSettings', 'rnet-ai');
                }
            });
        } else {
            vscode.window.showErrorMessage(message);
        }
    }
}

// Global service instance
export const apiService = new ApiService();