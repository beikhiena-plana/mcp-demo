from pathlib import Path
from fastmcp import FastMCP

# ------------------------------------------------------------------------------
# MCP SERVER INITIALIZATION
# ------------------------------------------------------------------------------

mcp = FastMCP("mcp-demo")

# ------------------------------------------------------------------------------
# BASE DIRECTORIES
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.resolve()
# Points to projects/node_project
NODE_PROJECT_ROOT = (BASE_DIR.parent.parent / "node_project").resolve()
# Points to projects/node_project/logs
LOG_DIR = (NODE_PROJECT_ROOT / "logs").resolve()

# Ensure directories exist
LOG_DIR.mkdir(exist_ok=True)
NODE_PROJECT_ROOT.mkdir(exist_ok=True)

# ------------------------------------------------------------------------------
# RESOURCES - Static or semi static data
# ------------------------------------------------------------------------------

@mcp.resource("logs://error.log")
def get_error_log() -> str:
    """Static resource for the main error log"""
    path = (LOG_DIR / 'error.log').resolve()
    if not path.is_file() or LOG_DIR not in path.parents:
        raise ValueError("Invalid or unauthorized log file access")
    return path.read_text(encoding="utf-8", errors="ignore")

# ------------------------------------------------------------------------------
# TOOLS - Functions to perform actions on the server
# ------------------------------------------------------------------------------
@mcp.tool()
def list_available_logs() -> list[str]:
    """List all log files available in the logs directory."""
    return [f.name for f in LOG_DIR.glob("*.log")]

@mcp.tool()
def read_log_file(filename: str) -> str:
    """
    Read a production log file.
    Example resource URI: logs://app.log
    """
    path = (LOG_DIR / filename).resolve()

    #  Only allow access to file and specified folder
    if not path.is_file() or LOG_DIR not in path.parents:
        raise ValueError("Invalid or unauthorized log file access")

    return path.read_text(encoding="utf-8", errors="ignore")

@mcp.tool()
def read_project_file(filename: str) -> str:
    """Read a source file from the node_project project."""
    path = (NODE_PROJECT_ROOT / filename).resolve()
    if not path.is_file() or NODE_PROJECT_ROOT not in path.parents:
        raise ValueError("Invalid or unauthorized project file access")
    return path.read_text(encoding="utf-8", errors="ignore")

@mcp.tool()
def list_project_files() -> list[str]:
    """List all files in node_project, excluding node_modules and logs."""
    files = []
    exclude = {"node_modules", "logs", ".git", ".env", "pnpm-lock.yaml"}
    
    for p in NODE_PROJECT_ROOT.rglob("*"):
        # Check if any part of the path (folder names) is in our exclude list
        if p.is_file() and not any(part in exclude for part in p.parts):
            files.append(str(p.relative_to(NODE_PROJECT_ROOT)))
    return files

@mcp.tool()
def apply_fix(filepath: str, new_content: str, reason: str) -> str:
    """
    Apply a fix by fully replacing the contents of a file in node_project.
    """
    path = (NODE_PROJECT_ROOT / filepath).resolve()

    if not path.is_file() or NODE_PROJECT_ROOT not in path.parents:
        raise ValueError(f"Unauthorized or missing file: {filepath}")

    old_size = path.stat().st_size
    path.write_text(new_content, encoding="utf-8")
    new_size = len(new_content.encode("utf-8")) # Bytes size for accuracy

    return (
        f"Fix applied to {filepath}\n"
        f"Reason: {reason}\n"
        f"Size change: {old_size} -> {new_size} bytes."
    )

# ------------------------------------------------------------------------------
# PROMPTS - Template string for instructions
# ------------------------------------------------------------------------------

@mcp.prompt()
def production_debug_prompt() -> str:
    return """
You are an experienced senior software engineer with expert debugging skills. 
Your workspace is the 'node_project' project.

WORKFLOW:
1. Call 'list_project_files' to see the structure.
2. Read 'logs://error.log' to find stack traces and line numbers.
3. Read the failing file using read_project_file.
4. Use 'apply_fix' to resolve the bug once identified.

STRICT RULES:
- Never guess line numbers; read the logs first.
- Ensure the fix includes necessary error handling or variable checks.
- Explain your fix before applying it.
""".strip()

def run_server():
    # default transport layer is stdio
    mcp.run()

if __name__ == "__main__":
    run_server()

