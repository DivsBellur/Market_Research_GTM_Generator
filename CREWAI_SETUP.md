# 🎯 Capstone Project: CrewAI Market Research & GTM Generator
## Created & Code Refactored by Instructor: AL MATEUS 
## Date: 08/23/2026

Welcome to the CrewAI component of your Capstone Project!

In this lab, you will set up a **Multi-Agent System** consisting of a Head Manager, Researcher, Analyst, and GTM Strategist. The system uses **OpenAI**, **SerpAPI**, and a custom **MCP Server** to generate a full market research and go-to-market (GTM) strategy report.

## 📂 Step 1: Download the Project Files

1. Download the entire project folder from the Google Drive link provided by your instructor:

   `https://drive.google.com/drive/folders/13NQKgtnQuIJPF8QxC-8yQZJ8yWIKspR_?usp=sharing`

2. **Extract/Unzip** the folder to a convenient location, such as your Desktop or `~/dev`.

3. Open your terminal (Command Prompt, PowerShell, Terminal, or WSL) and navigate into the project folder:

```bash
cd path/to/your/project_folder
```

## 🔑 Step 2: Set Up Your `.env` File

You need to create a `.env` file to store your API keys securely.

1. In the root of your project folder, create a new file named **`.env`** with no other extension.

2. Open the `.env` file with any text editor, such as VS Code, Notepad, or TextEdit.

3. Copy and paste the **exact** content below into your file:

```env
# === API KEYS ===
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here

# === MCP SERVER CONFIG ===
# Do NOT change this unless your instructor tells you to
MCP_SSE_URL=http://127.0.0.1:8005/sse
```

4. **Replace** `your_openai_api_key_here` with your actual OpenAI API Key.

5. **Replace** `your_serpapi_api_key_here` with your actual SerpAPI API Key.

6. **Save the file.**

> ⚠️ **Important:** Do **not** share this file with anyone. It contains your private API keys.

## 🛠️ Step 3: Set Up the Environment

We will use `uv`, a fast Python package manager, to manage our environment.

### 3.1 Install `uv` If You Don't Have It

#### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS / Linux / WSL

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3.2 Initialize and Install Dependencies

Make sure you are inside the project folder, then run:

```bash
uv sync
```

If you do not have a `pyproject.toml` file, run `uv init` first, then install the required packages:

```bash
uv add crewai crewai-tools streamlit python-dotenv serpapi google-search-results
```

## 🚀 Step 4: Start the System — Two Terminals Required

You must run **two separate terminal windows**.

### Terminal 1: Start the MCP Server

The MCP server provides research tools to the agents.

```bash
uv run server.py
```

#### Expected Output

```text
🚀 Starting MarketIntel MCP Server (SerpAPI)...
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

> ⚠️ **Keep this terminal OPEN and running.**

### Terminal 2: Start the Streamlit App

Open a **new** terminal window, make sure you are in the project folder, and run:

```bash
uv run streamlit run Azure-test.py
```

#### Expected Output

```text
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.X.X:8501
```

## 💻 Step 5: Test the System

1. Open your browser and go to:

   `http://localhost:8501`

2. You will see the **CrewAI Market Research & GTM Generator** interface.

3. In the text input box, type a research topic, such as:

   * `"OpenAI competitors"`
   * `"AI market analysis"`

4. Click **Send** or press **Enter**.

5. The system will:

   * Connect to the MCP server.
   * Create 4 agents:

     * Manager
     * Researcher
     * Analyst
     * GTM Strategist
   * Run a hierarchical workflow.
   * Display a beautifully formatted report containing:

     * Market data
     * Competitor analysis
     * GTM strategy

## 🧪 Troubleshooting

### ❌ "Port 8000 already in use"

* Our MCP server is configured for **port 8005**.
* Make sure you are running `uv run server.py`.
* Make sure nothing else is using port 8005.
* To check what is using the port, run the appropriate command for your operating system:

#### macOS / Linux

```bash
lsof -i :8005
```

#### Windows

```powershell
netstat -ano | findstr :8005
```

### ❌ "You are missing the 'serpapi' package"

If you see this error, run:

```bash
uv add serpapi
uv sync
```

### ❌ "Connection refused to MCP server"

* Ensure the MCP server in **Terminal 1** is still running.
* Check that your `.env` file contains:

```env
MCP_SSE_URL=http://127.0.0.1:8005/sse
```

### ❌ "OpenAI API call failed: Error code: 400"

* Make sure your `OPENAI_API_KEY` is valid.
* Make sure your OpenAI API account has available credits.
* Ensure you are using `gpt-4o-mini` or a newer model.

## 📄 What to Submit

Once the system works successfully, capture screenshots of the following:

1. The Streamlit UI with your input.
2. The final generated GTM report.
3. Your MCP server running in the terminal.

Submit these screenshots along with your project files as part of your Capstone deliverable.

> ⚠️ **Important:** Remove the `.env` file before submitting your project, or replace all real API keys with fake/placeholder keys.

## 📌 Quick Instructor Note

> **If you are running WSL, do NOT run the PowerShell command for `uv`. WSL is Linux, so use the `curl` command instead. Also, you must run two terminals—one for the server and one for the app.**

## 🎓 Capstone Completion Checklist

* [ ] Download the project folder.
* [ ] Extract the project files.
* [ ] Navigate to the project folder in the terminal.
* [ ] Create the `.env` file.
* [ ] Add your OpenAI API key.
* [ ] Add your SerpAPI API key.
* [ ] Verify the MCP server URL.
* [ ] Install `uv` if necessary.
* [ ] Run `uv sync`.
* [ ] Start the MCP server with `uv run server.py`.
* [ ] Keep the MCP server terminal running.
* [ ] Open a second terminal.
* [ ] Start the Streamlit app with `uv run streamlit run Azure-test.py`.
* [ ] Open `http://localhost:8501`.
* [ ] Test the system with a research topic.
* [ ] Capture a screenshot of the Streamlit UI.
* [ ] Capture a screenshot of the generated GTM report.
* [ ] Capture a screenshot of the MCP server terminal.
* [ ] Remove the `.env` file or replace real API keys with fake keys before submission.

## 🎯 Expected Final Result

After completing all steps, you should have a working **CrewAI Market Research & GTM Generator** capable of accepting a research topic, coordinating multiple specialized agents, using MCP-based research tools, and producing a comprehensive market research and go-to-market strategy report.
