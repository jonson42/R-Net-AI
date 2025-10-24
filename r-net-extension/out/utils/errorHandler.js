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
Object.defineProperty(exports, "__esModule", { value: true });
exports.ErrorHandler = exports.ExtensionError = exports.ErrorType = void 0;
const vscode = __importStar(require("vscode"));
var ErrorType;
(function (ErrorType) {
    ErrorType["VALIDATION"] = "VALIDATION";
    ErrorType["NETWORK"] = "NETWORK";
    ErrorType["API"] = "API";
    ErrorType["FILE_SYSTEM"] = "FILE_SYSTEM";
    ErrorType["CONFIGURATION"] = "CONFIGURATION";
    ErrorType["UNKNOWN"] = "UNKNOWN";
})(ErrorType || (exports.ErrorType = ErrorType = {}));
class ExtensionError extends Error {
    type;
    details;
    code;
    suggestions;
    constructor(type, message, details, code, suggestions = []) {
        super(message);
        this.name = 'ExtensionError';
        this.type = type;
        this.details = details;
        this.code = code;
        this.suggestions = suggestions;
    }
}
exports.ExtensionError = ExtensionError;
class ErrorHandler {
    static outputChannel;
    static initialize(outputChannel) {
        this.outputChannel = outputChannel;
    }
    /**
     * Handle and display errors with appropriate user feedback
     */
    static async handleError(error, context) {
        const errorDetails = this.parseError(error);
        // Log to output channel
        this.logError(errorDetails, context);
        // Show user notification with appropriate actions
        await this.showUserNotification(errorDetails);
    }
    /**
     * Parse different error types into structured format
     */
    static parseError(error) {
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
    static logError(errorDetails, context) {
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
    static async showUserNotification(errorDetails) {
        const actions = this.getActionsForError(errorDetails);
        let selectedAction;
        switch (errorDetails.type) {
            case ErrorType.NETWORK:
                selectedAction = await vscode.window.showErrorMessage(`🌐 ${errorDetails.message}`, ...actions);
                break;
            case ErrorType.API:
                selectedAction = await vscode.window.showErrorMessage(`🔑 ${errorDetails.message}`, ...actions);
                break;
            case ErrorType.FILE_SYSTEM:
                selectedAction = await vscode.window.showErrorMessage(`📁 ${errorDetails.message}`, ...actions);
                break;
            case ErrorType.VALIDATION:
                selectedAction = await vscode.window.showWarningMessage(`⚠️ ${errorDetails.message}`, ...actions);
                break;
            case ErrorType.CONFIGURATION:
                selectedAction = await vscode.window.showErrorMessage(`⚙️ ${errorDetails.message}`, ...actions);
                break;
            default:
                selectedAction = await vscode.window.showErrorMessage(`❌ ${errorDetails.message}`, ...actions);
        }
        // Handle selected action
        if (selectedAction) {
            await this.handleAction(selectedAction, errorDetails);
        }
    }
    /**
     * Get appropriate actions for error type
     */
    static getActionsForError(errorDetails) {
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
    static async handleAction(action, errorDetails) {
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
                vscode.window.showInformationMessage('Please check that VS Code has permission to read/write files in your workspace folder.');
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
    static async resetConfiguration() {
        const confirm = await vscode.window.showWarningMessage('This will reset all R-Net AI settings to their default values. Continue?', 'Yes', 'No');
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
    static createValidationError(message, suggestions = []) {
        return new ExtensionError(ErrorType.VALIDATION, message, undefined, undefined, suggestions);
    }
    /**
     * Create network error
     */
    static createNetworkError(message, details) {
        return new ExtensionError(ErrorType.NETWORK, message, details, undefined, ['Check network connection', 'Verify backend service is running']);
    }
    /**
     * Create API error
     */
    static createApiError(message, code) {
        return new ExtensionError(ErrorType.API, message, undefined, code, ['Check API key configuration', 'Verify API permissions']);
    }
    /**
     * Create file system error
     */
    static createFileSystemError(message, details) {
        return new ExtensionError(ErrorType.FILE_SYSTEM, message, details, undefined, ['Check file permissions', 'Ensure workspace is accessible']);
    }
}
exports.ErrorHandler = ErrorHandler;
//# sourceMappingURL=errorHandler.js.map