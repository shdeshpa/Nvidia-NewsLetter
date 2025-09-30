# =============================================================================
#  Filename: __init__.py
#
#  Short Description: NewsLetter2 package initialization
#
#  Creation date: 2025-09-30
#  Author: Shrinivas Deshpande
# =============================================================================

"""
NVIDIA AI Newsletter - CrewAI-based news aggregation and analysis system.

This package provides an intelligent newsletter generation system using
three specialized AI agents powered by OpenAI API and SerpAPI.
"""

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

__version__ = "0.1.0"
__author__ = "Shrinivas Deshpande"

__all__ = [
    "models",
    "agents",
    "tasks",
    "crew",
    "tools",
    "app",
]
