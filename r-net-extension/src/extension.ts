import * as vscode from 'vscode';
import * as fs from 'fs/promises';
import * as path from 'path';
import { ConfigurationService } from './services/configurationService';
import { apiService, ApiService, GenerationRequest } from './services/apiService';
import { ErrorHandler, ExtensionError, ErrorType } from './utils/errorHandler';

let outputChannel: vscode.OutputChannel;

/**
 * The main entry point for your extension.
 * @param context The extension context provided by VS Code.
 */
export function activate(context: vscode.ExtensionContext) {
	// Create output channel for logging
	outputChannel = vscode.window.createOutputChannel('R-Net AI');
	outputChannel.appendLine('AI Full-Stack Generator (GHC) is now active!');

	// Initialize error handler
	ErrorHandler.initialize(outputChannel);

	// Register commands
	const openPanelCommand = vscode.commands.registerCommand('ghc.openGeneratorPanel', () => {
		createGeneratorPanel(context);
	});

	const configureCommand = vscode.commands.registerCommand('ghc.configure', () => {
		ConfigurationService.showConfigurationDialog();
	});

	const testConnectionCommand = vscode.commands.registerCommand('ghc.testConnection', async () => {
		await testBackendConnection();
	});

	// Listen for configuration changes
	const configListener = ConfigurationService.onConfigurationChanged(() => {
		apiService.updateClient();
		outputChannel.appendLine('Configuration updated, API client refreshed');
	});

	context.subscriptions.push(
		openPanelCommand,
		configureCommand,
		testConnectionCommand,
		configListener,
		outputChannel
	);
}

/**
 * Test backend connection
 */
async function testBackendConnection(): Promise<void> {
	try {
		vscode.window.withProgress(
			{
				location: vscode.ProgressLocation.Notification,
				title: 'Testing backend connection...',
				cancellable: false
			},
			async () => {
				const result = await apiService.testConnection();
				if (result.success) {
					vscode.window.showInformationMessage('✅ Backend connection successful!');
				} else {
					vscode.window.showErrorMessage(`❌ Backend connection failed: ${result.error}`);
				}
			}
		);
			} catch (error) {
			await ErrorHandler.handleError(error, 'Backend Connection Test');
		}
}

/**
 * Creates and shows the Webview panel containing the HTML UI.
 */
async function createGeneratorPanel(context: vscode.ExtensionContext) {
	const panel = vscode.window.createWebviewPanel(
		'ghcGenerator',
		'AI Full-Stack Generator',
		vscode.ViewColumn.One,
		{
			enableScripts: true,
			localResourceRoots: [vscode.Uri.joinPath(context.extensionUri, 'src')]
		}
	);

	try {
		const htmlPath = vscode.Uri.joinPath(context.extensionUri, 'src', 'generator-webview.html');
		const htmlContent = await fs.readFile(htmlPath.fsPath, 'utf-8');
		panel.webview.html = htmlContent;
	} catch (error) {
		outputChannel.appendLine(`Error loading webview HTML: ${error}`);
		panel.webview.html = `<h1>Error Loading UI</h1><p>Could not load generator-webview.html. Check file paths and extension structure.</p>`;
		return;
	}

	// Handle messages from webview
	panel.webview.onDidReceiveMessage(
		async (message: any) => {
			if (message.command === 'generateCode') {
				await handleCodeGeneration(panel, message);
			}
		},
		undefined,
		context.subscriptions
	);
}

/**
 * Handle code generation request
 */
