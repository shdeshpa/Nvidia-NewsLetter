#!/bin/bash
# =============================================================================
#  Filename: quickstart.sh
#
#  Short Description: Quick setup script for NVIDIA AI Newsletter
#
#  Creation date: 2025-09-30
#  Author: Shrinivas Deshpande
# =============================================================================

set -e

echo "🚀 NVIDIA AI Newsletter - Quick Start"
echo "======================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "✅ .env file created. Please edit it and add your API keys:"
    echo "   - OPENAI_API_KEY (get from: https://platform.openai.com/api-keys)"
    echo "   - SERP_API_KEY (get from: https://serpapi.com/manage-api-key)"
    echo ""
    echo "After adding your keys, run this script again."
    exit 1
fi

# Check if API keys are set
source .env
if [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ] || [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Please set OPENAI_API_KEY in your .env file"
    exit 1
fi

if [ "$SERP_API_KEY" = "your_serpapi_api_key_here" ] || [ -z "$SERP_API_KEY" ]; then
    echo "❌ Please set SERP_API_KEY in your .env file"
    exit 1
fi

echo "✅ API keys configured"
echo ""

# Install dependencies if needed
echo "📦 Checking dependencies..."
uv sync
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Choose how to run the newsletter:"
echo ""
echo "  Option 1 - Streamlit UI (Recommended):"
echo "    uv run streamlit run src/NewsLetter2/app.py"
echo ""
echo "  Option 2 - Command Line:"
echo "    uv run python run_newsletter.py"
echo ""
