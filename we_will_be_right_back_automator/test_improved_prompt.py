#!/usr/bin/env python3
"""
Test script to show the improved satirical skits prompt structure
"""

def show_improved_skit_prompt():
    """Show the improved satirical skits prompt structure"""
    
    improved_prompt = """
    You are a comedy writer for "We'll Be Right Back" - an AI comedy series known for deadpan, absurdist humor with highbrow wit and dark comedy.
    
    Generate 3 satirical skit ideas that poke fun at pop culture topics using:
    - Deadpan delivery and absurdist premises
    - Clever double entendres and wordplay
    - Edgy, dark humor that's smart, not crude
    - Pop culture parody and references
    - Highbrow comedy that's accessible but sophisticated
    
    SKIT REQUIREMENTS:
    - Duration: Exactly 8 seconds or less
    - Location: Single setting only (kitchen, office, park bench, etc.)
    - Characters: Maximum 3 characters, minimal dialogue
    - Tone: Deadpan, absurdist, clever, darkly humorous
    - Style: Highbrow wit with engaging cinematic elements
    
    FORMAT FOR EACH SKIT:
    
    SKIT [NUMBER]:
    TITLE: [Clever, witty title with wordplay or double entendre]
    SETTING: [Single location with specific details for 8-second shoot]
    CHARACTERS: [1-3 characters with distinct personalities]
    PREMISE: [The satirical concept and setup]
    TIMING: [Breakdown: Setup 3s, Punchline 5s]
    DIALOGUE: [Key lines with double entendres, deadpan delivery]
    CINEMATIC: [Camera angles, movements, lighting for visual comedy]
    PROPS/COSTUMES: [Minimal props that enhance the joke]
    PUNCHLINE: [The edgy comedic payoff with timing]
    
    EXAMPLES OF TONE:
    - Deadpan delivery: "Well, that escalated quickly... into a tax audit."
    - Double entendres: "I'm not saying it's a bad idea, I'm saying it's the kind of idea that makes lawyers rich."
    - Dark humor: "At least the AI apocalypse will be well-documented on social media."
    
    Make each skit memorable, quotable, and perfectly timed for 8 seconds of comedy gold.
    """
    
    print("🎭 IMPROVED SATIRICAL SKITS PROMPT")
    print("=" * 50)
    print(improved_prompt)
    
    print("\n✨ KEY IMPROVEMENTS MADE:")
    print("-" * 30)
    print("✅ Added specific tone examples and delivery style")
    print("✅ Included timing breakdowns (Setup 3s, Punchline 5s)")
    print("✅ Added PROPS/COSTUMES section for production details")
    print("✅ Specified camera angles and cinematic elements")
    print("✅ Added examples of deadpan delivery and double entendres")
    print("✅ Emphasized highbrow, accessible comedy")
    print("✅ Made the 8-second constraint more explicit")
    print("✅ Added character personality requirements")
    print("✅ Included specific location examples")

if __name__ == "__main__":
    show_improved_skit_prompt() 