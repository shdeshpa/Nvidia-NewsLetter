# =============================================================================
#  Filename: test_api_keys.py
#
#  Short Description: Simple test to verify API keys are loaded correctly
#
#  Creation date: 2025-09-30
#  Author: Shrinivas Deshpande
# =============================================================================

"""Quick test to verify environment variables are loaded correctly."""

import os

from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()


def test_api_keys() -> None:
    """Test that required API keys are present."""
    logger.info("Testing API key configuration...")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    serp_key = os.getenv("SERP_API_KEY")
    
    if openai_key:
        logger.success(f"✅ OPENAI_API_KEY found: {openai_key[:20]}...")
    else:
        logger.error("❌ OPENAI_API_KEY not found in environment")
    
    if serp_key:
        logger.success(f"✅ SERP_API_KEY found: {serp_key[:20]}...")
    else:
        logger.error("❌ SERP_API_KEY not found in environment")
    
    if openai_key and serp_key:
        logger.success("🎉 All API keys configured correctly!")
        return True
    else:
        logger.error("❌ Missing API keys. Please check your .env file")
        return False


if __name__ == "__main__":
    test_api_keys()
