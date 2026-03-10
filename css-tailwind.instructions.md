---
applyTo: "**/*.css,**/*.ts,**/*.tsx"
---

# Styling & Tailwind Rules

## 1. Tailwind-First Policy
- **Primary Tool**: Use Tailwind CSS strictly for styling.
- Minimize bespoke CSS; if Tailwind can accomplish the layout or look (even with arbitrary values like `w-[24px]`), skip custom stylesheets.

## 2. Best Practices & Organization
- Always install and use `prettier-plugin-tailwindcss` to enforce consistent utility class ordering.
- Generally group classes conceptually (even if the plugin sorts them automatically later): Position -> View/Layout -> Spacing -> Typography -> Backgrounds -> Borders -> Effects.
- Keep deeply composed utilities in extracted constants or map over arrays instead of repeating dense HTML markup.

## 3. Responsive Web Design
- **Mobile-First Paradigm**: Write default styles for mobile (small screens).
- Incrementally use `sm:`, `md:`, `lg:`, `xl:` breakpoints for wider displays.
- Guarantee that all layouts (Journals, Mood Trackers) flow naturally down to mobile viewports without horizontal scrolling or overlap.

## 4. Accessibility & Interactive States
- Provide clear `:hover`, `:focus`, `:active`, and `:disabled` variants on all buttons and actionable inputs.
- Keyboard navigation is a priority: specify `:focus-visible` (e.g., `focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:outline-none`) to assist semantic accessibility.
- Ensure placeholder text contrast ratios adhere to general WCAG AA standards.

## 5. Standard CSS Usage
- Permitted *only* when absolutely mandatory (e.g., complex `@keyframes` animations, highly specific scrollbar tweaking, custom root variables not suited for Tailwind config).
- **Prohibited**: CSS-in-JS libraries (e.g., styled-components, Emotion) and inline styles (`style={{...}}`) except for dynamic, programmatic calculations that cannot be solved via Tailwind utility interpolation.
