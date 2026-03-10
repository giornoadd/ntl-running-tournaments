# C4 Architecture Diagrams

These diagrams map out the architecture of the **Running Competition 2026** system. Our "Filesystem-as-Source-of-Truth" approach shifts complex database systems into simple file structures managed by either Python automation or autonomous AI workflows.

---

## 1. Context Diagram

The System Context diagram provides a high-level overview of how the users (runners and administrators) interact with the core Running Competition System and its external dependencies.

```mermaid
C4Context
    title System Context: Running Competition 2026

    Person(runner, "Competitor", "A participant in the Mandalorian or IT System team")
    Person(admin, "Tournament Admin", "Manages the tournament configurations and execution")
    
    System(running_sys, "Running Competition System", "Manages the processing of evidence, calculates stats, creates leaderboards and personalized content.")
    
    System_Ext(gemini_api, "Google Gemini API", "Provides OCR capabilities to extract text and data from screenshots.")
    System_Ext(notebook_lm, "NotebookLM MCP", "Stores project context and acts as the knowledge base for AI agents.")
    System_Ext(ollama, "Local Ollama (qwen3:8b)", "Provides local LLM processing for summarization and translation.")

    Rel(runner, running_sys, "Submits running evidence (screenshots) directly to")
    Rel(runner, running_sys, "Reads leaderboard & profile data from")
    
    Rel(admin, running_sys, "Triggers AI workflows and Python pipeline via")

    Rel(running_sys, gemini_api, "Sends images for OCR extraction")
    Rel(running_sys, notebook_lm, "Queries for tournament rules/laws/history")
    Rel(running_sys, ollama, "Sends prompt for fast local Thai processing")
```

---

## 2. Container Diagram

The Container diagram zooms into the **Running Competition System** to show its core architectural components.

```mermaid
C4Container
    title Container Diagram: Running Competition System

    Person(admin, "Admin/Developer", "Triggers automation scripts or AI workflows")

    Container_Boundary(core_sys, "Running Competition Platform") {
        
        Container(python_pipeline, "Python Automation scripts", "Python 3.10+", "Handles file operations, watermarking, and core CSV calculations (recalculate_csv.py)")
        
        Container(ai_agent_sys, "AI Agent Workflows", "Prompt-driven routines", "Four distinct agents: Coach Assistant, Running Coach, Sports Analyst, Tournament Reporter")

        Container(filesystem_db, "Filesystem DB", "CSV / Markdown / Images", "The single source of truth for the entire tournament. Includes member_results/ and results/")
        
        Container(doc_site, "Documentation Hub", "Markdown", "Standardized docs/ directory, GEMINI.md index, rules and calendar files")
    }
    
    System_Ext(gemini_api, "Google Gemini API", "OCR & Multi-modal processing")

    Rel(admin, python_pipeline, "Executes", "bash / python")
    Rel(admin, ai_agent_sys, "Triggers via IDE slash commands", "/coach-assistant, /sports-analyst, etc.")
    
    Rel(python_pipeline, filesystem_db, "Reads raw images, Writes renamed images, Updates CSVs, Generates MDs")
    Rel(python_pipeline, gemini_api, "Calls API for OCR data extraction in analyze_with_gemini.py")
    
    Rel(ai_agent_sys, filesystem_db, "Reads data, Generates infographics, Writes Markdown reports")
    Rel(ai_agent_sys, doc_site, "Uses documentation logic to formulate responses")
```
