---
applyTo: "**/*"
---

# General Engineering Standards

## 1. Naming Conventions
- **Variables & Functions**: Use clear, descriptive `camelCase` names (e.g., `getUserJournal`, `isMoodSelected`).
- **Components & Classes**: Use `PascalCase` for React components and class names.
- **Constants**: Use `UPPER_SNAKE_CASE` for global constants.
- **Booleans**: Prefix boolean variables with `is`, `has`, `should`, or `can`.

## 2. File & Folder Structure
- Keep a flat structure for components where possible, minimizing deep nesting.
- Name files appropriately. React components should match their exported name (e.g., `MoodSelector.tsx`).
- Abstract shared utilities to a central `utils/` or `helpers/` folder.

## 3. Readability & Keep It Simple
- Code is read more often than written; prioritize readability over terseness.
- Write strict, self-documenting code.
- Functions should adhere to the Single Responsibility Principle. Keep them under 50 lines if possible.
- Avoid magic numbers and obscure strings; extract them to named constants.

## 4. Comments & Documentation
- Document the *why*, not the *what*. Code should explain *what* happens.
- Avoid obvious comments `// adds 1 to count`.
- Use JSDoc annotations for complex shared utilities or business logic to provide IDE intellisense.

## 5. Refactoring Discipline
- **Boy Scout Rule**: Leave the code cleaner than you found it.
- Favor incremental refactoring over complete rewrites. 
- Eliminate dead code immediately (no commented-out blocks of old code).

## 6. Error Handling
- Fail fast and recover gracefully.
- Do not swallow errors silently with empty `catch` blocks.
- Bubble errors up to boundaries or appropriate logging utilities if they cannot be handled locally.

## 7. Imports
- Organize imports logically:
  1. Built-in packages
  2. Third-party dependencies
  3. Absolute project imports (e.g., `@/components/...`)
  4. Relative local imports
- Remove unused imports strictly.

## 8. Collaboration & CI/CD
- Treat all linter warnings and TS issues as errors during development.
- Strive for deterministic, testable logic by preferring pure functions.
