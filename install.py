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

def install_conductor(use_local):
    print("🚂 Welcome to the Conductor Bootstrapper!")
    
    if use_local:
        install_dir = os.path.abspath(".agents/skills")
        print("Installing Conductor into PROJECT scope (./.agents/skills/)...")
    else:
        home_dir = os.path.expanduser("~")
        install_dir = os.path.join(home_dir, ".agents", "skills")
        print("Installing Conductor into GLOBAL scope (~/.agents/skills/)...")

    temp_repo_path = os.path.join(install_dir, "_temp_conductor_repo")
    repo_url = "https://github.com/moisgobg/conductor-skills.git"

    # 1. Clean up
    if os.path.exists(temp_repo_path):
        shutil.rmtree(temp_repo_path)
    os.makedirs(install_dir, exist_ok=True)

    # 2. Shallow Clone
    print(f"Downloading framework from {repo_url}...")
    run_command(f"git clone --depth 1 {repo_url} {temp_repo_path}")

    # 3. Install Skills
    source_skills_dir = os.path.join(temp_repo_path, "skills")
    print("\nCopying core skills:")
    for skill_folder in os.listdir(source_skills_dir):
        source_path = os.path.join(source_skills_dir, skill_folder)
        target_path = os.path.join(install_dir, skill_folder)
        
        if os.path.isdir(source_path):
            if os.path.exists(target_path):
                print(f"  - Updating {skill_folder}...")
                shutil.rmtree(target_path)
            else:
                print(f"  - Installing {skill_folder}...")
            shutil.copytree(source_path, target_path)

    # 4. Cleanup
    shutil.rmtree(temp_repo_path)
    
    print(f"\n✅ Conductor Core Skills installed successfully in {'local project' if use_local else 'global'} environment!")
    print("\nTo initialize a project, navigate to your root and ask your Agent:")
    print("> 'Run conductor-setup'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conductor Framework Bootstrapper")
    parser.add_argument("--project", action="store_true", help="Install into the current project directory (./.agents/skills/)")
    
    args = parser.parse_args()
    install_conductor(args.project)
