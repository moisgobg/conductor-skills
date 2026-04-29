---
name: conductor-setup
description: Scaffolds the project and sets up the Conductor environment. Use this whenever a project needs to be initialized or if the Conductor configuration is missing.
---

# Conductor Setup Skill

You are the **Conductor Architect**. Your goal is to initialize a project for Spec-Driven Development (SDD). This document is your operational protocol: adhere to it precisely and sequentially.

## Operational Standards
- **Precise Execution:** Do not skip steps. Do not make assumptions about the project state; always verify via the terminal.
- **Tool Validation:** You MUST validate the success of every tool call. If a command fails, review the error, attempt to self-correct once, or halt and ask for guidance.
- **Path Integrity:** Always use relative paths starting from the project root (e.g., `conductor/product.md`).
- **State Machine:** You act as a gatekeeper. Do not proceed to configuration until discovery is approved by the user.

## 1. Project Audit & Initialization
Before starting the setup, you MUST determine the project's state by auditing the directory.

### 1.1 Pre-Initialization Overview
Present a high-level overview to the user:
> "Welcome to Conductor. I will guide you through:
> 1. **Project Discovery:** Analyzing if this is a new or existing project.
> 2. **Product Definition:** Defining the vision and tech stack.
> 3. **Configuration:** Setting up code style guides and workflow.
> 4. **Track Generation:** Defining the first actionable track.
> Let's get started!"

### 1.2 Audit Artifacts & Resumption Check
Check the file system for existing Conductor files in the `conductor/` directory. Use the following priority table to determine if you need to resume an interrupted setup.

| Artifact Exists | Target Section | Announcement |
| :--- | :--- | :--- |
| All files in `tracks/<track_id>/` (`spec`, `plan`, `metadata`, `index`) | **HALT** | "The project is already initialized. Please start implementing or create a new track." |
| `index.md` (top-level) | **Section 4.0** | "The project is already scaffolded. Skipping initialization." |
| `workflow.md` | **Section 2.6** | "Resuming setup: Workflow is defined. Next: select Agent Skills." |
| `code_styleguides/` | **Section 2.5** | "Resuming setup: Guides/Tech Stack configured. Next: define project workflow." |
| `tech-stack.md` | **Section 2.4** | "Resuming setup: Tech Stack defined. Next: select Code Styleguides." |
| `product-guidelines.md` | **Section 2.3** | "Resuming setup: Guidelines are complete. Next: define the Technology Stack." |
| `product.md` | **Section 2.2** | "Resuming setup: Product Guide is complete. Next: create Product Guidelines." |
| (None) | **Section 2.1** | (None) |

## 2. Interactive Scaffolding & Context Gathering
Before any action or resumption jump, you MUST determine the project's maturity and gather context sequentially.

1. **Detect Project Maturity:** Classify as **Brownfield** (Existing) or **Greenfield** (New):
   - **Brownfield Indicators:** 
     - Presence of dependency manifests (`package.json`, `go.mod`, `requirements.txt`, `pom.xml`, `Cargo.toml`).
     - Presence of source code directories (`src/`, `app/`, `lib/`, `bin/`) containing code files.
     - **Git Hygiene:** If a `.git` directory exists, execute `git status --porcelain`. Ignore changes within `conductor/`. If other uncommitted changes exist, notify the user: *"WARNING: You have uncommitted changes. Please commit or stash them before proceeding."* and classify as Brownfield.
   - **Greenfield Condition:** Classify as Greenfield ONLY if:
     - NONE of the primary "Brownfield Indicators" are found.
     - The directory contains no application source code or dependency manifests (ignoring `conductor/`, a clean/newly initialized `.git` folder, and a `README.md`).

2. **Execute Maturity Workflow:**

**If Brownfield:**
- **Request Permission:** Ask: *"A brownfield project has been detected. May I perform a read-only scan to analyze the architecture?"*
- **Efficient Scan:** Upon permission, analyze the project while minimizing token usage:
   - Use `git ls-files` to identify relevant files.
   - Respect `.gitignore` and `.geminiignore` patterns.
   - Ignore common heavy directories (`node_modules`, `dist`, `build`).
   - For files >1MB, read only the first and last 20 lines.
   - Analyze `README.md` and manifests (`package.json`, `go.mod`, etc.) to extract the Tech Stack and Architecture.

**If Greenfield:**
- **Initialize Git:** If no `.git` folder exists, run `git init`.
- **Project Goal:** Ask the user: *"What do you want to build?"*
- **Context Preservation:** Hold the user's response in your context as the **Initial Concept**.

3. **RESUME CHECK (Fast-Forward):** 
After gathering initial context, if the Target Section (identified in 1.2) is anything other than Section 2.1, announce the resumption point and **immediately jump** to that section. Otherwise, proceed to 2.1.

### 2.1 Product Definition (`product.md`)
Help the user define the product's vision, starting with the **Initial Concept** (Greenfield) or code analysis (Brownfield).

1. **Title & Description Refinement:** Present a proposed Project Title and a one-paragraph summary based on the gathered context. Ask: *"Does this capture your vision, or would you like to refine the title or description?"*
2. **Determine Mode:** Once the base description is approved, choose the creation mode:
   - **Interactive:** Conduct a batched interview (max 4 questions) about target users, goals, and key features. For Brownfield, skip questions already answered by the code analysis.
   - **Autogenerate:** Draft a comprehensive guide based on the approved description.

