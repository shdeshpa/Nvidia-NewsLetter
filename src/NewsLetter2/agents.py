# =============================================================================
#  Filename: agents.py
#
#  Short Description: CrewAI agent definitions for NVIDIA newsletter generation
#
#  Creation date: 2025-09-30
#  Author: Shrinivas Deshpande
# =============================================================================

from typing import Any

from crewai import Agent
from loguru import logger

from NewsLetter2.tools import search_nvidia_news


def create_reporter_agent(llm: Any) -> Agent:
    """
    Create Reporter agent for collecting NVIDIA news.
    
    The Reporter uses SerpAPI to gather the 10 latest NVIDIA-related
    AI and technology news articles from various sources.
    
    Args:
        llm: Language model instance (OpenAI configured)
        
    Returns:
        Configured Reporter Agent with SerpAPI tool
    """
    agent = Agent(
        role="NVIDIA News Collector",
        goal=(
            "Search for the 10 latest NVIDIA AI and technology-related news articles. "
            "Focus on GPUs, AI platforms, enterprise adoption, partnerships, "
            "product launches, and financial/market impact."
        ),
        backstory=(
            "You are an expert tech journalist with deep knowledge of NVIDIA's "
            "ecosystem, AI hardware trends, and enterprise technology adoption. "
            "You have a keen eye for identifying significant news that matters "
            "to AI leaders, product managers, and technology decision-makers."
        ),
        tools=[search_nvidia_news],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    
    logger.info("Reporter agent created successfully")
    return agent


def create_editor_agent(llm: Any) -> Agent:
    """
    Create Editor agent for summarizing and analyzing news.
    
    The Editor reviews raw news articles and creates both concise summaries
    for the landing page and detailed analyses for individual article views.
    Tailored for AI enthusiasts, tech leaders, and product managers.
    
    Args:
        llm: Language model instance (OpenAI configured)
        
    Returns:
        Configured Editor Agent without additional tools (uses LLM directly)
    """
    agent = Agent(
        role="AI & Tech News Summarizer",
        goal=(
            "Review each of the 10 news articles and write: "
            "(1) A clear, engaging 2-3 sentence summary for the landing page, "
            "(2) A detailed 20-30 sentence article highlighting implications for "
            "AI adoption, enterprise strategy, product management, and NVIDIA's market influence."
        ),
        backstory=(
            "You are a senior technology editor with expertise in AI, semiconductors, "
            "and enterprise technology. You excel at distilling complex technical news "
            "into clear, actionable insights for business and product leaders. "
            "Your summaries are known for being professional, insightful, and highly "
            "relevant to strategic decision-making."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    
    logger.info("Editor agent created successfully")
    return agent


def create_senior_editor_agent(llm: Any) -> Agent:
    """
    Create Senior Editor agent for validation and editorial writing.
    
    The Senior Editor verifies accuracy, writes the front-page editorial,
    analyzes trends, compares NVIDIA with competitors, and provides
    strategic insights for product leaders.
    
    Args:
        llm: Language model instance (OpenAI configured)
        
    Returns:
        Configured Senior Editor Agent
    """
    agent = Agent(
        role="Editorial Writer & Verifier",
        goal=(
            "Verify accuracy and coherence of news summaries, then write an 800-1000 word "
            "editorial about NVIDIA's current position in the AI landscape. "
            "Include: (1) Clear narrative on NVIDIA's AI ecosystem role, "
            "(2) Trend analysis across the 10 stories, "
            "(3) 'What this means for product leaders' with actionable insights, "
            "(4) 'NVIDIA vs Competition' comparing with AMD, Intel, and hyperscalers."
        ),
        backstory=(
            "You are the chief technology analyst and editorial director with 15+ years "
            "covering semiconductor and AI industries. You have insider knowledge of "
            "NVIDIA, AMD, Intel, and cloud provider strategies. Your editorials are "
            "read by CTOs, product VPs, and investment analysts for their authoritative, "
            "strategic, and forward-looking perspectives on technology trends."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    
    logger.info("Senior Editor agent created successfully")
    return agent
