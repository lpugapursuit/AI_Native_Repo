#!/usr/bin/env python3
"""
Mock output viewer to show what the satirical skits function would produce
"""

def show_mock_output():
    """Show what the output would look like with real API data"""
    
    mock_skits = [
        {
            "title": "The Algorithm's Dinner Party",
            "setting": "Minimalist kitchen with smart appliances",
            "characters": "AI Assistant (deadpan), Human (confused), Smart Fridge (sassy)",
            "premise": "AI tries to host a dinner party but only serves algorithmically optimized food",
            "timing": "Setup 3s: AI announces dinner. Punchline 5s: Serves only kale smoothies",
            "dialogue": "AI: 'I've analyzed your preferences and determined you need 47% more fiber.' Human: 'I just wanted pizza.'",
            "cinematic": "Close-up on AI's emotionless face, wide shot of disappointing meal, slow zoom on kale smoothie",
            "props_costumes": "AI wears apron with circuit patterns, human in casual clothes, smart fridge with LED display",
            "punchline": "AI serves kale smoothie with deadpan delivery: 'Your taste buds will thank me in 3.7 years.'"
        },
        {
            "title": "Social Media Detox Gone Wrong",
            "setting": "Cozy living room with phone prominently displayed",
            "characters": "Person (anxious), Phone (tempting), Therapist (virtual)",
            "premise": "Person attempts social media detox but phone keeps sending notifications",
            "timing": "Setup 3s: Person deletes apps. Punchline 5s: Phone finds new ways to distract",
            "dialogue": "Person: 'I'm finally free!' Phone: *plays notification sound* Person: '...damn it.'",
            "cinematic": "Phone screen glow in dark room, person's face illuminated by notifications, dramatic lighting",
            "props_costumes": "Phone with bright screen, person in comfy clothes, virtual therapist on laptop",
            "punchline": "Phone starts playing 'Baby Shark' at max volume: 'You can't escape the algorithm.'"
        },
        {
            "title": "The Influencer's Existential Crisis",
            "setting": "Instagram-worthy bedroom with perfect lighting",
            "characters": "Influencer (panicked), Camera (judging), Mirror (honest)",
            "premise": "Influencer realizes they're living for likes instead of life",
            "timing": "Setup 3s: Influencer poses. Punchline 5s: Mirror shows reality",
            "dialogue": "Influencer: 'Do I even like this coffee, or do I just like how it looks?' Mirror: 'You don't even drink coffee.'",
            "cinematic": "Perfect lighting suddenly flickers, mirror shows unedited reflection, camera angle shifts to reveal truth",
            "props_costumes": "Influencer in trendy outfit, camera on tripod, mirror with honest reflection",
            "punchline": "Influencer sees real self in mirror: 'Oh no, I'm becoming a hashtag.'"
        }
    ]
    
    print("🎭 MOCK OUTPUT: Satirical Skits Generation")
    print("=" * 60)
    print("This is what the function would produce with a real API key:")
    print()
    
    for i, skit in enumerate(mock_skits, 1):
        print(f"🎬 SKIT {i}: {skit['title']}")
        print("-" * 50)
        print(f"SETTING: {skit['setting']}")
        print(f"CHARACTERS: {skit['characters']}")
        print(f"PREMISE: {skit['premise']}")
        print(f"TIMING: {skit['timing']}")
        print(f"DIALOGUE: {skit['dialogue']}")
        print(f"CINEMATIC: {skit['cinematic']}")
        print(f"PROPS/COSTUMES: {skit['props_costumes']}")
        print(f"PUNCHLINE: {skit['punchline']}")
        print()
    
    print("✨ To get real output:")
    print("1. Add your OpenAI API key to .env file")
    print("2. Run: py test_skits.py")
    print("3. Or run: py simple_test.py")

if __name__ == "__main__":
    show_mock_output() 