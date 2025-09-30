import asyncio
import os
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool

from agent_config import (
    MODEL_NAME,
    PRIMARY_SYSTEM_MESSAGE,
    CRITIC_SYSTEM_MESSAGE,
    RESEARCHER_SYSTEM_MESSAGE,
    MARKDOWN_SYSTEM_MESSAGE,
    PRESENTATION_SYSTEM_MESSAGE,
    TERMINATION_PHRASE,
    SELECTOR_PROMPT,
)


import subprocess
import sys
from pathlib import Path

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'  # End color

def generate_presentation(markdown: str, out_path: str = "out.pptx") -> str:
    """Generate a PowerPoint using Pandoc.

    Equivalent to running: pandoc example.md -o out.pptx --reference-doc=template.pptx

    Args:
        markdown: The Markdown content to convert (as a single string).
        out_path: Path where the PPTX should be written.
    Returns:
        A human-readable status string indicating success or the error output.
    """

    out_file = Path(out_path)
    md_file = out_file.with_suffix(".md")

    # Ensure the directory for the output file exists
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # Write Markdown to a file for Pandoc input
    try:
        md_file.write_text(markdown, encoding="utf-8")
    except Exception as e:
        return f"Failed to write Markdown to {md_file}: {e}"

    # Always use template.pptx as reference PPTX template
    template_flag = ["--reference-doc=template.pptx"]

    cmd = ["pandoc", str(md_file), "-o", str(out_file)] + template_flag
    try:
        result = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            cwd=str(Path(__file__).parent),
            check=False,
        )
    except Exception as e:
        return f"Failed to execute Pandoc: {e}"

    if result.returncode != 0:
        return (
            "Pandoc failed (code {}): {}".format(
                result.returncode,
                (result.stderr or result.stdout).strip()
            )
        )

    if out_file.exists():
        size = out_file.stat().st_size
        return f"Presentation generated at {out_file} ({size} bytes). Markdown saved to {md_file}."
    else:
        return "Pandoc reported success but output file not found."


async def main():
    # Load environment variables
    load_dotenv()

    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    # Create an OpenAI model client
    model_client = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=api_key
    )

    presentation_generator_tool = FunctionTool(generate_presentation, description="Generate a PowerPoint (.pptx) from provided Markdown content.")


    primary_agent = AssistantAgent(
        "primary",
        model_client=model_client,
        system_message=PRIMARY_SYSTEM_MESSAGE
    )

    critic_agent = AssistantAgent(
        "critic",
        model_client=model_client,
        system_message=CRITIC_SYSTEM_MESSAGE,
    )

    researcher_agent = AssistantAgent(
        "researcher",
        model_client=model_client,
        system_message=RESEARCHER_SYSTEM_MESSAGE,
    )

    markdown_agent = AssistantAgent(
        "markdown_generator",
        model_client=model_client,
        system_message=MARKDOWN_SYSTEM_MESSAGE,
    )

    presentation_agent = AssistantAgent(
        "presentation_generator",
        model_client=model_client,
        system_message=PRESENTATION_SYSTEM_MESSAGE,
        tools=[presentation_generator_tool],
    )

    # Define termination condition here using value from agent_config
    termination = TextMentionTermination(TERMINATION_PHRASE)

    # Create a team with the agents
    team = SelectorGroupChat(
        [primary_agent, researcher_agent, critic_agent, markdown_agent, presentation_agent],
        model_client=model_client,
        termination_condition=termination,
        selector_prompt=SELECTOR_PROMPT,
        allow_repeated_speaker=False,# Disallow an agent to speak multiple turns in a row.
    )

    # This is just for custom message logging, for default logging just do
    # await Console(team.run_stream(task="Is hawaii real pizza"))

    topic = "Is hawaii real pizza"
    print(f"\n{Colors.BLUE}=== Autogen Demo: Multi-Agent PPTX Generator ==={Colors.ENDC}")
    print(f"{Colors.BLUE}Topic: {topic}{Colors.ENDC}")
    print(f"{Colors.BLUE}="*80 + f"{Colors.ENDC}\n")

    # Always stream so users can see live progress
    print(f"{Colors.BLUE}[info] Streaming conversation...{Colors.ENDC}", flush=True)
    async for msg in team.run_stream(task=topic):
        author = getattr(msg, "source", None) or getattr(msg, "sender", None) or getattr(msg, "name", None) or getattr(msg, "role", None) or "agent"
        content = getattr(msg, "content", None)
        if content is None:
            try:
                # Some SDKs wrap text in .body or .text
                content = getattr(msg, "body", None) or getattr(msg, "text", None) or str(msg)
            except Exception:
                content = str(f"{Colors.RED}{msg}{Colors.ENDC}")
        sep = "=" * 80
        # print(sep, flush=True)
        print(f"\n{Colors.BLUE}[{author}] {sep}{Colors.ENDC}\n", flush=True)
        print(content, flush=True)

    print(f"\n{Colors.GREEN}=== Done ==={Colors.ENDC}")


if __name__ == "__main__":
    # Use asyncio.run() when running in a script
    asyncio.run(main())


