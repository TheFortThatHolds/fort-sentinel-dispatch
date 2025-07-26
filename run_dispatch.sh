#!/bin/bash
# Fort Sentinel Dispatch Runner
# Quick script to fetch and process news

set -e

# Check if topic provided
if [ $# -eq 0 ]; then
    echo "🧱 Fort Sentinel Dispatch System"
    echo "================================"
    echo ""
    echo "Usage: ./run_dispatch.sh <topic> [limit] [llm]"
    echo "       ./run_dispatch.sh --general [limit] [llm]"
    echo ""
    echo "Examples:"
    echo "  ./run_dispatch.sh 'climate change' 10 openai"
    echo "  ./run_dispatch.sh 'artificial intelligence' 5"
    echo "  ./run_dispatch.sh --general 10"
    echo ""
    exit 1
fi

# Parse arguments
if [ "$1" = "--general" ]; then
    MODE="general"
    LIMIT="${2:-10}"
    LLM="${3:-none}"
else
    MODE="topic"
    TOPIC="$1"
    LIMIT="${2:-10}"
    LLM="${3:-none}"
fi

echo "🧱 Fort Sentinel Dispatch System"
echo "================================"
if [ "$MODE" = "general" ]; then
    echo "Mode: General Headlines"
else
    echo "Topic: $TOPIC"
fi
echo "Articles: $LIMIT"
echo "LLM: $LLM"
echo ""

# Fetch articles
echo "📰 Fetching articles..."
if [ "$MODE" = "general" ]; then
    python scripts/fetch_articles.py --general --limit "$LIMIT"
else
    python scripts/fetch_articles.py --topic "$TOPIC" --limit "$LIMIT"
fi

# Generate dispatches
echo ""
echo "🧠 Generating Fort dispatches..."
python scripts/generate_dispatch.py --input articles.json --llm "$LLM"

# Show results
echo ""
echo "✅ Dispatches generated!"
echo "📁 Check the dispatch/ folder"
echo ""

# Offer to read latest
read -p "🎧 Read latest dispatch with FNAFI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python fnafi/narration_controller.py read --latest
fi