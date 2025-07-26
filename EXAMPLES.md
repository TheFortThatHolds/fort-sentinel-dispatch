# Fort Sentinel Dispatch - Usage Examples

## 📰 Topic-Based Searches

Search for any topic, location, company, person, or concept:

```bash
# Current events
python scripts/fetch_articles.py --topic "israel palestine"
python scripts/fetch_articles.py --topic "ukraine war"
python scripts/fetch_articles.py --topic "inflation crisis"

# Technology
python scripts/fetch_articles.py --topic "artificial intelligence ethics"
python scripts/fetch_articles.py --topic "chatgpt impact"
python scripts/fetch_articles.py --topic "tech layoffs 2025"

# Environmental
python scripts/fetch_articles.py --topic "climate emergency"
python scripts/fetch_articles.py --topic "renewable energy"
python scripts/fetch_articles.py --topic "ocean pollution"

# Geographic
python scripts/fetch_articles.py --topic "San Francisco"
python scripts/fetch_articles.py --topic "Tokyo Olympics"
python scripts/fetch_articles.py --topic "European Union"

# Financial
python scripts/fetch_articles.py --topic "cryptocurrency regulation"
python scripts/fetch_articles.py --topic "housing market crash"
python scripts/fetch_articles.py --topic "federal reserve"

# Social Issues
python scripts/fetch_articles.py --topic "mental health crisis"
python scripts/fetch_articles.py --topic "homelessness"
python scripts/fetch_articles.py --topic "education reform"

# Corporate
python scripts/fetch_articles.py --topic "Amazon workers"
python scripts/fetch_articles.py --topic "Tesla autopilot"
python scripts/fetch_articles.py --topic "pharmaceutical profits"
```

## 🌍 General Headlines

Get top headlines by country or category:

```bash
# Top headlines by country
python scripts/fetch_articles.py --general --country us
python scripts/fetch_articles.py --general --country gb  # Great Britain
python scripts/fetch_articles.py --general --country ca  # Canada
python scripts/fetch_articles.py --general --country au  # Australia
python scripts/fetch_articles.py --general --country de  # Germany
python scripts/fetch_articles.py --general --country fr  # France

# Top headlines by category
python scripts/fetch_articles.py --general --category technology
python scripts/fetch_articles.py --general --category business
python scripts/fetch_articles.py --general --category health
python scripts/fetch_articles.py --general --category science
python scripts/fetch_articles.py --general --category entertainment
python scripts/fetch_articles.py --general --category sports

# Combine country and category
python scripts/fetch_articles.py --general --country us --category technology
python scripts/fetch_articles.py --general --country gb --category business
```

## 🔄 Automated Workflows

### Daily News Ritual
```bash
#!/bin/bash
# morning_dispatch.sh

# Get general US headlines
python scripts/fetch_articles.py --general --country us --limit 5
python scripts/generate_dispatch.py --llm openai
python fnafi/narration_controller.py read --latest

# Get tech news
python scripts/fetch_articles.py --general --category technology --limit 3
python scripts/generate_dispatch.py
python fnafi/narration_controller.py read --latest
```

### Multi-Topic Scanner
```bash
#!/bin/bash
# scan_topics.sh

TOPICS=(
    "housing crisis"
    "climate change"
    "artificial intelligence"
    "economic recession"
    "healthcare costs"
)

for topic in "${TOPICS[@]}"; do
    echo "Scanning: $topic"
    python scripts/fetch_articles.py --topic "$topic" --limit 3
    python scripts/generate_dispatch.py
done

# Read all with FNAFI
python fnafi/narration_controller.py batch --limit 15
```

### Geographic News Monitor
```bash
#!/bin/bash
# location_monitor.sh

LOCATIONS=(
    "Silicon Valley tech"
    "Wall Street finance"
    "Washington DC politics"
    "Los Angeles entertainment"
    "Detroit automotive"
)

for location in "${LOCATIONS[@]}"; do
    python scripts/fetch_articles.py --topic "$location" --limit 2
    python scripts/generate_dispatch.py
done
```

## 🎭 Voice-Specific Searches

Match topics to appropriate Fort voices:

```bash
# RedWitness voice (justice/accountability)
python scripts/fetch_articles.py --topic "corporate fraud"
python scripts/fetch_articles.py --topic "government corruption"
python scripts/fetch_articles.py --topic "police accountability"

# SurvivorVoice (trauma-aware)
python scripts/fetch_articles.py --topic "trauma recovery"
python scripts/fetch_articles.py --topic "domestic violence support"
python scripts/fetch_articles.py --topic "mental health resources"

# StillnessScribe (contemplative)
python scripts/fetch_articles.py --topic "mindfulness research"
python scripts/fetch_articles.py --topic "spiritual practices"
python scripts/fetch_articles.py --topic "meditation benefits"

# TruthKeeper (analytical)
python scripts/fetch_articles.py --topic "data privacy"
python scripts/fetch_articles.py --topic "scientific breakthrough"
python scripts/fetch_articles.py --topic "economic analysis"
```

## 🔍 Advanced Queries

Combine keywords for specific results:

```bash
# Complex searches
python scripts/fetch_articles.py --topic "climate change AND corporate responsibility"
python scripts/fetch_articles.py --topic "artificial intelligence OR machine learning"
python scripts/fetch_articles.py --topic "housing crisis San Francisco"
python scripts/fetch_articles.py --topic "renewable energy investment 2025"

# Trending topics
python scripts/fetch_articles.py --topic "#MeToo movement"
python scripts/fetch_articles.py --topic "viral TikTok"
python scripts/fetch_articles.py --topic "Twitter controversy"

# Industry specific
python scripts/fetch_articles.py --topic "biotech breakthrough"
python scripts/fetch_articles.py --topic "quantum computing"
python scripts/fetch_articles.py --topic "space exploration"
```

## 💡 Tips

1. **Use quotes** for multi-word topics: `--topic "climate change"`
2. **Be specific** for better results: "San Francisco housing" vs just "housing"
3. **Check spelling** - NewsAPI is literal with search terms
4. **Experiment** with different phrasings if results seem off
5. **Mix approaches** - Try both topic search and category browsing

Remember: This system adds Fort-style emotional framing to ANY news topic, helping process information through a trauma-aware, truth-seeking lens.