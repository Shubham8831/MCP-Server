from mcp.server.fastmcp import FastMCP
import subprocess
import os
import sys

# Initialize the MCP server
mcp = FastMCP("GitHelper5")

# Configuration - make this configurable
REPO_PATH = r"C:\Users\shubu\Desktop\MCP"  # your repo path

@mcp.tool()
def push_to_github(commit_message: str = "auto commit") -> str:
    """
    Stage, commit, and push local changes to GitHub.
    
    Args:
        commit_message: The commit message to use (default: "auto commit")
    
    Returns:
        str: Success message or error details
    """
    try:
        # Check if the repository path exists
        if not os.path.exists(REPO_PATH):
            return f"❌ Error: Repository path does not exist: {REPO_PATH}"
        
        # Change to the repository directory
        os.chdir(REPO_PATH)
        
        # Check if it's a git repository
        if not os.path.exists(os.path.join(REPO_PATH, '.git')):
            return f"❌ Error: Not a git repository: {REPO_PATH}"
        
        # Stage all changes
        result1 = subprocess.run(
            ["git", "add", "."], 
            cwd=REPO_PATH, 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if there are any changes to commit
        status_result = subprocess.run(
            ["git", "status", "--porcelain"], 
            cwd=REPO_PATH, 
            capture_output=True, 
            text=True
        )
        
        if not status_result.stdout.strip():
            return "ℹ️ No changes to commit."
        
        # Commit changes
        result2 = subprocess.run(
            ["git", "commit", "-m", commit_message], 
            cwd=REPO_PATH, 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        # Push to origin main
        result3 = subprocess.run(
            ["git", "push", "-u", "origin", "main"], 
            cwd=REPO_PATH, 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        return "✅ Code pushed to GitHub!"
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode('utf-8') if e.stderr else str(e)
        return f"❌ Git error: {error_msg}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

@mcp.tool()
def git_status() -> str:
    """
    Check the current git status of the repository.
    
    Returns:
        str: Git status information
    """
    try:
        if not os.path.exists(REPO_PATH):
            return f"❌ Error: Repository path does not exist: {REPO_PATH}"
        
        result = subprocess.run(
            ["git", "status", "--short"], 
            cwd=REPO_PATH, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        if not result.stdout.strip():
            return "✅ Working tree clean - no changes to commit."
        
        return f"📋 Git Status:\n{result.stdout}"
        
    except subprocess.CalledProcessError as e:
        return f"❌ Git error: {e.stderr.decode('utf-8') if e.stderr else str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def set_repo_path(new_path: str) -> str:
    """
    Update the repository path.
    
    Args:
        new_path: The new path to the git repository
    
    Returns:
        str: Confirmation message
    """
    global REPO_PATH
    
    if os.path.exists(new_path) and os.path.exists(os.path.join(new_path, '.git')):
        REPO_PATH = new_path
        return f"✅ Repository path updated to: {REPO_PATH}"
    else:
        return f"❌ Invalid repository path: {new_path}"

# Test function
def test_mcp_server():
    """
    Test function to verify the MCP server tools work correctly.
    """
    print("🧪 Testing MCP Server Tools...")
    print("=" * 50)
    
    # Test 1: Check current git status
    print("Test 1: Checking git status...")
    status_result = git_status()
    print(f"Result: {status_result}")
    print()
    
    # Test 2: Test repository path validation
    print("Test 2: Testing repository path...")
    if os.path.exists(REPO_PATH):
        print(f"✅ Repository path exists: {REPO_PATH}")
    else:
        print(f"❌ Repository path does not exist: {REPO_PATH}")
    
    if os.path.exists(os.path.join(REPO_PATH, '.git')):
        print("✅ Git repository detected")
    else:
        print("❌ Not a git repository")
    print()
    
    # Test 3: Test push function (dry run)
    print("Test 3: Testing push function...")
    push_result = push_to_github("Test commit from MCP server")
    print(f"Result: {push_result}")
    print()
    
    print("🏁 Testing completed!")

def main():
    """
    Main function to run the MCP server or tests.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Run tests
        test_mcp_server()
    else:
        # Run the MCP server
        print(f"🚀 Starting MCP Server 'GitHelper'...")
        print(f"📁 Repository path: {REPO_PATH}")
        print("Available tools:")
        print("  - push_to_github: Stage, commit, and push changes")
        print("  - git_status: Check repository status")
        print("  - set_repo_path: Update repository path")
        print("\nTo test the tools, run: python server.py --test")
        print("=" * 50)
        
        # Run the FastMCP server
        mcp.run()

if __name__ == "__main__":
    main()