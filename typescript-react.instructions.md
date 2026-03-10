---
applyTo: "**/*.ts,**/*.tsx"
---

# TypeScript & React Standards

## 1. Strict TypeScript Enforcement
- **Strict Mode**: Assume `tsconfig.json` runs in strict mode (`strict: true`).
- **No `any`**: The use of `any` is strictly forbidden. 
  - Use `unknown` for truly dynamic types and narrow them using type guards.
- **Immutability**: Favor readonly props, `ReadonlyArray`, and immutable state updates.
- **Discriminated Unions**: Prefer discriminated unions to model complex or mutually exclusive states (e.g., `{ status: 'idle' } | { status: 'loading' } | { status: 'success', data: JournalEntry }`).
- **Type Definitions**: Export commonly reused `interface` and `type` definitions to a central types file.

## 2. React Components
- **Functional Only**: Use only Functional Components. No Class Components whatsoever.
- **Explicit Typings**: Explicitly type component props. E.g., `const MyComponent = ({ prop1 }: MyComponentProps) => ...`
- **Component Size**: Keep React components small and focused. Break them down if the JSX return tree becomes heavily indented or the file exceeds 200 lines.
- **Flat Structure Guidance**: Since all UI code resides inside `/webapp-react/src/components/`, name prefixes descriptively to avoid collision if necessary (e.g., `JournalEntryCard`, `MoodPickerWidget`).

## 3. Hooks Guidelines
- **Rules of Hooks**: Strictly adhere to calling hooks only at the top level of the component—never conditionally.
- **Custom Hooks**: Extract complex lifecycle or data-fetching logic into custom hooks (e.g., `useJournalEntries()`).
- **Dependency Arrays**: Always exhaustively declare dependencies in `useEffect`, `useCallback`, and `useMemo`.

## 4. State Management philosophy (Pure React)
- Rely solely on standard React Hooks (`useState`, `useReducer`, `useContext`, `useEffect`).
- Do not use external state libraries like Redux, Zustand, or Jotai.
- **Local State**: Keep UI state inside the specific component whenever possible.
- **Global State**: Lift state up or use React Context API strictly for genuinely global data (e.g., Authentication state, global Theme, or wide user preferences).

## 5. Backend Integration (Supabase)
- Encapsulate Supabase client logic outside of components when possible (e.g., in `services/supabase.ts`).
- Handle asynchronous boundary states (`isLoading`, `isError`, `isSuccess`) cleanly in React.
