# ClickUp Project Management Skill for OpenClaw

This repository contains the `clickup-project-management` skill for OpenClaw, designed to work with the [ClickUp MCP Server - Premium](https://github.com/taazkareem/clickup-mcp-server).

## Installation

You can install this skill in OpenClaw via ClawHub or by running:

```bash
openclaw skills install https://github.com/taazkareem/clickup-project-management
```

## Features

- **High-Performance Orchestration**: Advanced task automation, hierarchy management, and team collaboration.
- **Context-Aware Scoping**: Automatically pulls `teamId` and `listId` from your workspace `TOOLS.md`.
- **Dynamic Tool Discovery**: Uses `mcporter` to expose the full ClickUp toolset (Tasks, Folders, Lists, Docs, Time, Chat).
- **Remote-First Execution**: Prioritizes low-latency remote execution with local `npx` fallback.

## Requirements

- [mcporter](https://mcporter.dev) installed (automatically handled by the skill).
- A valid ClickUp API Key.
- (Optional) ClickUp Team ID and MCP License Key.

## License

MIT
