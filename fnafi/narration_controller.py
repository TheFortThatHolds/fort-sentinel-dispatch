#!/usr/bin/env python3
"""
FNAFI Integration Controller
Manages text-to-speech narration for Fort Sentinel Dispatches
"""

import os
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
import frontmatter
from typing import Dict, List, Optional

class FNAFIController:
    def __init__(self, fnafi_path: Optional[str] = None):
        self.fnafi_path = fnafi_path or "fnafi"
        self.dispatch_dir = Path("dispatch")
        
        # Voice personality mappings
        self.voice_mappings = {
            "RedWitness": {
                "voice": "intense",
                "speed": 1.1,
                "pitch": 0.9,
                "emotion": "righteous_anger"
            },
            "StillnessScribe": {
                "voice": "calm",
                "speed": 0.9,
                "pitch": 1.0,
                "emotion": "contemplative"
            },
            "TruthKeeper": {
                "voice": "analytical",
                "speed": 1.0,
                "pitch": 1.0,
                "emotion": "neutral_clarity"
            },
            "SurvivorVoice": {
                "voice": "gentle",
                "speed": 0.95,
                "pitch": 1.05,
                "emotion": "trauma_aware"
            }
        }
    
    def read_dispatch(self, filepath: str, voice_override: Optional[str] = None):
        """Read a dispatch file with FNAFI"""
        
        # Load markdown with frontmatter
        with open(filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        # Get voice settings
        voice_family = voice_override or post.metadata.get('voice', 'TruthKeeper')
        voice_config = self.voice_mappings.get(voice_family, self.voice_mappings['TruthKeeper'])
        
        # Prepare narration text
        narration_text = self._prepare_narration(post)
        
        # Execute FNAFI command
        cmd = [
            self.fnafi_path,
            "read",
            "--voice", voice_config['voice'],
            "--speed", str(voice_config['speed']),
            "--pitch", str(voice_config['pitch']),
            "--text", narration_text
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Narration started for: {post.metadata['title']}")
                print(f"🎭 Voice: {voice_family}")
            else:
                print(f"❌ Narration failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Error executing FNAFI: {e}")
    
    def _prepare_narration(self, post: frontmatter.Post) -> str:
        """Prepare text for narration"""
        
        # Build narration script
        sections = []
        
        # Title announcement
        sections.append(f"Fort Sentinel Dispatch: {post.metadata['title']}")
        
        # Date
        sections.append(f"Date: {post.metadata['date']}")
        
        # Fort Frame (emotional truth)
        if '## 🧠 Fort Frame' in post.content:
            frame_start = post.content.find('## 🧠 Fort Frame') + len('## 🧠 Fort Frame')
            frame_end = post.content.find('##', frame_start)
            frame_text = post.content[frame_start:frame_end].strip()
            sections.append(f"Fort Frame: {frame_text}")
        
        # Summary
        if post.metadata.get('summary'):
            sections.append(f"Summary: {post.metadata['summary']}")
        
        # Impact zones
        if post.metadata.get('impact_zones'):
            zones = ", ".join(post.metadata['impact_zones'])
            sections.append(f"Impact Zones: {zones}")
        
        return "\n\n".join(sections)
    
    def list_dispatches(self, tag: Optional[str] = None, date: Optional[str] = None) -> List[Dict]:
        """List available dispatches with optional filtering"""
        
        dispatches = []
        
        for date_dir in self.dispatch_dir.iterdir():
            if date_dir.is_dir():
                for file in date_dir.glob("*.md"):
                    with open(file, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                    
                    # Apply filters
                    if tag and tag not in post.metadata.get('tags', []):
                        continue
                    if date and date != str(post.metadata.get('date')):
                        continue
                    
                    dispatches.append({
                        "file": str(file),
                        "title": post.metadata['title'],
                        "date": post.metadata['date'],
                        "tags": post.metadata.get('tags', []),
                        "voice": post.metadata.get('voice', 'TruthKeeper')
                    })
        
        return sorted(dispatches, key=lambda x: x['date'], reverse=True)
    
    def read_latest(self, tag: Optional[str] = None):
        """Read the latest dispatch"""
        
        dispatches = self.list_dispatches(tag=tag)
        if dispatches:
            latest = dispatches[0]
            print(f"📰 Reading latest dispatch: {latest['title']}")
            self.read_dispatch(latest['file'])
        else:
            print("❌ No dispatches found")
    
    def batch_narrate(self, date: Optional[str] = None, limit: int = 5):
        """Narrate multiple dispatches in sequence"""
        
        dispatches = self.list_dispatches(date=date)[:limit]
        
        print(f"🎙️ Batch narration: {len(dispatches)} dispatches")
        
        for i, dispatch in enumerate(dispatches, 1):
            print(f"\n[{i}/{len(dispatches)}] {dispatch['title']}")
            self.read_dispatch(dispatch['file'])
            
            # Add pause between dispatches
            if i < len(dispatches):
                input("Press Enter for next dispatch...")

def main():
    parser = argparse.ArgumentParser(description="FNAFI narration controller for Fort Sentinel")
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read a dispatch')
    read_parser.add_argument('file', nargs='?', help='Dispatch file to read')
    read_parser.add_argument('--latest', action='store_true', help='Read latest dispatch')
    read_parser.add_argument('--tag', help='Filter by tag')
    read_parser.add_argument('--voice', help='Override voice family')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List dispatches')
    list_parser.add_argument('--tag', help='Filter by tag')
    list_parser.add_argument('--date', help='Filter by date (YYYY-MM-DD)')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch narrate dispatches')
    batch_parser.add_argument('--date', help='Filter by date')
    batch_parser.add_argument('--limit', type=int, default=5, help='Number of dispatches')
    
    args = parser.parse_args()
    
    controller = FNAFIController()
    
    if args.command == 'read':
        if args.latest:
            controller.read_latest(tag=args.tag)
        elif args.file:
            controller.read_dispatch(args.file, voice_override=args.voice)
        else:
            print("Specify --latest or provide a file path")
    
    elif args.command == 'list':
        dispatches = controller.list_dispatches(tag=args.tag, date=args.date)
        for d in dispatches:
            print(f"📄 {d['date']} - {d['title']} [{', '.join(d['tags'])}]")
    
    elif args.command == 'batch':
        controller.batch_narrate(date=args.date, limit=args.limit)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()