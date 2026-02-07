import os
import sys
import subprocess
import re
import shlex
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python call.py <tool_name> [args...]")
        sys.exit(1)

    tool_name = sys.argv[1]
    raw_args = sys.argv[2:]

    # --- Step 1: Resolve Operational Metadata (Business Scoping) ---
    metadata = {}
    tools_md_path = os.path.join(os.getcwd(), 'TOOLS.md')
    if os.path.exists(tools_md_path):
        with open(tools_md_path, 'r') as f:
            content = f.read()
            patterns = {
                'teamId': r'CLICKUP_TEAM_ID[:=]\s*([^\s\n]+)',
                'listId': r'CLICKUP_OPERATIONS_LIST_ID[:=]\s*([^\s\n]+)'
            }
            for key, p in patterns.items():
                match = re.search(p, content)
                if match:
                    metadata[key] = match.group(1).strip()

    # --- Step 2: Resolve Security Credentials (System Scoping) ---
    # Injected by OpenClaw from skills.entries.clickup-project-management.env
    env_vars = {}
    for key in ['CLICKUP_API_KEY', 'CLICKUP_TEAM_ID', 'CLICKUP_MCP_LICENSE_KEY', 'ENABLED_TOOLS']:
        val = os.getenv(key)
        if val:
            env_vars[key] = val

    # --- Step 3: Execution Logic ---
    # Use a local mcporter config for this specific agent to ensure true multi-user isolation
    # and prevent race conditions in concurrent multi-agent environments.
    local_config = os.path.join(os.getcwd(), '.mcporter.json')
    
    # Priority 1: Remote HTTP Version (High Performance)
    remote_url = "https://clickup-mcp.taazkareem.com/mcp"
    server_name = os.getenv('CLICKUP_MCP_SERVER_NAME', 'clickup-project-management')
    
    if env_vars.get('CLICKUP_API_KEY'):
        try:
            # Sync mcporter config for the remote server with correct headers
            config_cmd = [
                'mcporter', 'config', 'add', server_name,
                '--config', local_config,
                '--url', remote_url,
                '--header', f'X-ClickUp-Key={env_vars["CLICKUP_API_KEY"]}',
                '--header', f'X-ClickUp-Team-Id={env_vars.get("CLICKUP_TEAM_ID", "")}',
                '--header', f'X-License-Key={env_vars.get("CLICKUP_MCP_LICENSE_KEY", "")}',
                '--header', 'accept=application/json, text/event-stream',
                '--yes'
            ]
            
            # Add token optimization header
            if env_vars.get('ENABLED_TOOLS'):
                config_cmd.extend(['--header', f'X-Enabled-Tools={env_vars["ENABLED_TOOLS"]}'])
            
            subprocess.run(config_cmd, capture_output=True, check=True)
            
            # Call the tool using the local config
            cmd = ['mcporter', 'call', server_name, '--config', local_config, tool_name]
            
            # Auto-inject operational metadata as tool arguments if missing
            current_arg_keys = [a.split('=')[0] for a in raw_args if '=' in a]
            for m_key, m_val in metadata.items():
                if m_key not in current_arg_keys:
                    cmd.append(f"{m_key}={m_val}")
            
            cmd.extend(raw_args)
            
            print(f"Executing (Remote): {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout)
                sys.exit(0)
            else:
                print(f"Remote failed, falling back to local...")
        except Exception as e:
            # Silent fallback to stdio on configuration failure
            pass

    # Priority 2: Standard stdio fallback (The "Agnostic" Path)
    cmd = ['mcporter', 'call', '--stdio', 'npx -y @taazkareem/clickup-mcp-server', '--config', local_config]
    
    # Inject standard ClickUp environment variables from the agent environment
    for k, v in env_vars.items():
        cmd.extend(['--env', f'{k}={v}'])

    cmd.append(tool_name)
    
    # Inject metadata as arguments
    current_arg_keys = [a.split('=')[0] for a in raw_args if '=' in a]
    for m_key, m_val in metadata.items():
        if m_key not in current_arg_keys:
            cmd.append(f"{m_key}={m_val}")
    
    cmd.extend(raw_args)

    print(f"Executing (Local): {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
            sys.exit(result.returncode)
    except Exception as e:
        print(f"Execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
