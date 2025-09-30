#!/usr/bin/env python3
# Quick test to verify the entire system works

from loguru import logger
from NewsLetter2.crew import create_newsletter_crew

logger.info("🧪 Quick System Test")
logger.info("=" * 60)

try:
    logger.info("Step 1: Testing API keys...")
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found")
    if not os.getenv("SERP_API_KEY"):
        raise ValueError("SERP_API_KEY not found")
    logger.success("✅ API keys loaded")
    
    logger.info("Step 2: Testing crew creation...")
    crew = create_newsletter_crew()
    logger.success(f"✅ Crew created: {len(crew.agents)} agents, {len(crew.tasks)} tasks")
    
    logger.info("Step 3: Testing tool import...")
    from NewsLetter2.tools import search_nvidia_news
    logger.success(f"✅ Tool loaded: {search_nvidia_news.name}")
    
    logger.info("")
    logger.success("🎉 All tests passed! System is ready to generate newsletters!")
    logger.info("")
    logger.info("To generate a newsletter, run:")
    logger.info("  ./RUN_THIS.sh")
    logger.info("or")
    logger.info("  uv run streamlit run src/NewsLetter2/app.py")
    
except Exception as e:
    logger.error(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
