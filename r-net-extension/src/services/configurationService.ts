import * as vscode from 'vscode';

export interface ExtensionConfig {
    backend: {
        url: string;
        timeout: number;
    };
    generation: {
        autoOpen: boolean;
        createFolder: boolean;
    };
    ui: {
        theme: 'auto' | 'light' | 'dark';
    };
}

export class ConfigurationService {
    private static readonly EXTENSION_ID = 'rnet-ai';
    
    /**
     * Get the current extension configuration
     */
    static getConfiguration(): ExtensionConfig {
        const config = vscode.workspace.getConfiguration(this.EXTENSION_ID);
        
        return {
            backend: {
                url: config.get('backend.url', 'http://127.0.0.1:8000'),
                timeout: config.get('backend.timeout', 60000)
            },
            generation: {
                autoOpen: config.get('generation.autoOpen', true),
                createFolder: config.get('generation.createFolder', true)
            },
            ui: {
                theme: config.get('ui.theme', 'auto') as 'auto' | 'light' | 'dark'
            }
        };
    }
    
    /**
     * Update a configuration value
     */
    static async updateConfiguration(key: string, value: any, target?: vscode.ConfigurationTarget): Promise<void> {
        const config = vscode.workspace.getConfiguration(this.EXTENSION_ID);
        await config.update(key, value, target || vscode.ConfigurationTarget.Global);
    }
    
    /**
     * Validate backend connection
     */
    static async validateBackendConnection(url?: string): Promise<{ success: boolean; error?: string }> {
        const backendUrl = url || this.getConfiguration().backend.url;
        
        try {
            // We'll implement this when we add the HTTP client
            return { success: true };
        } catch (error) {
            return { 
                success: false, 
                error: error instanceof Error ? error.message : 'Unknown error' 
            };
        }
    }
    
    /**
     * Show configuration dialog
     */
    static async showConfigurationDialog(): Promise<void> {
        const config = this.getConfiguration();
        
        const backendUrl = await vscode.window.showInputBox({
            prompt: 'Backend Service URL',
            value: config.backend.url,
            validateInput: (value: string) => {
                if (!value) return 'URL is required';
                try {
                    // Simple URL validation
                    const urlPattern = /^https?:\/\/.+/;
                    if (!urlPattern.test(value)) {
                        return 'URL must start with http:// or https://';
                    }
                    return null;
                } catch {
                    return 'Invalid URL format';
                }
            }
        });
        
        if (backendUrl) {
            await this.updateConfiguration('backend.url', backendUrl);
            vscode.window.showInformationMessage('Configuration updated successfully!');
        }
    }
    
    /**
     * Register configuration change listener
     */
    static onConfigurationChanged(callback: (e: vscode.ConfigurationChangeEvent) => void): vscode.Disposable {
        return vscode.workspace.onDidChangeConfiguration((e: vscode.ConfigurationChangeEvent) => {
            if (e.affectsConfiguration(this.EXTENSION_ID)) {
                callback(e);
            }
        });
    }
}