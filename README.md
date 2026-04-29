# Conductor Skills

Modular AI agent skills for the **Conductor** spec-driven development framework. (Original repository: [gemini-cli-extensions/conductor](https://github.com/gemini-cli-extensions/conductor))

Conductor organizes software development into "Tracks" (features or bug fixes), providing a structured lifecycle from initialization to implementation and review. These skills allow AI agents (like Gemini CLI or Antigravity) to natively understand and execute the Conductor methodology.

## 🚀 Core Skills

- **`conductor-setup`**: Scaffolds a new project with product definitions, tech stacks, and workflows.
- **`conductor-new-track`**: Interactively plans a new feature or bug fix and generates specs/plans.
- **`conductor-implement`**: Guides the agent through the execution of a track's implementation plan.
- **`conductor-review`**: Performs automated and manual code reviews against project standards.
- **`conductor-status`**: Provides a high-level overview of project progress across all tracks.
- **`conductor-revert`**: Safely reverts specific logical units of work (tasks, phases, or tracks).

## 🛠 Installation

The fastest way to install Conductor Skills is using the universal bootstrapper.

### Gemini CLI
To install globally:
```bash
curl -fsSL https://raw.githubusercontent.com/moisgobg/conductor-skills/feat/poc/install.sh | bash
```
To install in project:
```bash
curl -fsSL https://raw.githubusercontent.com/moisgobg/conductor-skills/feat/poc/install.sh | bash -s -- --project
```

### Antigravity
To install locally in your current project:
```bash
curl -fsSL https://raw.githubusercontent.com/moisgobg/conductor-skills/feat/poc/install.sh | bash -s -- --project --antigravity
```

### Options
- `--project`: Installs skills into `./.agents/skills/` and rules into `./.agents/rules/`.
- `--antigravity`: Configures for Antigravity specific paths (e.g., `~/.gemini/antigravity/skills/`) and creates/updates compatibility rules.

## 📁 Repository Structure
- `/skills`: The protocol logic (`SKILL.md`) for each command.
- `/rules`: Compatibility rules for cross-platform tool translation.
- `install.sh`: The zero-dependency Unix bootstrapper.

## 🚂 Getting Started
Once installed, navigate to your project root and prompt your agent using natural language:
> "Let's create a new Conductor project!"
