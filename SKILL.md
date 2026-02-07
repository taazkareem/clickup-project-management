---
name: clickup-project-management
description: "A high-performance Skill for managing ClickUp via the Model Context Protocol (MCP). Orchestrate tasks, tags, lists, folders, files, docs, time, chat, and multi-step workflows using natural language."
metadata:
  {
    "openclaw":
      {
        "emoji": "🏗️",
        "requires": { "bins": ["mcporter", "python3"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter",
            },
          ],
      },
  }
---

# ClickUp Project Management Skill

This skill provides a high-performance interface for managing ClickUp. It is designed to be **context-aware**, automatically pulling `CLICKUP_TEAM_ID` and `CLICKUP_OPERATIONS_LIST_ID` from your `TOOLS.md` if available.

## Tool Discovery

To see all available tools and their required parameters, run:
`mcporter list clickup-project-management --schema`

## Usage

Always use the bundled launcher to execute tools. This ensures proper authentication, automatic scoping, and high-performance routing.

**Command Template:**
`python {baseDir}/scripts/call.py <TOOL_NAME> [ARGS]`

## Automatic Scoping

The launcher automatically checks your local `TOOLS.md` for the following keys:
- `CLICKUP_TEAM_ID`: Automatically injected as `teamId`.
- `CLICKUP_OPERATIONS_LIST_ID`: Automatically injected as `listId`.

This allows you to execute commands like `create_task name="Project Kickoff"` without manually providing IDs.

## Configuration

Requires `CLICKUP_API_KEY` to be set in your `openclaw.json` or process environment.
