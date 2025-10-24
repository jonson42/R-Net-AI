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
exports.ConfigurationService = void 0;
const vscode = __importStar(require("vscode"));
class ConfigurationService {
    static EXTENSION_ID = 'rnet-ai';
    /**
     * Get the current extension configuration
     */
    static getConfiguration() {
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
                theme: config.get('ui.theme', 'auto')
            }
        };
    }
    /**
     * Update a configuration value
     */
    static async updateConfiguration(key, value, target) {
        const config = vscode.workspace.getConfiguration(this.EXTENSION_ID);
        await config.update(key, value, target || vscode.ConfigurationTarget.Global);
    }
    /**
     * Validate backend connection
     */
    static async validateBackendConnection(url) {
        const backendUrl = url || this.getConfiguration().backend.url;
        try {
            // We'll implement this when we add the HTTP client
            return { success: true };
        }
        catch (error) {
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error'
            };
        }
    }
    /**
     * Show configuration dialog
     */
    static async showConfigurationDialog() {
        const config = this.getConfiguration();
        const backendUrl = await vscode.window.showInputBox({
            prompt: 'Backend Service URL',
            value: config.backend.url,
            validateInput: (value) => {
                if (!value)
                    return 'URL is required';
                try {
                    // Simple URL validation
                    const urlPattern = /^https?:\/\/.+/;
                    if (!urlPattern.test(value)) {
                        return 'URL must start with http:// or https://';
                    }
                    return null;
                }
                catch {
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
    static onConfigurationChanged(callback) {
        return vscode.workspace.onDidChangeConfiguration((e) => {
            if (e.affectsConfiguration(this.EXTENSION_ID)) {
                callback(e);
            }
        });
    }
}
exports.ConfigurationService = ConfigurationService;
//# sourceMappingURL=configurationService.js.map