async function handleCodeGeneration(panel: vscode.WebviewPanel, message: any): Promise<void> {
	try {
		outputChannel.appendLine('Received code generation request');
		
		// Show progress notification
		panel.webview.postMessage({
			command: 'generationStarted',
			text: 'Connecting to AI service...'
		});

		// Extract request data
		const { image_data, description, tech_stack, project_name } = message;

		// Validate inputs
		if (!image_data || !description || !tech_stack) {
			throw ErrorHandler.createValidationError(
				'Missing required input data',
				['Please upload an image', 'Provide a detailed description', 'Select technology stack']
			);
		}

		if (description.length < 10) {
			throw ErrorHandler.createValidationError(
				'Description is too short',
				['Please provide at least 10 characters', 'Add more details about your application requirements']
			);
		}

		// Generate project name from description if not provided
		const generatedProjectName = project_name || 
			description.toLowerCase()
				.replace(/[^a-z0-9\s]/g, '')
				.replace(/\s+/g, '-')
				.substring(0, 30) || 'generated-app';

		// Create generation request
		const request: GenerationRequest = {
			image_data,
			description,
			tech_stack,
			project_name: generatedProjectName
		};

		outputChannel.appendLine(`Starting generation for project: ${request.project_name}`);
		outputChannel.appendLine(`Tech stack: ${JSON.stringify(tech_stack)}`);

		// Update progress
		panel.webview.postMessage({
			command: 'generationStarted',
			text: 'Generating code with AI... This may take 15-45 seconds.'
		});

		// Call API service
		const response = await apiService.generateCode(request);

		if (response.success) {
			// Create project files
			await createProjectFiles(response, request.project_name || 'generated-app');
			
			// Show success message
			panel.webview.postMessage({
				command: 'generationComplete',
				text: `Successfully generated ${response.files.length} files! Check your workspace.`
			});

			// Show info with options
			const action = await vscode.window.showInformationMessage(
				`Code generation completed! Generated ${response.files.length} files.`,
				'Open Project Folder',
				'Show Setup Instructions'
			);

			if (action === 'Open Project Folder') {
				const workspaceFolders = vscode.workspace.workspaceFolders;
				if (workspaceFolders) {
					const projectPath = path.join(workspaceFolders[0].uri.fsPath, request.project_name || 'generated-app');
					vscode.commands.executeCommand('vscode.openFolder', vscode.Uri.file(projectPath), true);
				}
			} else if (action === 'Show Setup Instructions') {
				showSetupInstructions(response.setup_instructions);
			}

		} else {
			throw new Error(response.error_details || 'Code generation failed');
		}

	} catch (error) {
		outputChannel.appendLine(`Generation failed: ${error}`);
		
		const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
		
		panel.webview.postMessage({
			command: 'generationError',
			text: errorMessage
		});

		await ErrorHandler.handleError(error, 'Code Generation');
	}
}

/**
 * Create project files in workspace
 */
async function createProjectFiles(response: any, projectName: string): Promise<void> {
	const workspaceFolders = vscode.workspace.workspaceFolders;
	if (!workspaceFolders) {
		throw ErrorHandler.createFileSystemError(
			'No workspace folder found',
			'Please open a folder in VS Code before generating code'
		);
	}

	const config = ConfigurationService.getConfiguration();
	const rootPath = workspaceFolders[0].uri.fsPath;
	
	// Create project directory if configured
	const projectPath = config.generation.createFolder 
		? path.join(rootPath, projectName) 
		: rootPath;

	// Create project directory
	if (config.generation.createFolder) {
		await fs.mkdir(projectPath, { recursive: true });
	}

	// Create all files
	const createdFiles: string[] = [];
	
	for (const file of response.files) {
		const filePath = path.join(projectPath, file.path);
		const fileDir = path.dirname(filePath);
		
		// Create directory structure
		await fs.mkdir(fileDir, { recursive: true });
		
		// Write file content
		await fs.writeFile(filePath, file.content, 'utf-8');
		createdFiles.push(filePath);
		
		outputChannel.appendLine(`Created: ${file.path}`);
	}

	// Create setup instructions file
	if (response.setup_instructions && response.setup_instructions.length > 0) {
		const setupPath = path.join(projectPath, 'SETUP.md');
		const setupContent = `# Setup Instructions\n\n${response.setup_instructions.map((instruction: string, index: number) => `${index + 1}. ${instruction}`).join('\n')}\n`;
		await fs.writeFile(setupPath, setupContent, 'utf-8');
		createdFiles.push(setupPath);
	}

	// Open first file if configured
	if (config.generation.autoOpen && createdFiles.length > 0) {
		const firstFile = createdFiles.find(f => f.endsWith('.md') || f.endsWith('.ts') || f.endsWith('.js') || f.endsWith('.py'));
		if (firstFile) {
			const document = await vscode.workspace.openTextDocument(firstFile);
			await vscode.window.showTextDocument(document);
		}
	}

	outputChannel.appendLine(`Created ${createdFiles.length} files in ${projectPath}`);
}

/**
 * Show setup instructions in a new document
 */
async function showSetupInstructions(instructions: string[]): Promise<void> {
	const content = `# R-Net AI - Setup Instructions\n\n${instructions.map((instruction, index) => `${index + 1}. ${instruction}`).join('\n\n')}\n\n---\n\nGenerated by R-Net AI Extension`;
	
	const document = await vscode.workspace.openTextDocument({
		content,
		language: 'markdown'
	});
	
	await vscode.window.showTextDocument(document);
}

// This method is called when your extension is deactivated
export function deactivate() {
	if (outputChannel) {
		outputChannel.dispose();
	}
}
