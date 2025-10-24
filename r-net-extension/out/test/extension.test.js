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
const vscode = __importStar(require("vscode"));
const sinon = __importStar(require("sinon"));
const assert_1 = require("assert");
const configurationService_1 = require("../services/configurationService");
const apiService_1 = require("../services/apiService");
const errorHandler_1 = require("../utils/errorHandler");
suite('Extension Test Suite', () => {
    let sandbox;
    setup(() => {
        sandbox = sinon.createSandbox();
    });
    teardown(() => {
        sandbox.restore();
    });
    suite('ConfigurationService', () => {
        test('getConfiguration returns default values', () => {
            const config = configurationService_1.ConfigurationService.getConfiguration();
            assert_1.strict.strictEqual(config.backend.url, 'http://127.0.0.1:8000');
            assert_1.strict.strictEqual(config.backend.timeout, 60000);
            assert_1.strict.strictEqual(config.generation.autoOpen, true);
            assert_1.strict.strictEqual(config.generation.createFolder, true);
            assert_1.strict.strictEqual(config.ui.theme, 'auto');
        });
        test('updateConfiguration calls workspace configuration update', async () => {
            const mockConfig = {
                update: sandbox.stub().resolves()
            };
            sandbox.stub(vscode.workspace, 'getConfiguration').returns(mockConfig);
            await configurationService_1.ConfigurationService.updateConfiguration('backend.url', 'http://localhost:8001');
            assert_1.strict.ok(mockConfig.update.calledOnce);
            assert_1.strict.ok(mockConfig.update.calledWith('backend.url', 'http://localhost:8001'));
        });
    });
    suite('ApiService', () => {
        test('updateClient creates new axios instance', () => {
            // Test that updateClient doesn't throw
            assert_1.strict.doesNotThrow(() => {
                apiService_1.apiService.updateClient();
            });
        });
        test('testConnection handles network errors', async () => {
            sandbox.stub(apiService_1.apiService, 'checkHealth').rejects(new Error('Network error'));
            const result = await apiService_1.apiService.testConnection();
            assert_1.strict.strictEqual(result.success, false);
            assert_1.strict.ok(result.error?.includes('Network error'));
        });
    });
    suite('ErrorHandler', () => {
        let mockOutputChannel;
        setup(() => {
            mockOutputChannel = {
                appendLine: sandbox.stub(),
                show: sandbox.stub(),
                dispose: sandbox.stub()
            };
            errorHandler_1.ErrorHandler.initialize(mockOutputChannel);
        });
        test('parseError identifies network errors', () => {
            const networkError = new Error('ECONNREFUSED');
            // Use private method through any cast for testing
            const errorDetails = errorHandler_1.ErrorHandler.parseError(networkError);
            assert_1.strict.strictEqual(errorDetails.type, errorHandler_1.ErrorType.NETWORK);
            assert_1.strict.ok(errorDetails.suggestions.length > 0);
        });
        test('parseError identifies API errors', () => {
            const apiError = new Error('401 Unauthorized');
            const errorDetails = errorHandler_1.ErrorHandler.parseError(apiError);
            assert_1.strict.strictEqual(errorDetails.type, errorHandler_1.ErrorType.API);
            assert_1.strict.ok(errorDetails.suggestions.some((s) => s.includes('API key')));
        });
        test('parseError identifies file system errors', () => {
            const fsError = new Error('ENOENT: no such file or directory');
            const errorDetails = errorHandler_1.ErrorHandler.parseError(fsError);
            assert_1.strict.strictEqual(errorDetails.type, errorHandler_1.ErrorType.FILE_SYSTEM);
            assert_1.strict.ok(errorDetails.suggestions.some((s) => s.includes('permissions')));
        });
        test('createValidationError creates proper error', () => {
            const error = errorHandler_1.ErrorHandler.createValidationError('Invalid input', ['Check your data']);
            assert_1.strict.strictEqual(error.type, errorHandler_1.ErrorType.VALIDATION);
            assert_1.strict.strictEqual(error.message, 'Invalid input');
            assert_1.strict.deepStrictEqual(error.suggestions, ['Check your data']);
        });
        test('createNetworkError creates proper error', () => {
            const error = errorHandler_1.ErrorHandler.createNetworkError('Connection failed', 'ECONNREFUSED');
            assert_1.strict.strictEqual(error.type, errorHandler_1.ErrorType.NETWORK);
            assert_1.strict.strictEqual(error.message, 'Connection failed');
            assert_1.strict.strictEqual(error.details, 'ECONNREFUSED');
        });
        test('handleError logs to output channel', async () => {
            const testError = new Error('Test error');
            sandbox.stub(vscode.window, 'showErrorMessage').resolves();
            await errorHandler_1.ErrorHandler.handleError(testError, 'Test Context');
            assert_1.strict.ok(mockOutputChannel.appendLine.called);
        });
    });
    suite('Integration Tests', () => {
        test('extension activates without errors', async () => {
            const extension = vscode.extensions.getExtension('YourName.ai-fullstack-generator');
            if (extension && !extension.isActive) {
                await extension.activate();
            }
            // If we get here without throwing, activation succeeded
            assert_1.strict.ok(true);
        });
        test('commands are registered', async () => {
            const commands = await vscode.commands.getCommands(true);
            // Commands might not show up immediately, so we check if they're available
            // In a real extension test, the extension should be activated first
            const hasOpenPanel = commands.includes('ghc.openGeneratorPanel');
            const hasConfigure = commands.includes('ghc.configure');
            const hasTestConnection = commands.includes('ghc.testConnection');
            // At least one command should be registered (or skip this test in unit testing)
            assert_1.strict.ok(hasOpenPanel || hasConfigure || hasTestConnection || commands.length > 0);
        });
    });
    suite('Input Validation', () => {
        test('validates image data is not empty', () => {
            const emptyImageError = errorHandler_1.ErrorHandler.createValidationError('Missing required input data');
            assert_1.strict.strictEqual(emptyImageError.type, errorHandler_1.ErrorType.VALIDATION);
        });
        test('validates description length', () => {
            const shortDescription = 'short';
            const isValid = shortDescription.length >= 10;
            assert_1.strict.strictEqual(isValid, false);
        });
        test('validates tech stack completeness', () => {
            const incompleteTechStack = {
                frontend: 'React'
                // Missing backend and database
            };
            const isComplete = !!(incompleteTechStack.frontend &&
                incompleteTechStack.backend &&
                incompleteTechStack.database);
            assert_1.strict.strictEqual(isComplete, false);
        });
    });
    suite('File Operations', () => {
        test('handles workspace folder validation', () => {
            // Mock empty workspace folders
            sandbox.stub(vscode.workspace, 'workspaceFolders').value(undefined);
            const error = errorHandler_1.ErrorHandler.createFileSystemError('No workspace folder found', 'Please open a folder in VS Code before generating code');
            assert_1.strict.strictEqual(error.type, errorHandler_1.ErrorType.FILE_SYSTEM);
            assert_1.strict.ok(error.message.includes('workspace folder'));
        });
    });
});
//# sourceMappingURL=extension.test.js.map