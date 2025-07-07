#!/usr/bin/env python3
"""
Test script for the satirical skits generation function
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from copywriting_agent import CopywritingAgent

def test_satirical_skits():
    """Test the satirical skits generation function"""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize the agent
    agent = CopywritingAgent()
    
    print("🎭 Testing Satirical Skits Generation")
    print("=" * 50)
    
    # Test with different themes
    themes = ["pop culture", "tech industry", "social media"]
    
    for theme in themes:
        print(f"\n📝 Generating skits for theme: {theme.upper()}")
        print("-" * 30)
        
        try:
            skits = agent.generate_satirical_skits(theme=theme, count=3)
            
            for i, skit in enumerate(skits, 1):
                print(f"\n🎬 SKIT {i}:")
                print(f"Title: {skit.get('title', 'N/A')}")
                print(f"Setting: {skit.get('setting', 'N/A')}")
                print(f"Characters: {skit.get('characters', 'N/A')}")
                print(f"Premise: {skit.get('premise', 'N/A')}")
                print(f"Dialogue: {skit.get('dialogue', 'N/A')}")
                print(f"Cinematic: {skit.get('cinematic', 'N/A')}")
                print(f"Punchline: {skit.get('punchline', 'N/A')}")
                print("-" * 20)
                
        except Exception as e:
            print(f"Error generating skits for {theme}: {e}")
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_satirical_skits() 