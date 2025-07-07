#!/usr/bin/env python3
"""
Test script to show the satirical skits prompt structure
"""

def show_skit_prompt():
    """Show the satirical skits prompt structure"""
    
    skit_prompt = """
    Generate 3 satirical skit ideas for "We'll Be Right Back" - an AI comedy series.
    
    Requirements for each skit:
    - 8 seconds or less duration
    - One location/setting only
    - No more than 1-3 characters
    - Highbrow, clever tone with dark humor
    - Double entendres and edgy comedic deliveries
    - Engaging cinematic elements
    - Satirical take on pop culture topics
    - Pop culture references and parody elements
    
    For each skit, provide:
    1. TITLE: Clever, witty title
    2. SETTING: Single location description
    3. CHARACTERS: 1-3 character descriptions
    4. PREMISE: The satirical concept
    5. DIALOGUE: Key lines with double entendres
    6. CINEMATIC: Visual/camera elements
    7. PUNCHLINE: The edgy comedic payoff
    
    Format each skit as a structured comedy sketch that could be filmed in 8 seconds.
    """
    
    print("🎭 SATIRICAL SKITS PROMPT STRUCTURE")
    print("=" * 50)
    print(skit_prompt)
    
    print("\n📝 SUGGESTED IMPROVEMENTS:")
    print("-" * 30)
    print("1. Add specific examples of double entendres")
    print("2. Include timing breakdowns (setup, punchline)")
    print("3. Specify camera angles and movements")
    print("4. Add costume/prop requirements")
    print("5. Include specific pop culture references")
    print("6. Add tone examples (deadpan delivery, etc.)")
    print("7. Specify lighting/mood requirements")

if __name__ == "__main__":
    show_skit_prompt()

# Different themes
skits = agent.generate_satirical_skits(theme="tech industry", count=3)
skits = agent.generate_satirical_skits(theme="politics", count=2)
skits = agent.generate_satirical_skits(theme="social media", count=5) 