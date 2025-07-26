#!/usr/bin/env python3
"""
Fort Sentinel Dispatch API Server
Flask backend for PWA
"""

import os
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys

# Add scripts to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from fetch_articles import NewsFetcher
from generate_dispatch import FortParser, DispatchGenerator

app = Flask(__name__, static_folder='public')
CORS(app)

# Store articles temporarily in memory (in production, use Redis/DB)
article_cache = {}

@app.route('/')
def serve_pwa():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('public', path)

@app.route('/api/fetch-news')
def fetch_news():
    """Fetch news articles"""
    try:
        # Get API key from header
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        # Get parameters
        topic = request.args.get('topic')
        is_general = request.args.get('general', 'false').lower() == 'true'
        country = request.args.get('country', 'us')
        category = request.args.get('category')
        limit = int(request.args.get('limit', 10))
        
        # Fetch articles
        fetcher = NewsFetcher(api_key)
        
        if is_general:
            articles = fetcher.fetch_general_news(
                country=country,
                category=category,
                page_size=limit
            )
        else:
            if not topic:
                return jsonify({'error': 'Topic required for search'}), 400
            articles = fetcher.fetch_articles(topic, page_size=limit)
        
        # Cache articles
        for i, article in enumerate(articles):
            article_id = f"{datetime.now().timestamp()}_{i}"
            article_cache[article_id] = article
        
        # Return with IDs
        return jsonify({
            'articles': [
                {**article, 'id': f"{datetime.now().timestamp()}_{i}"}
                for i, article in enumerate(articles)
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-dispatch', methods=['POST'])
def generate_dispatch():
    """Generate Fort dispatch from article"""
    try:
        data = request.json
        article_id = data.get('article_id')
        
        if not article_id or article_id not in article_cache:
            return jsonify({'error': 'Invalid article ID'}), 400
        
        article = article_cache[article_id]
        
        # Generate Fort analysis
        parser = FortParser(llm_provider='none')  # Use basic analysis for demo
        analysis = parser.analyze_article(article)
        
        # Generate dispatch
        generator = DispatchGenerator()
        filepath = generator.generate_dispatch(article, analysis)
        
        # Return dispatch data
        return jsonify({
            'title': article['title'],
            'summary': analysis['summary'],
            'fort_frame': analysis['fort_frame'],
            'tags': analysis['tags'],
            'voice': analysis['voice_family'],
            'impact_zones': analysis['impact_zones'],
            'url': article['url'],
            'filepath': str(filepath),
            'fnafi_command': f'fnafi read "{filepath}"'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dispatches')
def get_dispatches():
    """Get saved dispatches"""
    try:
        tag = request.args.get('tag')
        date = request.args.get('date')
        
        dispatches = []
        dispatch_dir = Path('dispatch')
        
        if not dispatch_dir.exists():
            return jsonify({'dispatches': []})
        
        for date_dir in dispatch_dir.iterdir():
            if date_dir.is_dir():
                for file in date_dir.glob('*.md'):
                    # Read frontmatter
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.startswith('---'):
                            _, frontmatter, _ = content.split('---', 2)
                            # Parse frontmatter (simple parsing)
                            metadata = {}
                            for line in frontmatter.strip().split('\n'):
                                if ': ' in line:
                                    key, value = line.split(': ', 1)
                                    metadata[key] = value.strip('"')
                            
                            # Apply filters
                            if tag and tag not in metadata.get('tags', ''):
                                continue
                            if date and date != metadata.get('date', ''):
                                continue
                            
                            dispatches.append({
                                'file': str(file),
                                'title': metadata.get('title', ''),
                                'date': metadata.get('date', ''),
                                'tags': json.loads(metadata.get('tags', '[]')),
                                'voice': metadata.get('voice', ''),
                                'summary': metadata.get('summary', '')
                            })
        
        return jsonify({
            'dispatches': sorted(dispatches, key=lambda x: x['date'], reverse=True)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)