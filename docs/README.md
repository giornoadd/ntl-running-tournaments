# Documentation Index

This directory contains the official rules, participant lists, and operational workflows for the **Running Competition 2026 — Mandalorian vs IT System**.

## 📊 Live Standings (as of 22 Mar 2026 — Week 12)

| Team | Total Distance | Avg/Person | Active Members |
| :--- | :--- | :--- | :--- |
| 💻 **IT System** | **840.89 km** | **84.09 km** | 8 / 10 |
| 🪖 **Mandalorian** | **724.94 km** | **72.49 km** | 8 / 10 |

> **IT System leads by 11.59 km/person** 🏆

### 🌟 Top 5 Individuals

| Rank | Name | Team | Distance |
| :---: | :--- | :--- | :--- |
| 🥇 1 | GIO | 🪖 Mandalorian | 432.97 km |
| 🥈 2 | Jojo | 💻 IT System | 299.04 km |
| 🥉 3 | Boy | 💻 IT System | 154.08 km |
| 🏅 4 | O | 💻 IT System | 151.01 km |
| 🏅 5 | Sand | 🪖 Mandalorian | 93.05 km |

---

## 📚 Standard Docs Suite

- 📐 **[Technical Architecture](technical.md)**
  Filesystem-as-Source-of-Truth architecture and Python pipeline logic.
- 🚀 **[Getting Started](getting-started.md)**
  Environment setup, Python dependencies, and manual run commands.
- 🔐 **[Auth Flows & Permissions](auth-flows.md)**
  API keys (Gemini Vision OCR), MCP integration, and access mapping.
- 🗺️ **[C4 Architecture Diagrams](c4-diagrams.md)**
  System Context and Container models for the AI Agent System.
- 📖 **[Workflow Usage Guide](usage.md)**
  Manuals for Agent slash commands and Python batch operation.

---

## 📋 Tournament Documents

- 🏆 **[Tournament Rules](tournaments/Tournament%20Rules.md)**
  Competition rules, minimum distance requirements, scoring criteria, and awards.

- 👥 **[Team Member List](tournaments/Team%20member%20list.md)**
  Official roster of 10-person teams for Mandalorian and IT System.

- 📅 **[Tournament Calendar](tournaments/Tournament%20Calendar.md)**
  Full-year weekly schedule with Thai holidays and quarterly deadlines.

## ⚙️ Operational Docs

- 🔄 **[End-to-End Workflow](End-to-End%20Workflow.md)**
  How evidence screenshots are processed — from submission to statistics.

## 🤖 AI Agent System

Four AI agents manage the tournament operations:

| Agent | Workflow | Role |
| :--- | :--- | :--- |
| 🏟️ **Coach Assistant** | `/coach-assistant` | Rename files, update CSV/stats, duplicate check, Drive sync |
| 🏃 **Running Coach** | `/running-coach` | Post-run analysis, goal setting, running plans, coach analysis |
| 📈 **Sports Analyst** | `/sports-analyst` | Infographic content, personal stats cards, recaps, README update |
| 📣 **Tournament Reporter** | `/tournament-reporter` | News, LINE/Facebook posts, motivation & engagement |
| 💻 **Software Engineer** | `/software-engineer` | Full data pipeline rebuild + React dashboard deploy |
| 🔄 **Update Dashboard** | `/update-dashboard` | Quick dashboard rebuild — recalculate, build, push |

👉 **[Full Agent Guide — How to Use](AI%20Agent%20System.md)**

**Shared Skills:** All agents can query the [NotebookLM Knowledge Base](https://notebooklm.google.com/notebook/b1637cb3-37a1-4cdf-8f55-36b8ae810a9a) and use the Local Ollama (`qwen3:8b`) for Thai text processing.

---
*Last updated: 2026-03-22*
