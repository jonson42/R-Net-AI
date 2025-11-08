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
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs/promises"));
const path = __importStar(require("path"));
const configurationService_1 = require("./services/configurationService");
const apiService_1 = require("./services/apiService");
const errorHandler_1 = require("./utils/errorHandler");
let outputChannel;
/**
 * The main entry point for your extension.
 * @param context The extension context provided by VS Code.
 */
function activate(context) {
    try {
        // Create output channel for logging
        outputChannel = vscode.window.createOutputChannel('R-Net AI');
        outputChannel.appendLine('=== EXTENSION ACTIVATION STARTED ===');
        outputChannel.appendLine('AI Full-Stack Generator (7GA) is now active!');
        outputChannel.show(); // Force show the output channel
        // Show activation message to user
        vscode.window.showInformationMessage('R-Net AI Extension Activated! Commands: GHC');
        console.log('R-Net AI Extension Activated Successfully');
        // Initialize error handler
        errorHandler_1.ErrorHandler.initialize(outputChannel);
        outputChannel.appendLine('Error handler initialized');
    }
    catch (error) {
        console.error('Extension activation failed:', error);
        vscode.window.showErrorMessage(`Extension activation failed: ${error}`);
        return;
    }
    // Register commands
    outputChannel.appendLine('Registering commands...');
    const openPanelCommand = vscode.commands.registerCommand('ghc.openGeneratorPanel', () => {
        outputChannel.appendLine('OpenGeneratorPanel command executed');
        vscode.window.showInformationMessage('Opening Generator Panel...');
        createGeneratorPanel(context);
    });
    const configureCommand = vscode.commands.registerCommand('ghc.configure', () => {
        console.log('GHC Configure command executed');
        outputChannel.appendLine('Configure command executed');
        vscode.window.showInformationMessage('Configure command executed!');
        configurationService_1.ConfigurationService.showConfigurationDialog();
    });
    const testConnectionCommand = vscode.commands.registerCommand('ghc.testConnection', async () => {
        outputChannel.appendLine('=== MANUAL CONNECTION TEST STARTED ===');
        outputChannel.appendLine('Test connection command executed');
        vscode.window.showInformationMessage('Testing connection...');
        try {
            await testBackendConnection();
            outputChannel.appendLine('=== MANUAL CONNECTION TEST COMPLETED ===');
        }
        catch (error) {
            outputChannel.appendLine(`=== CONNECTION TEST FAILED: ${error} ===`);
        }
    });
    // Add a simple test command
    const testCommand = vscode.commands.registerCommand('ghc.test', () => {
        outputChannel.appendLine('Simple test command executed');
        vscode.window.showInformationMessage('R-Net AI Extension is working! All commands should be available.');
    });
    // Add API test command
    const testAPICommand = vscode.commands.registerCommand('ghc.testAPI', async () => {
        outputChannel.appendLine('=== API TEST COMMAND STARTED ===');
        vscode.window.showInformationMessage('Testing API call to backend...');
        try {
            // Test health endpoint
            outputChannel.appendLine('Testing health endpoint...');
            const healthResult = await apiService_1.apiService.testConnection();
            outputChannel.appendLine(`Health test result: ${JSON.stringify(healthResult)}`);
            if (healthResult.success) {
                // Test generate endpoint with minimal data
                outputChannel.appendLine('Testing generate endpoint...');
                // Create a minimal test image (1x1 white pixel in base64)
                const testImageBase64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==';
                const testRequest = {
                    image_data: testImageBase64,
                    description: 'Simple test application with a hello world component and basic navigation',
                    tech_stack: {
                        frontend: 'React',
                        backend: 'FastAPI',
                        database: 'PostgreSQL'
                    },
                    project_name: 'api-test'
                };
                const generateResult = await apiService_1.apiService.generateCode(testRequest);
                outputChannel.appendLine(`Generate test result: Success=${generateResult.success}, Files=${generateResult.files.length}`);
                if (generateResult.success) {
                    vscode.window.showInformationMessage(`API Test Successful! Generated ${generateResult.files.length} files.`);
                }
                else {
                    vscode.window.showWarningMessage(`API Test Failed: ${generateResult.error_details || 'Unknown error'}`);
                }
            }
            else {
                vscode.window.showWarningMessage(`Health Check Failed: ${healthResult.error}`);
            }
        }
        catch (error) {
            outputChannel.appendLine(`API test error: ${error}`);
            vscode.window.showErrorMessage(`API Test Error: ${error}`);
        }
        outputChannel.appendLine('=== API TEST COMMAND COMPLETED ===');
    });
    outputChannel.appendLine('All commands registered successfully');
    // Listen for configuration changes
    const configListener = configurationService_1.ConfigurationService.onConfigurationChanged(() => {
        apiService_1.apiService.updateClient();
        outputChannel.appendLine('Configuration updated, API client refreshed');
    });
    context.subscriptions.push(openPanelCommand, configureCommand, testConnectionCommand, testCommand, testAPICommand, configListener, outputChannel);
    outputChannel.appendLine('=== EXTENSION ACTIVATION COMPLETED ===');
    outputChannel.appendLine('Commands available:');
    outputChannel.appendLine('- ghc.openGeneratorPanel (GHC: Open AI Full-Stack Generator)');
    outputChannel.appendLine('- ghc.configure (GHC: Configure Settings)');
    outputChannel.appendLine('- ghc.testConnection (GHC: Test Backend Connection)');
    // Test if commands are actually registered
    vscode.commands.getCommands(true).then(commands => {
        const ghcCommands = commands.filter(cmd => cmd.startsWith('ghc.'));
        outputChannel.appendLine(`Registered GHC commands: ${ghcCommands.join(', ')}`);
        if (ghcCommands.length === 0) {
            outputChannel.appendLine('WARNING: No GHC commands found in registered commands!');
            vscode.window.showWarningMessage('Extension commands not registered properly!');
        }
    });
}
/**
 * Test backend connection
 */
