---
applyTo: "**/*.tsx,**/*.ts,**/*.css"
---

# Design & UI/UX Principles

## 1. Minimal & Frictionless UI
- **Primary Objective**: The interface should be uncluttered to maximize the user's focus on journaling and mood tracking.
- Do not let decorative elements overwhelm content. Keep it obvious, simple, and clean.

## 2. Layout, Grid & Spacing Systems
- Employ consistent padding and margin scaling across identical component types.
- Value negative (white) space. Embrace "breathing room" to distinctly group related UI sections.
- For layouts where data flows vertically (e.g., a timeline of past journals), ensure horizontal rhythm matches the grid correctly.

## 3. Typography Hierarchy
- Fonts represent narrative context: scale sizes purposefully to establish visual hierarchy.
  - **H1 / Primary Titles**: (E.g., "Today's Journal") should be unmistakably prominent.
  - **H2/H3 / Subheadings**: Clearly separate sections.
  - **Body Text**: Must prioritize optimal line-height (~1.5 to 1.6) and restricted max character width (e.g., `max-w-prose`) to avoid eye fatigue.

## 4. Color & Semantic Use
- **Constraint**: Stick to a restrained color palette.
- **Mood Tracking**: Mood representation must consistently map to specific semantic colors throughout the app without deviating (e.g., Joy=Yellow, Sadness=Blue). 
- Use colors purposefully to communicate status (Error=Red, Success=Green, Warning=Amber), not exclusively for decoration.

## 5. UI Component Consistency
- Treat input fields, buttons, and journal cards as unified modular components. 
- Disallow layout fragmentation (e.g., using two completely different card layouts for Journal objects unless context directly demands).
- Define "Primary" vs. "Secondary" UI components (e.g., a solid background Primary button vs a ghost Secondary button).

## 6. Accessibility (System-Agnostic)
- Ensure contrast between text and background accommodates all users visually.
- Never use color alone to convey critical information (use icons/text alongside semantic color).
- Include appropriate semantic HTML (`<main>`, `<section>`, `<article>`, `<nav>`).
