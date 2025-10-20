# 🚀 AI Full-Stack Generator (GHC) – VS Code Extension

**General-purpose Human-Computer Interface (GHC)**
A Visual Studio Code extension designed to **accelerate full-stack development** by generating boilerplate and functional code using AI.

This powerful tool accepts a **UI sketch (image)** and a **natural language prompt** via an embedded Webview panel, then sends this **multimodal input** to an AI backend (simulated in this repo) to generate production-ready code.

---

## ✨ Key Features

This extension provides a streamlined and structured interface for AI-assisted code generation:

* 🔁 **Multimodal Input**
  Upload or drag-and-drop UI mockups and design sketches (PNG/JPG supported).

* 🧠 **Detailed Prompting**
  Enter rich functional requirements, API logic, and UI/UX behaviors in a dedicated text area.

* 🛠️ **Granular Tech Stack Configuration**
  Choose your preferred technologies:

  * **Frontend**: React, Angular, HTML (and more)
  * **Backend**: FastAPI, Flask, .NET (and others)
  * **Database**: PostgreSQL, MongoDB (etc.)

* 🧩 **Seamless VS Code Integration**
  Fully embedded as a custom panel within the VS Code environment.

---

## 🛠️ Prerequisites

To build and run this extension locally, ensure the following are installed:

* [Node.js](https://nodejs.org/) and `npm`
* [TypeScript](https://www.typescriptlang.org/)
* [Visual Studio Code](https://code.visualstudio.com/) (v1.80.0 or later)
* Familiarity with the [VS Code Extension API](https://code.visualstudio.com/api)

---

## ⚙️ Setup and Installation

Follow these steps in your terminal to get the project running locally:

```bash
# 1. Clone the repository
git clone https://github.com/github.com/jonson42/R-Net-AI.git
cd ai-fullstack-generator

# 2. Install dependencies
npm install

# 3. Compile TypeScript source code
npm run compile
```

💡 **Note:** Compilation also ensures the `generator-webview.html` file is placed correctly in the `src/` directory, required for the extension UI.

---

## 🏃 Usage (Running the Extension)

### 1. Launch the Extension Development Host

* Open the project folder in VS Code:
  `code .`
* Go to **Run and Debug** (`Ctrl+Shift+D` / `Cmd+Shift+D`)
* Select **Run Extension** from the dropdown
* Click the green ▶️ **Start Debugging** button

A new VS Code window will open — this is your **Extension Development Host**.

### 2. Open the Generator Panel

* In the new window, open the **Command Palette**:
  `Ctrl+Shift+P` / `Cmd+Shift+P`
* Type and select:
  `GHC: Open AI Full-Stack Generator`

### 3. Generate Code

1. **Upload Image**: Select your UI sketch (PNG/JPG)
2. **Input Prompt**: Describe your app's logic and features
3. **Select Tech Stack**: Frontend, Backend, and Database options
4. Click **Generate Full-Stack Code**

📝 **Simulation Note**:
Currently, the AI response is **simulated** — a `generated_app_readme.md` file will be created in your workspace as a placeholder for generated output.

---

## 📂 Project Structure

| File / Directory         | Description                                                                       |
| ------------------------ | --------------------------------------------------------------------------------- |
| `extension.ts`           | TypeScript entry point – manages the Webview panel and handles message passing.   |
| `generator-webview.html` | UI for the generator panel. Includes HTML, Tailwind CSS, and frontend JavaScript. |
| `package.json`           | Extension manifest – defines commands, dependencies, and build scripts.           |
| `tsconfig.json`          | TypeScript compiler configuration.                                                |
| `src/`                   | Output folder containing compiled JavaScript and HTML files.                      |

---

## 🤝 Contribution

Contributions are welcome! 🚀

If you'd like to:

* Improve the UI
* Enhance message passing
* Implement real AI backend integration

...feel free to [open an issue](https://github.com/github.com/jonson42/R-Net-AI/issues) or submit a [pull request](https://github.com/jonson42/R-Net-AI/pulls).

---

## 📄 License

This project is licensed under the [8GA License](LICENSE).

