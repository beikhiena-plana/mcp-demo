# MCP Demo - TekTok

A high-performance [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server built with [FastMCP](https://gofastmcp.com/getting-started/welcome). This server allows Claude to safely diagnose issues and apply fixes to a specific project directory.

## Quick Start

### Prerequisites
* [**Python**](https://python.org)
* [**uv**](https://docs.astral.sh/uv/getting-started/installation)
* [**Nodejs**](https://nodejs.org/en)


## Local Setup
In the root project install all dependencies by running:
```bash
cd mcp_server
```
and run
```bash
uv sync
```
then run this to start the server locally:

```bash
uv run serve
```

or

```bash
uv run mcp_demo/server.py
```

To run `node_project` run:

Install `PNPM` or you coukd use `NPM` but I'm using pnpm here:
```bash
cd node_project
```
and run
```bash
pnpm install
```

then run:

```bash
pnpm dev
```

## Claude Desktop

To make the server discoverable to Claude Desktop, in the Developer section click the edit config button and update `claude_desktop_config.json` file as below:

```json
{
  "mcpServers": {
    "mcp-demo": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/Users/absolute-path-to-project/mcp-demo",
        "run",
        "mcp_demo/server.py"
      ]
    }
  }
}
```

## Inspection

To inspect the mcp server and see all primitives and other info run this:

```bash
npx @modelcontextprotocol/inspector uv run mcp_demo/server.py
```

## Server Primitives

#### Tools (Actions)
| Tool | Description |
| :--- | :--- |
| `list_project_files` | Recursively maps the `node-demo` structure (excludes node_modules/logs). |
| `list_available_logs` | Shows all `.log` files in the production log directory. |
| `read_project_file` | Reads source code from `node-demo` with path-safety verification. |
| `read_log_file` | Accesses specific log contents to identify stack traces. |
| `apply_fix` | Replaces file contents with a bug fix and returns a size-change report. |

#### Resources (Data)
| URI | Description |
| :--- | :--- |
| `logs://error.log` | Static resource for the primary production error log. |

#### Prompts (Personas)
| Prompt | Usage |
| :--- | :--- |
| `production_debug_prompt` | Sets Claude as a Senior Software Engineer; enforces a "Logs-First" debugging workflow. |

