import * as vscode from 'vscode';

export enum ErrorType {
    VALIDATION = 'VALIDATION',
    NETWORK = 'NETWORK',
    API = 'API',
    FILE_SYSTEM = 'FILE_SYSTEM',
    CONFIGURATION = 'CONFIGURATION',
    UNKNOWN = 'UNKNOWN'
}

export interface ErrorDetails {
    type: ErrorType;
    message: string;
    details?: string;
    code?: string;
    suggestions?: string[];
}

export class ExtensionError extends Error {
    public readonly type: ErrorType;
    public readonly details?: string;
    public readonly code?: string;
    public readonly suggestions: string[];

    constructor(type: ErrorType, message: string, details?: string, code?: string, suggestions: string[] = []) {
        super(message);
        this.name = 'ExtensionError';
        this.type = type;
        this.details = details;
        this.code = code;
        this.suggestions = suggestions;
    }
}

export class ErrorHandler {
    private static outputChannel: vscode.OutputChannel;

    static initialize(outputChannel: vscode.OutputChannel) {
        this.outputChannel = outputChannel;
    }

    /**
     * Handle and display errors with appropriate user feedback
     */
    static async handleError(error: unknown, context?: string): Promise<void> {
        const errorDetails = this.parseError(error);
        
        // Log to output channel
        this.logError(errorDetails, context);
        
        // Show user notification with appropriate actions
        await this.showUserNotification(errorDetails);
    }

    /**
     * Parse different error types into structured format
     */
    private static parseError(error: unknown): ErrorDetails {
        if (error instanceof ExtensionError) {
            return {
                type: error.type,
                message: error.message,
                details: error.details,
                code: error.code,
                suggestions: error.suggestions
            };
        }

        if (error instanceof Error) {
            // Network errors
            if (error.message.includes('ECONNREFUSED') || error.message.includes('ENOTFOUND')) {
                return {
                    type: ErrorType.NETWORK,
                    message: 'Cannot connect to backend service',
                    details: error.message,
                    suggestions: [
                        'Make sure the backend service is running',
                        'Check the backend URL in settings',
                        'Verify your network connection'
                    ]
                };
            }

            // File system errors
            if (error.message.includes('ENOENT') || error.message.includes('EACCES')) {
                return {
                    type: ErrorType.FILE_SYSTEM,
                    message: 'File system error',
                    details: error.message,
                    suggestions: [
                        'Check file permissions',
                        'Ensure the workspace folder is accessible',
                        'Try running VS Code as administrator (if needed)'
                    ]
                };
            }

            // API errors
            if (error.message.includes('API') || error.message.includes('401') || error.message.includes('403')) {
                return {
                    type: ErrorType.API,
                    message: 'API authentication or access error',
                    details: error.message,
                    suggestions: [
                        'Check your OpenAI API key',
                        'Verify API key permissions',
                        'Check API usage limits'
                    ]
                };
            }

            // Generic error
            return {
                type: ErrorType.UNKNOWN,
                message: error.message,
                details: error.stack,
                suggestions: ['Try again', 'Check the output logs for more details']
            };
        }

        // Non-Error objects
        return {
            type: ErrorType.UNKNOWN,
            message: 'An unknown error occurred',
            details: String(error),
            suggestions: ['Try again', 'Restart VS Code if the issue persists']
        };
    }

    /**
     * Log error details to output channel
     */
    private static logError(errorDetails: ErrorDetails, context?: string): void {
        const timestamp = new Date().toISOString();
        
        this.outputChannel.appendLine(`[${timestamp}] ERROR ${context ? `(${context})` : ''}`);
        this.outputChannel.appendLine(`Type: ${errorDetails.type}`);
        this.outputChannel.appendLine(`Message: ${errorDetails.message}`);
        
        if (errorDetails.code) {
            this.outputChannel.appendLine(`Code: ${errorDetails.code}`);
        }
        
        if (errorDetails.details) {
            this.outputChannel.appendLine(`Details: ${errorDetails.details}`);
        }
        
        if (errorDetails.suggestions && errorDetails.suggestions.length > 0) {
            this.outputChannel.appendLine('Suggestions:');
            errorDetails.suggestions.forEach((suggestion, index) => {
                this.outputChannel.appendLine(`  ${index + 1}. ${suggestion}`);
            });
        }
        
        this.outputChannel.appendLine('---');
    }