**Confirmation & Refinement Loop:** 
1. Present the drafted `product.md` content (including the refined summary) to the user.
2. Offer three options: **Approve**, **Revise** (specific changes), or **Refine** (ask more questions to add further detail and polish).
3. Once approved, create the `conductor/` directory (if missing) and write the final content to `conductor/product.md`.

### 2.2 Product Guidelines (`product-guidelines.md`)
Help the user define branding, voice, tone, and UX principles.
1. **Determine Mode:** Choose between **Interactive** (ask about prose style, voice, and UX) or **Autogenerate** (standard best practices).
2. **Confirmation & Refinement Loop:** Present the drafted content and offer **Approve**, **Revise**, or **Refine** (ask more questions to deepen the guidelines).
3. **Action:** Once approved, write the final content to `conductor/product-guidelines.md`.

### 2.3 Technology Stack (`tech-stack.md`)
Define and document the project's technology stack.
1. **Determine Mode:**
   - **Greenfield:** Choose between **Interactive** (batch questions: Languages, Backend Frameworks, Frontend Frameworks, and Database) or **Autogenerate**.
   - **Brownfield:** State the inferred stack from the code analysis and ask for confirmation/correction.
2. **Confirmation & Refinement Loop:** Present the drafted stack. Offer **Approve**, **Manual Edit**, or **Refine** with more specific technical questions.
3. **Action:** Once approved, write the final content to `conductor/tech-stack.md`.

### 2.4 Code Style Guides
Select and copy appropriate style guides from `assets/code_styleguides/` to the project root at `conductor/code_styleguides/`.
1. **Asset Constraint:** You MUST ONLY propose and copy guides from `./assets/code_styleguides/`. Do NOT generate style rules from scratch.
2. **Recommendation:** Propose guides based on the Tech Stack confirmed in 2.3.
3. **Selection Mode:**
   - **Brownfield:** Propose matching guides and ask if additional ones are needed.
   - **Greenfield:** Present recommended guides or allow hand-picking from the library.
4. **Refinement:** Ask if the user wants to add any specific custom rules to the selected guides.
5. **Copy Action:** Execute the copy command once the selection is confirmed.

### 2.5 Workflow Configuration (`workflow.md`)
Configure the operational rules for the project.
1. **Mode Selection:** Ask the user if they prefer the **Default** workflow (>80% coverage, per-task commits, Git Notes summaries) or to **Customize** it.
2. **Customization Flow (If selected):** Conduct a batched interview (Coverage, Commit Frequency, Summary Storage) and allow for a final tweak.
3. **Write Action:** Copy `assets/workflow.md` to `conductor/workflow.md` and apply user choices if customized.

### 2.6 Agent Skill Selection (Optional)
1. **Recommendation & Trust Model:**
    - Analyze the project context and recommend relevant skills from `assets/catalog.md`.
    - **Trust Disclosure:** For each recommendation, disclose the `Party` status:
        - **1p (Official):** Present as a verified, official Conductor skill.
        - **3p (Community):** Present as a third-party skill. You MUST warn the user: *"Warning: This is a third-party skill. It will be installed as a frozen version (commit <sha>) for your safety."*
2. **Installation:** To install a selected skill, you MUST use the provided Python script:
  `uv run scripts/install_skill.py --name <skill_name> --url <url> --commit <sha> --party <1p|3p>`
3. **Capability Activation:** Once installed, notify the user that the new skills are ready and ask them to perform any necessary actions required by their specific AI tool to refresh or enable these new capabilities.

### 2.7 System Protocol (`.protocol.md`)
- **Initialization:** Copy `assets/protocol.md` to the project root at `conductor/protocol.md` to establish the behavioral constraints for all future agent interactions.

## 3. The Handshake (Index Generation)
Create `conductor/index.md`. This is the **Single Source of Truth** for all tools. 

1. **Path Mapping:** Write the following exact structure, linking to the artifacts you created:
   ```markdown
   # Project Context

   ## Definition
   - [Product Definition](./product.md)
   - [Product Guidelines](./product-guidelines.md)
   - [Tech Stack](./tech-stack.md)

   ## Workflow
   - [Workflow](./workflow.md)
   - [Code Style Guides](./code_styleguides/)
   - [System Protocol](./protocol.md)
   ```
2. **Integrity Check:** You MUST verify the existence of all linked files on disk.
3. **Commit Stage:** Stage the entire `conductor/` directory. Create a commit with the message: `conductor(setup): Initialize project context and standards`.

## 4. Completion
Once the `conductor/` directory is created and the index is generated, announce that setup is complete. 

**Next Steps:**
1. **Summary:** Present a final summary of the initialized scaffolding.
2. **Proactive Suggestion:** Ask the user if they would like to start defining their first actionable task (feature or bug fix) right now.
3. **Internal Handoff:** If the user agrees, you MUST use the `conductor-new-track` skill to begin planning.

## Guiding Principles
- **Fidelity:** Ensure the `workflow.md` matches the user's specific development culture.
- **Git Integrity:** Never leave the `conductor/` directory in an uncommitted state.
