# /// script
# dependencies = []
# ///
#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil
import argparse

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e.stderr.decode() if e.stderr else e}", file=sys.stderr)
        sys.exit(1)

def install_conductor(use_local, target_agent):
    print("🚂 Welcome to the Conductor Bootstrapper!")
    
    home_dir = os.path.expanduser("~")
    
    # 1. Determine Paths
    if use_local:
        print("Scope: PROJECT (./)")
        skills_dir = os.path.abspath(".agents/skills")
        rules_dir = os.path.abspath(".cursor/rules")
    else:
        print("Scope: GLOBAL (~/)")
        skills_dir = os.path.join(home_dir, ".agents", "skills")
        rules_dir = os.path.join(home_dir, ".cursor", "rules")

    print(f"Agent: {target_agent.upper()}")

    temp_repo_path = os.path.join(skills_dir, "_temp_conductor_repo")
    repo_url = "https://github.com/moisgobg/conductor-skills.git"

    # 2. Cleanup & Prep
    if os.path.exists(temp_repo_path):
        shutil.rmtree(temp_repo_path)
    os.makedirs(skills_dir, exist_ok=True)

    # 3. Download
    print(f"Downloading framework from {repo_url}...")
    run_command(f"git clone --depth 1 {repo_url} {temp_repo_path}")

    # 4. Install Core Skills
    source_skills_dir = os.path.join(temp_repo_path, "skills")
    print("\nCopying core skills:")
    for skill_folder in os.listdir(source_skills_dir):
        source_path = os.path.join(source_skills_dir, skill_folder)
        target_path = os.path.join(skills_dir, skill_folder)
        
        if os.path.isdir(source_path):
            if os.path.exists(target_path):
                print(f"  - Updating {skill_folder}...")
                shutil.rmtree(target_path)
            else:
                print(f"  - Installing {skill_folder}...")
            shutil.copytree(source_path, target_path)

    # 5. Agent-specific configuration
    if target_agent == "antigravity":
        print("\nApplying Antigravity compatibility rules...")
        os.makedirs(rules_dir, exist_ok=True)
        source_rule = os.path.join(temp_repo_path, "rules", "antigravity.md")
        target_rule = os.path.join(rules_dir, "conductor-compatibility.mdc")
        
        if os.path.exists(source_rule):
            shutil.copy2(source_rule, target_rule)
            print(f"  - Installed adapter rule to {target_rule}")
        else:
            print(f"  ! Warning: Could not find {source_rule} in repository.")
    
    elif target_agent == "gemini":
        print("\nGemini CLI detected: Skills are natively compatible.")

    # 6. Final Cleanup
    shutil.rmtree(temp_repo_path)
    
    print(f"\n✅ Conductor installed successfully!")
    print(f"Location: {skills_dir}")
    print("\nTo start, run:")
    print("> 'Run conductor-setup'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conductor Framework Bootstrapper")
    parser.add_argument("--project", action="store_true", help="Install into the current directory scope")
    parser.add_argument("--agent", choices=["gemini", "antigravity"], default="gemini", help="Target agent platform")
    
    args = parser.parse_args()
    install_conductor(args.project, args.agent)