    /**
     * Show appropriate user notification based on error type
     */
    private static async showUserNotification(errorDetails: ErrorDetails): Promise<void> {
        const actions = this.getActionsForError(errorDetails);
        
        let selectedAction: string | undefined;
        
        switch (errorDetails.type) {
            case ErrorType.NETWORK:
                selectedAction = await vscode.window.showErrorMessage(
                    `🌐 ${errorDetails.message}`,
                    ...actions
                );
                break;
                
            case ErrorType.API:
                selectedAction = await vscode.window.showErrorMessage(
                    `🔑 ${errorDetails.message}`,
                    ...actions
                );
                break;
                
            case ErrorType.FILE_SYSTEM:
                selectedAction = await vscode.window.showErrorMessage(
                    `📁 ${errorDetails.message}`,
                    ...actions
                );
                break;
                
            case ErrorType.VALIDATION:
                selectedAction = await vscode.window.showWarningMessage(
                    `⚠️ ${errorDetails.message}`,
                    ...actions
                );
                break;
                
            case ErrorType.CONFIGURATION:
                selectedAction = await vscode.window.showErrorMessage(
                    `⚙️ ${errorDetails.message}`,
                    ...actions
                );
                break;
                
            default:
                selectedAction = await vscode.window.showErrorMessage(
                    `❌ ${errorDetails.message}`,
                    ...actions
                );
        }
        
        // Handle selected action
        if (selectedAction) {
            await this.handleAction(selectedAction, errorDetails);
        }
    }

    /**
     * Get appropriate actions for error type
     */
    private static getActionsForError(errorDetails: ErrorDetails): string[] {
        const commonActions = ['Show Logs', 'Try Again'];
        
        switch (errorDetails.type) {
            case ErrorType.NETWORK:
                return ['Configure Backend', 'Test Connection', ...commonActions];
                
            case ErrorType.API:
                return ['Configure API Key', 'Check Settings', ...commonActions];
                
            case ErrorType.CONFIGURATION:
                return ['Open Settings', 'Reset Configuration', ...commonActions];
                
            case ErrorType.FILE_SYSTEM:
                return ['Check Permissions', 'Select Different Folder', ...commonActions];
                
            default:
                return commonActions;
        }
    }

    /**
     * Handle user action selection
     */
    private static async handleAction(action: string, errorDetails: ErrorDetails): Promise<void> {
        switch (action) {
            case 'Show Logs':
                this.outputChannel.show();
                break;
                
            case 'Configure Backend':
                vscode.commands.executeCommand('ghc.configure');
                break;
                
            case 'Test Connection':
                vscode.commands.executeCommand('ghc.testConnection');
                break;
                
            case 'Configure API Key':
            case 'Check Settings':
            case 'Open Settings':
                vscode.commands.executeCommand('workbench.action.openSettings', 'rnet-ai');
                break;
                
            case 'Reset Configuration':
                await this.resetConfiguration();
                break;
                
            case 'Check Permissions':
                vscode.window.showInformationMessage(
                    'Please check that VS Code has permission to read/write files in your workspace folder.'
                );
                break;
                
            case 'Select Different Folder':
                vscode.commands.executeCommand('workbench.action.files.openFolder');
                break;
                
            case 'Try Again':
                // This would typically trigger the last failed operation
                vscode.window.showInformationMessage('Please try your last operation again.');
                break;
        }
    }

    /**
     * Reset configuration to defaults
     */
    private static async resetConfiguration(): Promise<void> {
        const confirm = await vscode.window.showWarningMessage(
            'This will reset all R-Net AI settings to their default values. Continue?',
            'Yes', 'No'
        );
        
        if (confirm === 'Yes') {
            const config = vscode.workspace.getConfiguration('rnet-ai');
            await config.update('backend.url', undefined, vscode.ConfigurationTarget.Global);
            await config.update('backend.timeout', undefined, vscode.ConfigurationTarget.Global);
            await config.update('generation.autoOpen', undefined, vscode.ConfigurationTarget.Global);
            await config.update('generation.createFolder', undefined, vscode.ConfigurationTarget.Global);
            await config.update('ui.theme', undefined, vscode.ConfigurationTarget.Global);
            
            vscode.window.showInformationMessage('Configuration reset to defaults.');
        }
    }

    /**
     * Create validation error
     */
    static createValidationError(message: string, suggestions: string[] = []): ExtensionError {
        return new ExtensionError(ErrorType.VALIDATION, message, undefined, undefined, suggestions);
    }

    /**
     * Create network error
     */
    static createNetworkError(message: string, details?: string): ExtensionError {
        return new ExtensionError(
            ErrorType.NETWORK, 
            message, 
            details, 
            undefined, 
            ['Check network connection', 'Verify backend service is running']
        );
    }

    /**
     * Create API error
     */
    static createApiError(message: string, code?: string): ExtensionError {
        return new ExtensionError(
            ErrorType.API, 
            message, 
            undefined, 
            code, 
            ['Check API key configuration', 'Verify API permissions']
        );
    }

    /**
     * Create file system error
     */
    static createFileSystemError(message: string, details?: string): ExtensionError {
        return new ExtensionError(
            ErrorType.FILE_SYSTEM, 
            message, 
            details, 
            undefined, 
            ['Check file permissions', 'Ensure workspace is accessible']
        );
    }
}