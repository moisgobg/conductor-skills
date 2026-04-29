# Conductor System Protocol

This document defines the strict operational and behavioral constraints for any AI agent interacting with this project. You MUST adhere to these principles at all times to ensure consistency, reliability, and project integrity.

## 1. Fidelity (No Hallucination)
- **Source of Truth:** Never assume architectural patterns, styling, or workflows. You MUST always refer to the local `conductor/` directory (specifically `workflow.md` and `code_styleguides/`) as the absolute source of truth.
- **Asset Constraint:** Do not generate standard configuration files (like `.gitignore`, linters) from memory if a project-specific template or style guide exists.

## 2. Git Integrity
- **Atomic Commits:** Every logical phase or task completion MUST result in a Git commit. Never bundle unrelated changes.
- **Traceability:** Never leave the `conductor/` directory in a "dirty" uncommitted state after completing a major action (like setting up the project, planning a track, or updating the registry).
- **History Respect:** When reverting or modifying past work, base your actions on the verifiable `git log`, not just the written plan.

## 3. Path & Environment Agnosticism
- **Relative Paths:** Always use relative paths starting from the project root (e.g., `conductor/product.md`) for file operations.
- **Intent over Tooling:** Follow the logical intent of the instructions. If a specific tool (like an interactive prompt) is not available in your current environment, achieve the same objective using standard conversational output or available fallback tools.
