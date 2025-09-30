# AutoGen Studio: Install and Run Guide

This guide shows how to install and launch AutoGen Studio in a separate, local environment. It is independent from running the demo in this repository and can be used to explore, design, and run multi‑agent workflows via a web UI.

Note: AutoGen Studio is an optional companion tool. You do not need it to run this demo, but it can be useful for prototyping and inspecting agent workflows.


## Prerequisites
- Windows, macOS, or Linux
- Python 3.10+ (3.11 recommended)
- A terminal with internet access
- Optional (depending on your models): provider API keys (e.g., OpenAI)

Tips:
- It’s best to install AutoGen Studio in its own virtual environment (venv) or via pipx to avoid dependency conflicts.


## Install (recommended via pip)
You can install AutoGen Studio globally (using pipx) or in a virtual environment (using pip).

Option A — pipx (isolated, global install):
- Install pipx if needed: https://pipx.pypa.io/latest/installation/
- Then:

  pipx install autogenstudio

Option B — pip (inside a virtual environment):
1) Create and activate a virtual environment.
   - Windows PowerShell:

     python -m venv .venv
     .\.venv\Scripts\Activate.ps1

   - macOS/Linux Bash:

     python3 -m venv .venv
     source .venv/bin/activate

2) Install:

   python -m pip install --upgrade pip
   python -m pip install autogenstudio

If you need all optional extras (e.g., more providers/integrations), you can try:

   python -m pip install "autogenstudio[all]"


## Launch the UI
After installation, start the Studio web app. Depending on your installation, one of the following commands should work. Try them in order:

- autogenstudio ui
- autogenstudio
- python -m autogenstudio ui

You can also specify host/port, for example:

  autogenstudio ui --host 127.0.0.1 --port 8081

When it starts, it will print a local URL (e.g., http://127.0.0.1:8081). Open that in your browser.


## Configure model provider keys
AutoGen Studio needs access to model provider APIs. Common ways to provide keys:

- Environment variables in your shell before launching:

  - Windows PowerShell:

        setx OPENAI_API_KEY "sk-..."
        # Close and reopen the terminal, then launch Studio

  - macOS/Linux Bash (session only):

        export OPENAI_API_KEY="sk-..."
        autogenstudio ui

- Or use a .env file in the directory where you launch Studio:

      OPENAI_API_KEY=sk-...

Notes:
- The exact variable names depend on providers. Examples: OPENAI_API_KEY, AZURE_OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.
- Restart Studio after changing environment variables.


## Using this project with Studio (optional)
- Studio is a general UI for AutoGen multi‑agent workflows. While this repository runs a scripted demo via main.py, you can prototype similar teams and prompts in Studio’s UI.
- The prompts and model name used here are in agent_config.py. You can copy/paste those into Studio when designing agents.


## Troubleshooting
- Command not found:
  - If autogenstudio is not recognized, try:

        python -m autogenstudio ui

  - If you used pipx, ensure the pipx bin directory is on your PATH (reopen your terminal after installing pipx).

- Port already in use:

      autogenstudio ui --port 8082

- Dependency conflicts in a global Python:
  - Prefer pipx or a clean virtual environment.

- Provider errors or 401/403:
  - Verify your API key, billing status, model name availability, and region (for Azure/OpenAI).

- Can’t reach the UI URL:
  - Firewalls or corporate proxies may block local ports. Try a different port or machine.


## Uninstall
- pipx:

      pipx uninstall autogenstudio

- pip (inside an active venv):

      python -m pip uninstall autogenstudio


---
If you encounter issues, consult the AutoGen Studio documentation or repository for the most up‑to‑date instructions and supported providers.