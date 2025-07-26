#!/usr/bin/env python3
"""
Fort Sentinel News Fetcher
Pulls real-time news from NewsAPI and saves to JSON
"""

import os
import json
import argparse
from datetime import datetime
import requests
from typing import List, Dict, Optional

class NewsFetcher:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('NEWSAPI_KEY')
        if not self.api_key:
            raise ValueError("NewsAPI key required. Set NEWSAPI_KEY env var or pass to constructor.")
        
        self.base_url = "https://newsapi.org/v2"
        self.headers = {"X-Api-Key": self.api_key}
    
    def fetch_articles(self, 
                      query: str, 
                      language: str = "en",
                      sort_by: str = "relevancy",
                      page_size: int = 10) -> List[Dict]:
        """Fetch articles from NewsAPI based on query"""
        
        endpoint = f"{self.base_url}/everything"
        params = {
            "q": query,
            "language": language,
            "sortBy": sort_by,
            "pageSize": page_size
        }
        
        return self._process_api_response(endpoint, params)
    
    def fetch_general_news(self,
                          country: str = "us",
                          category: Optional[str] = None,
                          page_size: int = 10) -> List[Dict]:
        """Fetch general/top headlines from NewsAPI"""
        
        endpoint = f"{self.base_url}/top-headlines"
        params = {
            "country": country,
            "pageSize": page_size
        }
        
        if category:
            params["category"] = category
        
        return self._process_api_response(endpoint, params)
    
    def _process_api_response(self, endpoint: str, params: Dict) -> List[Dict]:
        """Process API response and format articles"""
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] != "ok":
                raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")
            
            articles = []
            for article in data["articles"]:
                articles.append({
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "content": article.get("content", ""),
                    "publishedAt": article["publishedAt"],
                    "source": article["source"]["name"],
                    "author": article.get("author", "Unknown"),
                    "urlToImage": article.get("urlToImage", ""),
                    "fetchedAt": datetime.now().isoformat()
                })
            
            return articles
            
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return []
        except Exception as e:
            print(f"Error fetching articles: {e}")
            return []
    
    def save_articles(self, articles: List[Dict], output_path: str = "articles.json"):
        """Save articles to JSON file"""
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "count": len(articles),
            "articles": articles
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(articles)} articles to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Fetch news articles for Fort Sentinel Dispatch")
    parser.add_argument("--topic", "-t", help="Search topic/keywords (e.g., 'climate change', 'New York', 'technology')")
    parser.add_argument("--general", "-g", action="store_true", help="Fetch general/top headlines instead of topic search")
    parser.add_argument("--country", "-c", default="us", help="Country code for general news (default: us)")
    parser.add_argument("--category", help="Category for general news (business, entertainment, health, science, sports, technology)")
    parser.add_argument("--output", "-o", default="articles.json", help="Output JSON file")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Number of articles to fetch")
    parser.add_argument("--api-key", "-k", help="NewsAPI key (or set NEWSAPI_KEY env var)")
    
    args = parser.parse_args()
    
    if not args.topic and not args.general:
        parser.error("Either --topic or --general must be specified")
    
    try:
        fetcher = NewsFetcher(args.api_key)
        
        if args.general:
            articles = fetcher.fetch_general_news(country=args.country, category=args.category, page_size=args.limit)
            search_desc = f"general news ({args.country}" + (f", {args.category}" if args.category else "") + ")"
        else:
            articles = fetcher.fetch_articles(args.topic, page_size=args.limit)
            search_desc = f"'{args.topic}'"
        
        if articles:
            fetcher.save_articles(articles, args.output)
            print(f"\nFetched {len(articles)} articles about {search_desc}")
            print(f"First article: {articles[0]['title']}")
        else:
            print("No articles found or error occurred.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()