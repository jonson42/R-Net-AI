import * as vscode from 'vscode';
import * as fs from 'fs/promises';
import * as path from 'path';

// --- Global variables for the panel and API Key (simulated) ---
// In a real extension, you would securely load or prompt for the API key.
const API_KEY = "YOUR_GEMINI_API_KEY"; // Placeholder for the actual key

/**
 * The main entry point for your extension.
 * @param context The extension context provided by VS Code.
 */
export function activate(context: vscode.ExtensionContext) {
	console.log('AI Full-Stack Generator (GHC) is now active!');

	// Register the command that opens the Webview panel
	let disposable = vscode.commands.registerCommand('ghc.openGeneratorPanel', () => {
		createGeneratorPanel(context);
	});

	context.subscriptions.push(disposable);
}

/**
 * Creates and shows the Webview panel containing the HTML UI.
 */
async function createGeneratorPanel(context: vscode.ExtensionContext) {
	const panel = vscode.window.createWebviewPanel(
		'ghcGenerator', // Internal panel type
		'AI Full-Stack Generator', // Panel title shown to the user
		vscode.ViewColumn.One, // Editor column to show the panel in
		{
			// Enable scripts in the webview
			enableScripts: true,
			// Restrict the webview to load resources only from the extension's 'media' or 'src' directory
			localResourceRoots: [vscode.Uri.joinPath(context.extensionUri, 'src')]
		}
	);

	try {
		// 1. Read the HTML file content
		// We use Uri.joinPath to create a secure, path-agnostic URI for the file.
		// Assuming generator-webview.html is located in the 'src' directory after build.
		const htmlPath = vscode.Uri.joinPath(context.extensionUri, 'src', 'generator-webview.html');
		const htmlContent = await fs.readFile(htmlPath.fsPath, 'utf-8');
		
		// 2. Set the HTML content of the panel
		panel.webview.html = htmlContent;

	} catch (error) {
		console.error('Error loading webview HTML:', error);
		panel.webview.html = `<h1>Error Loading UI</h1><p>Could not load generator-webview.html. Check file paths and extension structure.</p>`;
		return;
	}

	// 3. Handle messages received from the Webview (generator-webview.html)
	panel.webview.onDidReceiveMessage(
		async message => {
			if (message.command === 'generateCode') {
				console.log('Received generation request from Webview.');
				
				// Show a brief message to the user that the process has started
				panel.webview.postMessage({ 
					command: 'generationStarted',
					text: 'Processing your request... Analyzing image and prompt.'
				});

				// Extract the payload
				const { image_data, description, tech_stack } = message;

				// --- Placeholder for the actual API call logic ---
				try {
					// 1. You would call your Python backend (or direct Gemini API) here.
					//    The API call uses image_data (Base64) and description.
					console.log(`Frontend Stack: ${tech_stack.frontend}, Description length: ${description.length}`);

					// 2. Simulated delay for the generation process
					await new Promise(resolve => setTimeout(resolve, 5000)); 

					// 3. Simulate receiving files and writing them to the workspace
					//    This is where you'd handle the response from your AI/backend.
					
					// Example: Create a simple placeholder file
					const workspaceFolders = vscode.workspace.workspaceFolders;
					if (workspaceFolders) {
						const rootPath = workspaceFolders[0].uri.fsPath;
						const targetFilePath = path.join(rootPath, 'generated_app_readme.md');
						
						await fs.writeFile(
							targetFilePath, 
							`# Generated Application\n\n**Frontend:** ${tech_stack.frontend}\n**Backend:** ${tech_stack.backend}\n**Database:** ${tech_stack.database}\n\n**Description:**\n${description}`
						);
						
						vscode.window.showInformationMessage('Code generation finished. Check your workspace for generated files.');
						
						panel.webview.postMessage({ 
							command: 'generationComplete',
							text: 'Successfully generated files into your workspace!'
						});
					} else {
						throw new Error("No open workspace folder found to save files.");
					}

				} catch (error) {
					console.error('Generation failed:', error);
					vscode.window.showErrorMessage(`AI Generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
					panel.webview.postMessage({ 
						command: 'generationError',
						text: `Generation failed: ${error instanceof Error ? error.message : 'Check console for details.'}`
					});
				}
			}
		},
		undefined,
		context.subscriptions
	);
}

// this method is called when your extension is deactivated
export function deactivate() {}
