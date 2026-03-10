# GitHub Copilot Instructions

This repository contains a Vite + React + Supabase web application for a Daily Journal with Mood Tracker.

## Tech Stack & Architecture
- **Frontend**: React (Vite)
- **Language**: TypeScript (Strict Mode)
- **Styling**: Tailwind CSS (Tailwind-first approach)
- **Backend/Database**: Supabase
- **State Management**: Pure React Context & Hooks (No Redux/Zzustand)
- **Source Code Location**: All React source code is under `/webapp-react/src/`.
- **Component Architecture**: Flat structure (components go directly into `/webapp-react/src/components/`, not nested by feature/type).

## Copilot Rule Files
GitHub Copilot must reference and adhere to the following specific instruction files located in this repository:
- `general.instructions.md`: Universal engineering and code quality standards.
- `typescript-react.instructions.md`: Strict TypeScript definitions and React functional guidelines.
- `css-tailwind.instructions.md`: Tailwind utility ordering, responsive design, and accessibility rules.
- `design.instructions.md`: Project-wide UI/UX principles, layout consistency, and typography hierarchy.

Always prioritize these rules when generating code, refactoring, or suggesting improvements.
