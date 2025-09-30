# Autogen Demo: Multi‑Agent PPTX Generator

This project demonstrates a small multi‑agent workflow that:
- coordinates several agents (primary, researcher, critic, markdown generator, presentation generator),
- produces Markdown for slides,
- converts that Markdown into a PowerPoint file using Pandoc and a provided template (template.pptx).

The entry point is main.py. The agent settings live in agent_config.py.


## What it does
- You provide a topic via the hard‑coded task in main.py (you can change it).
- Agents collaborate to research, draft, review, and then turn Markdown into a .pptx deck.
- The presentation is rendered with Pandoc using template.pptx as the reference theme.
- The resulting files are written by default to:
  - out.pptx (the generated presentation)
  - out.md (the intermediate Markdown saved next to the PPTX)


## Prerequisites
- Windows, macOS, or Linux
- Python 3.10+ (3.11 recommended)
- Pandoc installed and available on PATH
  - Install: https://pandoc.org/installing.html (macOS: brew install pandoc; Linux: use your package manager or the official installer)
  - After installing, open a new terminal and run: pandoc --version
- An OpenAI API key


## Quick start (Windows PowerShell)
1) Clone this repository and open a PowerShell prompt in the project folder.

2) Create and activate a virtual environment:
   - Create: py -3.11 -m venv .venv
   - Activate: .\.venv\Scripts\Activate.ps1
   - If activation is blocked, start PowerShell "As Administrator" and run:
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

3) Install Python dependencies:
   - Install from requirements.txt:

     pip install --upgrade pip
     pip install -r requirements.txt

   This will install the Autogen components and helpers defined in requirements.txt (e.g., autogen-agentchat>=0.4.0, autogen-ext[openai]>=0.4.0, python-dotenv) and their transitive dependencies.

4) Install Pandoc (if not already):
   - Download and install from https://pandoc.org/installing.html
   - Confirm it works: pandoc --version

5) Provide your OpenAI API key:
   - Create a file named .env in the project root with the following content:

     OPENAI_API_KEY=sk-...your-key-here...

6) Run the demo:

   python .\main.py

   - The console will stream the multi‑agent conversation.
   - When finished, you should see out.pptx in the project root.


## Quick start (macOS/Linux Bash)
1) Clone this repository and open a terminal in the project folder.

2) Create and activate a virtual environment:
   - Create: python3 -m venv .venv
   - Activate: source .venv/bin/activate

3) Install Python dependencies from requirements.txt:

   python3 -m pip install --upgrade pip
   python3 -m pip install -r requirements.txt

4) Install Pandoc (if not already):
   - macOS (Homebrew): brew install pandoc
   - Debian/Ubuntu: sudo apt-get update && sudo apt-get install -y pandoc
   - Fedora: sudo dnf install -y pandoc
   - Or use the official installers: https://pandoc.org/installing.html
   - Confirm it works: pandoc --version

5) Provide your OpenAI API key:
   - EITHER create a .env file in the project root with:

     OPENAI_API_KEY=sk-...your-key-here...

   - OR export it in your shell before running:

     export OPENAI_API_KEY=sk-...your-key-here...

6) Run the demo:

   python3 ./main.py

   - The console will stream the multi-agent conversation.
   - When finished, you should see out.pptx in the project root.


## Configuration
- Agent prompts and model name are in agent_config.py.
- Default OpenAI model name: gpt-4o (adjust MODEL_NAME if needed).
- The presentation tool in main.py writes Markdown next to the PPTX and calls:
  pandoc <markdown-file> -o <out.pptx> --reference-doc=template.pptx


## Changing the topic
- In main.py, locate the team.run_stream(task=...) call and replace the example topic with your own prompt.


## Troubleshooting
- Module not found (autogen_…): Ensure you installed dependencies via `pip install -r requirements.txt` and you’re using the correct Python venv.
- Pandoc failed: Verify pandoc --version works in the same terminal. On Windows, reopen PowerShell after installing Pandoc to refresh PATH; on macOS/Linux, open a new terminal or re-source your shell config (e.g., source ~/.bashrc or exec $SHELL) so PATH updates take effect.
- OPENAI_API_KEY is required: Create the .env file as shown or export the variable in your shell before running.
- SSL or network issues: Try again from a different network or ensure corporate proxies are configured in your environment.