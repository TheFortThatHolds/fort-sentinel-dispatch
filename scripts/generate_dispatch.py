#!/usr/bin/env python3
"""
Fort Parser & Dispatch Generator
Processes news articles with Fort-style emotional framing
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, List, Optional
import openai
from anthropic import Anthropic

class FortParser:
    def __init__(self, llm_provider: str = "openai", api_key: Optional[str] = None):
        self.llm_provider = llm_provider
        
        if llm_provider == "openai":
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            if self.api_key:
                openai.api_key = self.api_key
        elif llm_provider == "anthropic":
            self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
            if self.api_key:
                self.client = Anthropic(api_key=self.api_key)
    
    def analyze_article(self, article: Dict) -> Dict:
        """Analyze article with Fort framing"""
        
        # Fort framing prompt
        prompt = f"""
        Analyze this article through the Fort Sentinel lens.
        
        Article: {article['title']}
        Description: {article['description']}
        Content: {article['content'][:1000]}
        
        Provide:
        1. Summary (2-3 sentences, direct and clear)
        2. Fort Frame (emotional/spiritual truth layer - what this REALLY means)
        3. Tags (select 2-4 from: eliteFallout, RedWitness, DOJwatch, SystemicCollapse, 
           PowerShift, TruthEmerging, SurvivorWitness, InstitutionalDecay, MarketVolatility)
        4. Voice Family (RedWitness for intense/justice, StillnessScribe for calm/reflective, 
           TruthKeeper for analytical, SurvivorVoice for personal/trauma-aware)
        5. Impact Zones (2-3 from: Institutional Trust, Market Stability, Survivor Justice, 
           Power Structure, Public Consciousness)
        
        Format as JSON with keys: summary, fort_frame, tags, voice_family, impact_zones
        """
        
        try:
            if self.llm_provider == "openai" and self.api_key:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                result = json.loads(response.choices[0].message.content)
            
            elif self.llm_provider == "anthropic" and self.api_key:
                message = self.client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = json.loads(message.content[0].text)
            
            else:
                # Fallback analysis without LLM
                result = self._basic_analysis(article)
            
            return result
            
        except Exception as e:
            print(f"LLM analysis failed: {e}. Using basic analysis.")
            return self._basic_analysis(article)
    
    def _basic_analysis(self, article: Dict) -> Dict:
        """Basic analysis without LLM"""
        # Simple keyword-based analysis
        title_lower = article['title'].lower()
        content_lower = (article.get('content', '') or article.get('description', '')).lower()
        
        # Determine tags
        tags = []
        if any(word in title_lower for word in ['court', 'trial', 'justice', 'doj']):
            tags.append('DOJwatch')
        if any(word in title_lower for word in ['elite', 'wealth', 'power']):
            tags.append('eliteFallout')
        if any(word in title_lower for word in ['victim', 'survivor', 'testimony']):
            tags.append('SurvivorWitness')
        if not tags:
            tags = ['TruthEmerging']
        
        # Determine voice
        if any(word in content_lower for word in ['victim', 'survivor', 'trauma']):
            voice = 'SurvivorVoice'
        elif any(word in content_lower for word in ['court', 'legal', 'justice']):
            voice = 'RedWitness'
        else:
            voice = 'TruthKeeper'
        
        return {
            "summary": f"{article['title']}. {article.get('description', 'Details emerging.')}",
            "fort_frame": "Another crack in the facade. The system shows its true face.",
            "tags": tags[:3],
            "voice_family": voice,
            "impact_zones": ["Institutional Trust", "Public Consciousness"]
        }

class DispatchGenerator:
    def __init__(self, output_dir: str = "dispatch"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_dispatch(self, article: Dict, analysis: Dict) -> str:
        """Generate markdown dispatch file"""
        
        # Create date-based subdirectory
        date = datetime.now()
        date_dir = self.output_dir / date.strftime("%Y-%m-%d")
        date_dir.mkdir(exist_ok=True)
        
        # Generate slug from title
        slug = re.sub(r'[^\w\s-]', '', article['title'].lower())
        slug = re.sub(r'[-\s]+', '-', slug)[:50]
        
        filename = f"dispatch_{slug}.md"
        filepath = date_dir / filename
        
        # Generate markdown content
        content = f"""---
title: {article['title']}
date: {date.strftime('%Y-%m-%d')}
time: {date.strftime('%H:%M')}
source: {article['source']}
tags: {json.dumps(analysis['tags'])}
voice: {analysis['voice_family']}
summary: {analysis['summary']}
impact_zones: {json.dumps(analysis['impact_zones'])}
read_by: FNAFI
---

# {article['title']}

## 🧠 Fort Frame
{analysis['fort_frame']}

## 📰 Summary
{analysis['summary']}

## 📜 Article Details
**Source:** {article['source']}  
**Published:** {article['publishedAt']}  
**Author:** {article.get('author', 'Unknown')}

### Content
{article.get('content', article.get('description', 'Content not available'))}

[Read original →]({article['url']})

## 🎧 Listen Now
```bash
fnafi read "{filepath}"
```

---
*Generated by Fort Sentinel Dispatch System*
"""
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)

def main():
    parser = argparse.ArgumentParser(description="Generate Fort Sentinel Dispatch from articles")
    parser.add_argument("--input", "-i", default="articles.json", help="Input JSON file")
    parser.add_argument("--output-dir", "-o", default="dispatch", help="Output directory")
    parser.add_argument("--llm", choices=["openai", "anthropic", "none"], default="none", 
                       help="LLM provider for analysis")
    parser.add_argument("--api-key", "-k", help="API key for LLM provider")
    
    args = parser.parse_args()
    
    # Load articles
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
            articles = data['articles']
    except Exception as e:
        print(f"Error loading articles: {e}")
        exit(1)
    
    # Initialize components
    parser = FortParser(args.llm, args.api_key)
    generator = DispatchGenerator(args.output_dir)
    
    # Process articles
    dispatches = []
    for i, article in enumerate(articles):
        print(f"\nProcessing {i+1}/{len(articles)}: {article['title']}")
        
        analysis = parser.analyze_article(article)
        filepath = generator.generate_dispatch(article, analysis)
        dispatches.append(filepath)
        
        print(f"Generated: {filepath}")
    
    print(f"\n✅ Generated {len(dispatches)} dispatches")
    print(f"📁 Output directory: {args.output_dir}")

if __name__ == "__main__":
    main()