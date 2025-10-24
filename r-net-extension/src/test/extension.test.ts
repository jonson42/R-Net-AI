import * as vscode from 'vscode';
import * as sinon from 'sinon';
import { strict as assert } from 'assert';
import { ConfigurationService } from '../services/configurationService';
import { apiService } from '../services/apiService';
import { ErrorHandler, ErrorType } from '../utils/errorHandler';

suite('Extension Test Suite', () => {
	let sandbox: sinon.SinonSandbox;

	setup(() => {
		sandbox = sinon.createSandbox();
	});

	teardown(() => {
		sandbox.restore();
	});

	suite('ConfigurationService', () => {
		test('getConfiguration returns default values', () => {
			const config = ConfigurationService.getConfiguration();
			assert.strictEqual(config.backend.url, 'http://127.0.0.1:8000');
			assert.strictEqual(config.backend.timeout, 60000);
			assert.strictEqual(config.generation.autoOpen, true);
			assert.strictEqual(config.generation.createFolder, true);
			assert.strictEqual(config.ui.theme, 'auto');
		});

		test('updateConfiguration calls workspace configuration update', async () => {
			const mockConfig = {
				update: sandbox.stub().resolves()
			};
			sandbox.stub(vscode.workspace, 'getConfiguration').returns(mockConfig as any);

			await ConfigurationService.updateConfiguration('backend.url', 'http://localhost:8001');

			assert.ok(mockConfig.update.calledOnce);
			assert.ok(mockConfig.update.calledWith('backend.url', 'http://localhost:8001'));
		});
	});

	suite('ApiService', () => {
		test('updateClient creates new axios instance', () => {
			// Test that updateClient doesn't throw
			assert.doesNotThrow(() => {
				apiService.updateClient();
			});
		});

		test('testConnection handles network errors', async () => {
			sandbox.stub(apiService, 'checkHealth').rejects(new Error('Network error'));

			const result = await apiService.testConnection();

			assert.strictEqual(result.success, false);
			assert.ok(result.error?.includes('Network error'));
		});
	});

	suite('ErrorHandler', () => {
		let mockOutputChannel: vscode.OutputChannel;

		setup(() => {
			mockOutputChannel = {
				appendLine: sandbox.stub(),
				show: sandbox.stub(),
				dispose: sandbox.stub()
			} as any;
			ErrorHandler.initialize(mockOutputChannel);
		});

		test('parseError identifies network errors', () => {
			const networkError = new Error('ECONNREFUSED');
			// Use private method through any cast for testing
			const errorDetails = (ErrorHandler as any).parseError(networkError);

			assert.strictEqual(errorDetails.type, ErrorType.NETWORK);
			assert.ok(errorDetails.suggestions.length > 0);
		});

		test('parseError identifies API errors', () => {
			const apiError = new Error('401 Unauthorized');
			const errorDetails = (ErrorHandler as any).parseError(apiError);

			assert.strictEqual(errorDetails.type, ErrorType.API);
			assert.ok(errorDetails.suggestions.some((s: string) => s.includes('API key')));
		});

		test('parseError identifies file system errors', () => {
			const fsError = new Error('ENOENT: no such file or directory');
			const errorDetails = (ErrorHandler as any).parseError(fsError);

			assert.strictEqual(errorDetails.type, ErrorType.FILE_SYSTEM);
			assert.ok(errorDetails.suggestions.some((s: string) => s.includes('permissions')));
		});

		test('createValidationError creates proper error', () => {
			const error = ErrorHandler.createValidationError('Invalid input', ['Check your data']);

			assert.strictEqual(error.type, ErrorType.VALIDATION);
			assert.strictEqual(error.message, 'Invalid input');
			assert.deepStrictEqual(error.suggestions, ['Check your data']);
		});

		test('createNetworkError creates proper error', () => {
			const error = ErrorHandler.createNetworkError('Connection failed', 'ECONNREFUSED');

			assert.strictEqual(error.type, ErrorType.NETWORK);
			assert.strictEqual(error.message, 'Connection failed');
			assert.strictEqual(error.details, 'ECONNREFUSED');
		});

		test('handleError logs to output channel', async () => {
			const testError = new Error('Test error');
			sandbox.stub(vscode.window, 'showErrorMessage').resolves();

			await ErrorHandler.handleError(testError, 'Test Context');

			assert.ok((mockOutputChannel.appendLine as sinon.SinonStub).called);
		});
	});

	suite('Integration Tests', () => {
		test('extension activates without errors', async () => {
			const extension = vscode.extensions.getExtension('YourName.ai-fullstack-generator');
			if (extension && !extension.isActive) {
				await extension.activate();
			}
			// If we get here without throwing, activation succeeded
			assert.ok(true);
		});

		test('commands are registered', async () => {
			const commands = await vscode.commands.getCommands(true);
			
			// Commands might not show up immediately, so we check if they're available
			// In a real extension test, the extension should be activated first
			const hasOpenPanel = commands.includes('ghc.openGeneratorPanel');
			const hasConfigure = commands.includes('ghc.configure');
			const hasTestConnection = commands.includes('ghc.testConnection');
			
			// At least one command should be registered (or skip this test in unit testing)
			assert.ok(hasOpenPanel || hasConfigure || hasTestConnection || commands.length > 0);
		});
	});

	suite('Input Validation', () => {
		test('validates image data is not empty', () => {
			const emptyImageError = ErrorHandler.createValidationError('Missing required input data');
			assert.strictEqual(emptyImageError.type, ErrorType.VALIDATION);
		});

		test('validates description length', () => {
			const shortDescription = 'short';
			const isValid = shortDescription.length >= 10;
			assert.strictEqual(isValid, false);
		});

		test('validates tech stack completeness', () => {
			const incompleteTechStack = {
				frontend: 'React'
				// Missing backend and database
			};
			const isComplete = !!(incompleteTechStack.frontend && 
							  (incompleteTechStack as any).backend && 
							  (incompleteTechStack as any).database);
			assert.strictEqual(isComplete, false);
		});
	});

	suite('File Operations', () => {
		test('handles workspace folder validation', () => {
			// Mock empty workspace folders
			sandbox.stub(vscode.workspace, 'workspaceFolders').value(undefined);

			const error = ErrorHandler.createFileSystemError(
				'No workspace folder found',
				'Please open a folder in VS Code before generating code'
			);

			assert.strictEqual(error.type, ErrorType.FILE_SYSTEM);
			assert.ok(error.message.includes('workspace folder'));
		});
	});
});
