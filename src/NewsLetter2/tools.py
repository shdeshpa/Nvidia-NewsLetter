# =============================================================================
#  Filename: tools.py
#
#  Short Description: Custom tools for news collection using SerpAPI
#
#  Creation date: 2025-09-30
#  Author: Shrinivas Deshpande
# =============================================================================

import os
from typing import Any

from crewai.tools import tool
from loguru import logger
from serpapi import GoogleSearch


@tool("Search Latest NVIDIA AI News")
def search_nvidia_news(query: str = "NVIDIA AI GPU technology news") -> list[dict[str, Any]]:
    """
    Searches for the 10 latest NVIDIA AI and technology-related news articles.
    Focus areas: GPUs, AI platforms, enterprise adoption, partnerships,
    product launches, and financial/market impact.
    
    Args:
        query: Search query (default focuses on NVIDIA AI/GPU news)
        
    Returns:
        List of up to 10 raw news articles with title, source, URL, snippet,
        thumbnail, and publication date
    """
    api_key = os.getenv("SERP_API_KEY", "")
    
    if not api_key:
        logger.error("SERP_API_KEY not found in environment")
        raise ValueError("SERP_API_KEY environment variable is required")
    
    try:
        params = {
            "engine": "google_news",
            "q": query,
            "api_key": api_key,
            "num": 10,
            "gl": "us",
            "hl": "en",
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        news_results = results.get("news_results", [])[:10]
        
        articles: list[dict[str, Any]] = []
        for item in news_results:
            article = {
                "title": item.get("title", ""),
                "source": item.get("source", {}).get("name", "Unknown Source"),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "thumbnail": item.get("thumbnail"),
                "published_date": item.get("date"),
            }
            articles.append(article)
        
        logger.info(f"Retrieved {len(articles)} NVIDIA news articles from SerpAPI")
        return articles
        
    except Exception as e:
        logger.error(f"Error searching NVIDIA news: {e}")
        raise
