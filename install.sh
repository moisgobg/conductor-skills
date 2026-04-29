#!/bin/bash

# Conductor Framework Bootstrapper (Unix/macOS)
set -e

# Default values
PROJECT_SCOPE=false
AGENT="gemini"
INSTALL_DIR=""
RULES_DIR=""

# Helper: Print usage
print_usage() {
  echo "Usage: ./install.sh [options]"
  echo ""
  echo "Options:"
  echo "  --project    Install into the current directory scope (./.agents/skills/)"
  echo "  --agent      Target agent platform (gemini|antigravity) [default: gemini]"
  echo "  --help       Show this help message"
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --project) PROJECT_SCOPE=true ;;
    --agent) AGENT="$2"; shift ;;
    --help) print_usage; exit 0 ;;
    *) echo "Unknown parameter passed: $1"; print_usage; exit 1 ;;
  esac
  shift
done

echo "🚂 Welcome to the Conductor Bootstrapper!"

# 1. Determine Paths
if [ "$PROJECT_SCOPE" = true ]; then
  echo "Scope: PROJECT (./)"
  INSTALL_DIR="$(pwd)/.agents/skills"
  RULES_DIR="$(pwd)/.agents/rules"
else
  echo "Scope: GLOBAL (~/)"
  if [ "$AGENT" = "antigravity" ]; then
    INSTALL_DIR="$HOME/.gemini/antigravity/skills"
    RULES_DIR="$HOME/.gemini"
  else
    INSTALL_DIR="$HOME/.agents/skills"
    # Gemini CLI rules folder (if applicable)
    RULES_DIR="$HOME/.agents/rules"
  fi
fi

echo "Agent: ${AGENT^^}"

REPO_URL="https://github.com/moisgobg/conductor-skills.git"
TEMP_REPO_PATH="$INSTALL_DIR/_temp_conductor_repo"

# 2. Cleanup & Prep
if [ -d "$TEMP_REPO_PATH" ]; then
  rm -rf "$TEMP_REPO_PATH"
fi
mkdir -p "$INSTALL_DIR"

# 3. Download
echo "Downloading framework from $REPO_URL..."
git clone --depth 1 "$REPO_URL" "$TEMP_REPO_PATH" > /dev/null 2>&1

# 4. Install Core Skills
echo -e "\nCopying core skills:"
SOURCE_SKILLS_DIR="$TEMP_REPO_PATH/skills"

for skill in "$SOURCE_SKILLS_DIR"/*/; do
  skill_name=$(basename "$skill")
  target_path="$INSTALL_DIR/$skill_name"
  
  if [ -d "$target_path" ]; then
    echo "  - Updating $skill_name..."
    rm -rf "$target_path"
  else
    echo "  - Installing $skill_name..."
  fi
  cp -r "$skill" "$target_path"
done

# 5. Agent-specific configuration
if [ "$AGENT" = "antigravity" ]; then
  echo -e "\nApplying Antigravity compatibility rules..."
  mkdir -p "$RULES_DIR"
  SOURCE_RULE="$TEMP_REPO_PATH/rules/antigravity.md"
  
  if [ "$PROJECT_SCOPE" = true ]; then
    TARGET_RULE="$RULES_DIR/conductor-compatibility.md"
  else
    # For Global Scope, we append/write to GEMINI.md as per Antigravity docs
    TARGET_RULE="$RULES_DIR/GEMINI.md"
  fi
  
  if [ -f "$SOURCE_RULE" ]; then
    if [ "$PROJECT_SCOPE" = true ]; then
      cp "$SOURCE_RULE" "$TARGET_RULE"
      echo "  - Installed adapter rule to $TARGET_RULE"
    else
      # Append to GEMINI.md if it exists, or create it
      echo -e "\n" >> "$TARGET_RULE" 2>/dev/null || true
      cat "$SOURCE_RULE" >> "$TARGET_RULE"
      echo "  - Added adapter rule to $TARGET_RULE"
    fi
  else
    echo "  ! Warning: Could not find $SOURCE_RULE in repository."
  fi
elif [ "$AGENT" = "gemini" ]; then
  echo -e "\nGemini CLI detected: Skills are natively compatible."
fi

# 6. Final Cleanup
rm -rf "$TEMP_REPO_PATH"

echo -e "\n✅ Conductor installed successfully!"
echo "Location: $INSTALL_DIR"
echo -e "\nTo start, run:"
echo "> 'Run conductor-setup'"
