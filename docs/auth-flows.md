# Auth Flows & Permissions

This document outlines the authentication requirements, API keys, and access controls needed to run the automation pipeline and the AI Agent system.

## 1. Gemini API (Vision OCR)

The core data extraction pipeline (`src/analyze_with_gemini.py`) uses the Google Gemini API to perform reliable Optical Character Recognition (OCR) on the diverse screenshots submitted by the runners (Runna, Strava, Apple Fitness, Coros, Garmin, etc.).

### Requirement
- **Scope**: Access to Gemini 1.5 Pro or Gemini 1.5 Flash vision capabilities.
- **Variable**: `GEMINI_API_KEY` in the `.env` file.

### How to obtain:
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Navigate to **Get API key**.
3. Create a new key and copy it into your `.env` file.

*Security Note: The `.env` file is included in `.gitignore` and must never be committed to the repository.*

## 2. Agent Knowledge Base (NotebookLM MCP)

The AI Agents rely on the NotebookLM Model Context Protocol (MCP) server to query historical tournament rules, past decisions, and overarching logic.

### Requirement
- **Scope**: Read access to the specific NotebookLM document ID.
- **Configuration**: Managed via the user's local MCP configuration (`mcp_config.json`).
- **Notebook ID**: `b1637cb3-37a1-4cdf-8f55-36b8ae810a9a`

*Note: No dedicated API key is required in the `.env` file for this, as the MCP protocol handles workspace context injection directly via the IDE or agent runner.*

## 3. Local LLM Execution (Ollama)

For tasks that do not require multimodal vision (e.g., summarizing Thai text, translating, local drafting), agents can utilize a local Ollama instance running the `qwen3:8b` model.

### Requirement
- **Scope**: Local HTTP API access (`localhost:11434`).
- **Authentication**: None. The service must be running locally.
- **Setup**: Install Ollama and run `ollama run qwen3:8b`.

## 4. Python Interpreter Tool (Auto-Infographics)

The Tournament Reporter agent utilizes a sandboxed Python Interpreter tool (`google:python_interpreter`) to autonomously generate infographic charts (using matplotlib/seaborn).

### Requirement
- **Scope**: Sandboxed Python execution environment.
- **Authentication**: None. Controlled via the agent's tool execution access.
