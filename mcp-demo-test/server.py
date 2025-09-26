from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP("GitHelper")

REPO_PATH = r"C:\Users\shubu\Desktop\MCP"  # your repo path

@mcp.tool()
def push_to_github(commit_message: str = "auto commit") -> str:
    """Stage, commit, and push local changes to GitHub."""
    try:
        subprocess.run(["git", "add", "."], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=REPO_PATH, check=True)
        return "✅ Code pushed to GitHub!"
    except subprocess.CalledProcessError as e:
        return f"⚠️ Git error: {e}"