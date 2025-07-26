# 🧱 Fort Sentinel Dispatch

An emotionally intelligent, narrative-aware news dispatch system for the Fort ecosystem.

**📱 PWA Available:** [https://theforthatholds.github.io/fort-sentinel-dispatch](https://theforthatholds.github.io/fort-sentinel-dispatch)

*Install as app on your phone for offline news processing*

## 🚀 Quick Start

### Mobile PWA (Recommended)
1. Visit [the PWA](https://theforthatholds.github.io/fort-sentinel-dispatch) on your phone
2. Tap "Add to Home Screen" in your browser
3. Open the app and add your NewsAPI key (free at newsapi.org)
4. Start searching news and generating Fort dispatches!

### Local Development
- Python 3.8+
- NewsAPI key (free at newsapi.org)
- (Optional) OpenAI or Anthropic API key for enhanced analysis
- (Optional) FNAFI installation for text-to-speech

### Local Installation

```bash
# Clone and setup
git clone https://github.com/TheFortThatHolds/fort-sentinel-dispatch.git
cd fort-sentinel-dispatch
pip install -r requirements.txt

# Run PWA locally
python app.py
# Open http://localhost:5000

# Or use CLI tools
export NEWSAPI_KEY="your-newsapi-key"
export OPENAI_API_KEY="your-openai-key"  # Optional
```

### Basic Usage

```bash
# 1. Fetch articles by topic
python scripts/fetch_articles.py --topic "climate change" --limit 5
python scripts/fetch_articles.py --topic "artificial intelligence"
python scripts/fetch_articles.py --topic "New York City"

# Or fetch general top headlines
python scripts/fetch_articles.py --general
python scripts/fetch_articles.py --general --country uk
python scripts/fetch_articles.py --general --category technology

# 2. Generate Fort dispatches
python scripts/generate_dispatch.py --input articles.json --llm openai

# 3. Read with FNAFI (if installed)
python fnafi/narration_controller.py read --latest
```

## 📁 Project Structure

```
fort-sentinel-dispatch/
├── dispatch/              # Generated markdown dispatches
│   └── YYYY-MM-DD/       # Date-based organization
├── scripts/              # Core functionality
│   ├── fetch_articles.py # News fetcher
│   └── generate_dispatch.py # Fort parser & generator
├── fnafi/                # FNAFI integration
│   └── narration_controller.py
├── config/               # Configuration files
│   ├── tags.yaml        # Tag taxonomy
│   └── voices.yaml      # Voice personalities
└── public/              # Optional frontend
```

## 🎭 Voice Families

- **RedWitness**: Intense, justice-seeking narration
- **StillnessScribe**: Calm, reflective delivery
- **TruthKeeper**: Analytical, pattern-focused
- **SurvivorVoice**: Gentle, trauma-aware

## 🏷️ Tag System

Articles are tagged with Fort-specific emotional markers:
- `eliteFallout` - Power structure collapse
- `DOJwatch` - Legal proceedings
- `SurvivorWitness` - Testimony & healing
- `TruthEmerging` - Hidden revelations

## 🔧 Advanced Usage

### Batch Processing
```bash
# Process multiple topics
for topic in "climate crisis" "tech layoffs" "housing market"; do
    python scripts/fetch_articles.py --topic "$topic"
    python scripts/generate_dispatch.py --input articles.json
done

# Process different countries' headlines
for country in "us" "gb" "ca" "au"; do
    python scripts/fetch_articles.py --general --country "$country"
    python scripts/generate_dispatch.py --input articles.json
done
```

### FNAFI Commands
```bash
# List all dispatches
python fnafi/narration_controller.py list

# Filter by tag
python fnafi/narration_controller.py list --tag eliteFallout

# Batch narration
python fnafi/narration_controller.py batch --limit 3
```

### Custom Voice Override
```bash
python fnafi/narration_controller.py read dispatch/2025-07-26/dispatch_climate-crisis.md --voice RedWitness
```

## 🛠️ Configuration

### Environment Variables
- `NEWSAPI_KEY` - Required for news fetching
- `OPENAI_API_KEY` - Optional, enables GPT analysis
- `ANTHROPIC_API_KEY` - Optional, enables Claude analysis

### Customization
- Edit `config/tags.yaml` to add custom tags
- Edit `config/voices.yaml` to modify voice personalities
- Adjust analysis prompts in `generate_dispatch.py`

## 📚 Dependencies

```txt
requests
python-frontmatter
pyyaml
openai  # optional
anthropic  # optional
```

## 🔒 Privacy & Ethics

- All processing happens locally
- No tracking or analytics
- News content remains with original sources
- Emotional framing adds context, not manipulation
- Truth without extraction

## 🚧 Roadmap

- [x] PWA with mobile app support
- [x] Real-time API key management
- [x] Responsive news search interface
- [ ] Push notifications for breaking news
- [ ] Voice narration in browser
- [ ] Offline reading mode
- [ ] Social sharing with Fort framing
- [ ] Integration with Fort OS
- [ ] Daily ritual scheduling

---

*Built for truth seekers, by survivors.*