async function testBackendConnection() {
    try {
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Testing backend connection...',
            cancellable: false
        }, async () => {
            const result = await apiService_1.apiService.testConnection();
            if (result.success) {
                vscode.window.showInformationMessage('✅ Backend connection successful!');
            }
            else {
                vscode.window.showErrorMessage(`❌ Backend connection failed: ${result.error}`);
            }
        });
    }
    catch (error) {
        await errorHandler_1.ErrorHandler.handleError(error, 'Backend Connection Test');
    }
}
/**
 * Creates and shows the Webview panel containing the HTML UI.
 */
async function createGeneratorPanel(context) {
    const panel = vscode.window.createWebviewPanel('ghcGenerator', 'AI Full-Stack Generator', vscode.ViewColumn.One, {
        enableScripts: true,
        localResourceRoots: [vscode.Uri.joinPath(context.extensionUri, 'src')]
    });
    try {
        const htmlPath = vscode.Uri.joinPath(context.extensionUri, 'src', 'generator-webview.html');
        const htmlContent = await fs.readFile(htmlPath.fsPath, 'utf-8');
        panel.webview.html = htmlContent;
    }
    catch (error) {
        outputChannel.appendLine(`Error loading webview HTML: ${error}`);
        panel.webview.html = `<h1>Error Loading UI</h1><p>Could not load generator-webview.html. Check file paths and extension structure.</p>`;
        return;
    }
    // Handle messages from webview
    panel.webview.onDidReceiveMessage(async (message) => {
        if (message.command === 'generateCode') {
            await handleCodeGeneration(panel, message);
        }
    }, undefined, context.subscriptions);
}
/**
 * Handle code generation request
 */
async function handleCodeGeneration(panel, message) {
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
            throw errorHandler_1.ErrorHandler.createValidationError('Missing required input data', ['Please upload an image', 'Provide a detailed description', 'Select technology stack']);
        }
        if (description.length < 10) {
            throw errorHandler_1.ErrorHandler.createValidationError('Description is too short', ['Please provide at least 10 characters', 'Add more details about your application requirements']);
        }
        // Generate project name from description if not provided
        const generatedProjectName = project_name ||
            description.toLowerCase()
                .replace(/[^a-z0-9\s]/g, '')
                .replace(/\s+/g, '-')
                .substring(0, 30) || 'generated-app';
        // Create generation request
        const request = {
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
        const response = await apiService_1.apiService.generateCode(request);
        if (response.success) {
            // Create project files
            await createProjectFiles(response, request.project_name || 'generated-app');
            // Show success message
            panel.webview.postMessage({
                command: 'generationComplete',
                text: `Successfully generated ${response.files.length} files! Check your workspace.`
            });
            // Show info with options
            const action = await vscode.window.showInformationMessage(`Code generation completed! Generated ${response.files.length} files.`, 'Open Project Folder', 'Show Setup Instructions');
            if (action === 'Open Project Folder') {
                const workspaceFolders = vscode.workspace.workspaceFolders;
                if (workspaceFolders) {
                    const projectPath = path.join(workspaceFolders[0].uri.fsPath, request.project_name || 'generated-app');
                    vscode.commands.executeCommand('vscode.openFolder', vscode.Uri.file(projectPath), true);
                }
            }
            else if (action === 'Show Setup Instructions') {
                showSetupInstructions(response.setup_instructions);
            }
        }
        else {
            throw new Error(response.error_details || 'Code generation failed');
        }
    }
    catch (error) {
        outputChannel.appendLine(`Generation failed: ${error}`);
        const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
        panel.webview.postMessage({
            command: 'generationError',
            text: errorMessage
        });
        await errorHandler_1.ErrorHandler.handleError(error, 'Code Generation');
    }
}
/**
 * Create project files in workspace
 */
async function createProjectFiles(response, projectName) {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) {
        throw errorHandler_1.ErrorHandler.createFileSystemError('No workspace folder found', 'Please open a folder in VS Code before generating code');
    }
    const config = configurationService_1.ConfigurationService.getConfiguration();
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
    const createdFiles = [];
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
        const setupContent = `# Setup Instructions\n\n${response.setup_instructions.map((instruction, index) => `${index + 1}. ${instruction}`).join('\n')}\n`;
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
async function showSetupInstructions(instructions) {
    const content = `# R-Net AI - Setup Instructions\n\n${instructions.map((instruction, index) => `${index + 1}. ${instruction}`).join('\n\n')}\n\n---\n\nGenerated by R-Net AI Extension`;
    const document = await vscode.workspace.openTextDocument({
        content,
        language: 'markdown'
    });
    await vscode.window.showTextDocument(document);
}
// This method is called when your extension is deactivated
function deactivate() {
    if (outputChannel) {
        outputChannel.dispose();
    }
}
//# sourceMappingURL=extension.js.map