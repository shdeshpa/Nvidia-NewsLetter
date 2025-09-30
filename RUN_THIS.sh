#!/bin/bash
# Quick command to start the newsletter UI

echo "🚀 Starting NVIDIA AI Newsletter..."
echo ""
echo "Opening Streamlit UI at http://localhost:8501"
echo ""
echo "Click 'Generate New Newsletter' in the sidebar to begin!"
echo ""

uv run streamlit run src/NewsLetter2/app.py
