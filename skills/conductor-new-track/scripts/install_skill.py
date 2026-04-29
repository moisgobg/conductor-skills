# /// script
# dependencies = []
# ///
#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
import shutil
import re

def run_command(command, cwd=None):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def parse_github_url(url):
    """
    Parses a GitHub URL (raw or tree) to extract repo URL and subfolder path.
    Example: https://raw.githubusercontent.com/firebase/agent-skills/main/skills/firebase-ai-logic-basics/
    Repo: https://github.com/firebase/agent-skills.git
    Path: skills/firebase-ai-logic-basics
    """
    # Handle raw content URLs
    raw_match = re.match(r"https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.*)", url)
    if raw_match:
        owner, repo, branch, path = raw_match.groups()
        repo_url = f"https://github.com/{owner}/{repo}.git"
        return repo_url, branch, path.strip("/")

    # Handle standard web URLs
    web_match = re.match(r"https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.*)", url)
    if web_match:
        owner, repo, branch, path = web_match.groups()
        repo_url = f"https://github.com/{owner}/{repo}.git"
        return repo_url, branch, path.strip("/")

    return None, None, None

def install_skill(name, url, commit=None):
    # Always install to Workspace tier (Local) in the new modular architecture
    base_path = os.path.abspath('.agents/skills/')
    install_path = os.path.join(base_path, name)
    
    if os.path.exists(install_path):
        print(f"Skill '{name}' already exists at {install_path}. Updating...")
        shutil.rmtree(install_path)
    
    os.makedirs(base_path, exist_ok=True)
    
    repo_url, branch, subfolder = parse_github_url(url)
    
    if repo_url and subfolder:
        print(f"Detected GitHub repository: {repo_url}")
        print(f"Target subfolder: {subfolder}")
        
        temp_clone_path = os.path.join(base_path, f"_temp_{name}")
        if os.path.exists(temp_clone_path):
            shutil.rmtree(temp_clone_path)
            
        print(f"Cloning {repo_url}...")
        run_command(f"git clone --filter=blob:none --no-checkout {repo_url} {temp_clone_path}")
        
        target_ref = commit if commit else branch
        print(f"Setting up sparse-checkout for {subfolder} at {target_ref}...")
        
        run_command(f"git sparse-checkout set {subfolder}", cwd=temp_clone_path)
        run_command(f"git checkout {target_ref}", cwd=temp_clone_path)
        
        # Move the specific skill folder to the final destination
        skill_source = os.path.join(temp_clone_path, subfolder)
        shutil.move(skill_source, install_path)
        
        # Cleanup temp clone
        shutil.rmtree(temp_clone_path)
    else:
        # Fallback: Treat as a direct file copy if it's a local path
        if os.path.isdir(url):
            print(f"Copying local skill from {url}...")
            shutil.copytree(url, install_path)
        else:
            print(f"URL format not fully recognized for automated folder download: {url}", file=sys.stderr)
            print("Please ensure the URL is a GitHub folder or a local directory.", file=sys.stderr)
            sys.exit(1)

    print(f"Successfully installed skill '{name}' to {install_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install an Agent Skill deterministically (Optimized for uv).")
    parser.add_argument("--name", required=True, help="Name of the skill")
    parser.add_argument("--url", required=True, help="URL or path to the skill folder")
    parser.add_argument("--commit", help="Specific commit SHA to use")
    parser.add_argument("--party", choices=['1p', '3p'], default='1p', help="Trust level: 1p (official) or 3p (third-party)")

    args = parser.parse_args()
    
    if args.party == '3p' and not args.commit:
        print("SECURITY ERROR: Third-party skills (3p) MUST provide a --commit hash for deterministic installation.", file=sys.stderr)
        sys.exit(1)
        
    install_skill(args.name, args.url, args.commit)
