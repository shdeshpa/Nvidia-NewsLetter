# =============================================================================
#  Filename: tasks.py
#
#  Short Description: CrewAI task definitions for newsletter workflow
#
#  Creation date: 2025-09-30
#  Author: Shrinivas Deshpande
# =============================================================================

from crewai import Task
from loguru import logger

from NewsLetter2.agents import (
    create_editor_agent,
    create_reporter_agent,
    create_senior_editor_agent,
)


def create_reporter_task(reporter_agent) -> Task:
    """
    Create task for Reporter agent to collect NVIDIA news.
    
    Args:
        reporter_agent: The Reporter Agent instance
        
    Returns:
        Task configured for news collection via SerpAPI
    """
    task = Task(
        description=(
            "Use the SerpAPI tool to search for the 10 latest NVIDIA-related news articles. "
            "Focus on: AI developments, GPU technologies, enterprise adoption, partnerships, "
            "product launches, market movements, and competitive positioning. "
            "Return a structured list of articles with title, source, URL, snippet, "
            "thumbnail, and publication date."
        ),
        expected_output=(
            "A list of exactly 10 raw news articles about NVIDIA, each containing: "
            "title, source, url, snippet, thumbnail (if available), and published_date. "
            "Output should be in JSON format."
        ),
        agent=reporter_agent,
    )
    
    logger.info("Reporter task created")
    return task


def create_editor_task(editor_agent, reporter_task) -> Task:
    """
    Create task for Editor agent to summarize news articles.
    
    Args:
        editor_agent: The Editor Agent instance
        reporter_task: The Reporter task (for dependency chain)
        
    Returns:
        Task configured for article summarization and detailed writing
    """
    task = Task(
        description=(
            "Review the 10 NVIDIA news articles provided by the Reporter. "
            "For each article, write: "
            "1. A short_summary: 2-3 compelling sentences capturing the essence, "
            "   written for AI/tech leaders and product managers. "
            "2. A detailed_article: 20-30 sentences providing in-depth analysis, "
            "   covering implications for AI adoption, enterprise strategy, product "
            "   management, and NVIDIA's market influence. "
            "Maintain a professional, insightful tone that resonates with business "
            "decision-makers."
        ),
        expected_output=(
            "A list of 10 processed news articles, each with: title, source, url, "
            "thumbnail, short_summary (2-3 sentences), detailed_article (20-30 sentences), "
            "and published_date. Output in JSON format."
        ),
        agent=editor_agent,
        context=[reporter_task],
    )
    
    logger.info("Editor task created")
    return task


def create_senior_editor_task(senior_editor_agent, editor_task) -> Task:
    """
    Create task for Senior Editor to validate and write editorial.
    
    Args:
        senior_editor_agent: The Senior Editor Agent instance
        editor_task: The Editor task (for dependency chain)
        
    Returns:
        Task configured for validation, editorial writing, and trend analysis
    """
    task = Task(
        description=(
            "1. Verify the accuracy and coherence of all 10 summarized articles from the Editor. "
            "2. Write an 800-1000 word front-page editorial with the following sections: "
            "   - headline: Compelling title for the editorial "
            "   - narrative: Clear story about NVIDIA's current position in AI landscape "
            "   - trend_analysis: Patterns and themes across the 10 news stories "
            "   - product_leader_insights: Actionable recommendations for enterprise adoption, "
            "     product strategy, and market timing "
            "   - competition_analysis: Comparison of NVIDIA with AMD, Intel, and hyperscalers "
            "     (AWS, Azure, GCP) in terms of technology, market position, and strategy. "
            "Tone should be authoritative, strategic, and forward-looking."
        ),
        expected_output=(
            "A complete Newsletter object in JSON format containing: "
            "1. editorial: {headline, narrative, trend_analysis, product_leader_insights, "
            "   competition_analysis, image_url, created_at} "
            "2. articles: list of 10 validated ProcessedNewsArticle objects "
            "3. generated_at: timestamp "
            "4. edition_number: optional edition number"
        ),
        agent=senior_editor_agent,
        context=[editor_task],
        output_file="newsletter_output.json",
    )
    
    logger.info("Senior Editor task created")
    return task
