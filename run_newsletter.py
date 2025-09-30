# =============================================================================
#  Filename: run_newsletter.py
#
#  Short Description: CLI entry point for NVIDIA newsletter generation
#
#  Creation date: 2025-09-30
#  Author: Shrinivas Deshpande
# =============================================================================

"""
Command-line interface for generating NVIDIA AI newsletter.

Usage:
    python run_newsletter.py

This script orchestrates the CrewAI workflow to collect, summarize,
and package NVIDIA news into a professional newsletter.
"""

from loguru import logger

from NewsLetter2.crew import run_newsletter_generation


def main() -> None:
    """Execute newsletter generation workflow."""
    logger.info("🚀 Starting NVIDIA AI Newsletter Generation")
    logger.info("=" * 60)
    
    try:
        result = run_newsletter_generation()
        
        logger.success("✅ Newsletter generated successfully!")
        logger.info("Output saved to: newsletter_output.json")
        logger.info("To view the newsletter, run: streamlit run src/NewsLetter2/app.py")
        
    except Exception as e:
        logger.error(f"❌ Newsletter generation failed: {e}")
        raise


if __name__ == "__main__":
    main()
