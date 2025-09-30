# =============================================================================
#  Filename: crew.py
#
#  Short Description: CrewAI workflow orchestration for NVIDIA newsletter
#
#  Creation date: 2025-09-30
#  Author: Shrinivas Deshpande
# =============================================================================

import os
from typing import Any

from crewai import Crew, LLM, Process
from loguru import logger

from NewsLetter2.agents import (
    create_editor_agent,
    create_reporter_agent,
    create_senior_editor_agent,
)
from NewsLetter2.tasks import (
    create_editor_task,
    create_reporter_task,
    create_senior_editor_task,
)


def create_newsletter_crew() -> Crew:
    """
    Create and configure the complete NVIDIA newsletter crew.
    
    Orchestrates three agents (Reporter, Editor, Senior Editor) in a sequential
    workflow to collect, summarize, analyze, and package NVIDIA news into
    a professional newsletter format.
    
    Returns:
        Configured Crew instance ready for execution
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment")
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    # Configure LLM using CrewAI's LLM class
    llm = LLM(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=api_key,
    )
    
    # Create agents
    reporter = create_reporter_agent(llm)
    editor = create_editor_agent(llm)
    senior_editor = create_senior_editor_agent(llm)
    
    # Create tasks with dependencies
    reporter_task = create_reporter_task(reporter)
    editor_task = create_editor_task(editor, reporter_task)
    senior_editor_task = create_senior_editor_task(senior_editor, editor_task)
    
    # Assemble crew
    crew = Crew(
        agents=[reporter, editor, senior_editor],
        tasks=[reporter_task, editor_task, senior_editor_task],
        process=Process.sequential,
        verbose=True,
    )
    
    logger.info("NVIDIA Newsletter Crew assembled successfully")
    return crew


def run_newsletter_generation() -> dict[str, Any]:
    """
    Execute the complete newsletter generation workflow.
    
    Runs the crew to collect NVIDIA news, summarize articles, write editorial,
    and produce a complete newsletter package. Results are automatically cached.
    
    Returns:
        Dictionary containing the final newsletter with editorial and articles
    """
    from NewsLetter2.cache_manager import cache_manager
    from NewsLetter2.models import Newsletter
    import json
    from pathlib import Path
    
    logger.info("Starting NVIDIA newsletter generation...")
    
    crew = create_newsletter_crew()
    result = crew.kickoff()
    
    logger.info("Newsletter generation completed")
    
    # Try to save to cache
    try:
        # Load from the output file to get clean data
        output_file = Path("newsletter_output.json")
        if output_file.exists():
            with open(output_file) as f:
                content = f.read()
                
            # Clean markdown fences
            if content.startswith('```json'):
                content = content[7:]
            elif content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            data = json.loads(content)
            newsletter = Newsletter(**data)
            
            # Save to cache
            cache_manager.save_to_cache(newsletter)
            logger.success("Newsletter saved to cache")
    except Exception as e:
        logger.warning(f"Could not save to cache: {e}")
    
    return result
