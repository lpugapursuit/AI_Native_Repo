"""
Copywriting Agent for Automated Workflow
Handles content generation, copywriting tasks, and text processing
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from we_will_be_right_back_automator.src.api_clients import get_openai_client, OpenAIClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CopywritingAgent:
    """
    AI-powered copywriting agent for automated content generation
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the copywriting agent
        
        Args:
            api_key: API key for the AI service (OpenAI, etc.)
        """
        # Use the unified API client system
        self.openai_client = get_openai_client() or OpenAIClient(api_key)
        
        if not self.openai_client.api_key:
            logger.warning("No OpenAI API key provided. Some features may not work.")
    
    def generate_copy(self, 
                     prompt: str, 
                     style: str = "professional",
                     tone: str = "friendly",
                     length: str = "medium",
                     target_audience: str = "general") -> str:
        """
        Generate copy based on given parameters
        
        Args:
            prompt: The main prompt or topic for the copy
            style: Writing style (professional, casual, creative, etc.)
            tone: Tone of voice (friendly, formal, humorous, etc.)
            length: Desired length (short, medium, long)
            target_audience: Target audience description
            
        Returns:
            Generated copy text
        """
        try:
            system_prompt = self._build_system_prompt(style, tone, target_audience)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate {length} copy about: {prompt}"}
            ]
            
            response = self._make_api_request(messages)
            return response.get('choices', [{}])[0].get('message', {}).get('content', '')
            
        except Exception as e:
            logger.error(f"Error generating copy: {e}")
            return f"Error generating copy: {str(e)}"
    
    def generate_social_media_copy(self, video_description: str, platform: str, brand_voice_guidelines: dict):
        """
        Generate social media copy based on video description and brand guidelines
        
        Args:
            video_description: Description of the video content
            platform: Target social media platform (twitter, instagram, linkedin, facebook, tiktok, youtube)
            brand_voice_guidelines: Dictionary containing brand voice parameters
            
        Returns:
            Generated social media copy optimized for the platform
        """
        try:
            # Extract brand voice parameters
            tone = brand_voice_guidelines.get('tone', 'deadpan')
            style = brand_voice_guidelines.get('style', 'absurdist')
            personality = brand_voice_guidelines.get('personality', 'sarcastic')
            call_to_action = brand_voice_guidelines.get('call_to_action', 'subscribe')
            series_name = brand_voice_guidelines.get('series_name', "We'll Be Right Back")
            
            # Comprehensive platform-specific prompts for AI comedy series
            platform_prompts = {
                "youtube": f"""
                You are writing copy for '{series_name}', an AI comedy series with deadpan, absurdist humor. 
                
                Video Description: {video_description}
                
                Create the following for YouTube:
                
                1. TITLE (60 characters max, clickbait but deadpan):
                - Use deadpan humor and subtle absurdity
                - Include numbers, questions, or unexpected twists
                - Avoid over-the-top clickbait, keep it dry and ironic
                
                2. DESCRIPTION (5000 characters max):
                - Start with a deadpan, absurdist hook
                - Include 2-3 bullet points with dry humor
                - Add relevant timestamps if applicable
                - Include deadpan call-to-action
                - Add 3-5 relevant hashtags at the end
                - Keep the absurdist tone throughout
                
                3. HASHTAGS (15-20 relevant tags):
                - Mix comedy, AI, and relevant topic hashtags
                - Include some absurdist/niche tags
                - Use both popular and specific hashtags
                
                Tone: Deadpan, absurdist, sarcastic, dry humor
                Style: Understated, ironic, subtly chaotic
                """,
                
                "instagram": f"""
                You are writing copy for '{series_name}', an AI comedy series with deadpan, absurdist humor.
                
                Video Description: {video_description}
                
                Create an Instagram caption with:
                - Deadpan, absurdist opening line
                - 2-3 lines of dry humor about the content
                - Subtle call-to-action
                - 5-8 relevant hashtags
                - Emoji usage: minimal and ironic
                
                Format: Engaging but understated, perfect for Instagram's visual-first platform
                Tone: Deadpan, absurdist, subtly chaotic
                """,
                
                "tiktok": f"""
                You are writing copy for '{series_name}', an AI comedy series with deadpan, absurdist humor.
                
                Video Description: {video_description}
                
                Create a TikTok caption with:
                - Hook that's absurdist but TikTok-friendly
                - 1-2 lines of deadpan humor
                - Trending but ironic hashtags
                - Call-to-action that fits TikTok culture
                - 3-5 hashtags (mix trending and niche)
                
                Format: Short, punchy, but maintain the deadpan absurdist voice
                Tone: Deadpan, absurdist, TikTok-aware but not pandering
                """,
                
                "twitter": f"""
                You are writing copy for '{series_name}', an AI comedy series with deadpan, absurdist humor.
                
                Video Description: {video_description}
                
                Create a Twitter post (280 characters max):
                - Deadpan, absurdist tweet
                - Include relevant hashtags
                - Subtle call-to-action
                - Use Twitter's conversational but dry tone
                
                Tone: Deadpan, absurdist, Twitter-native
                """,
                
                "linkedin": f"""
                You are writing copy for '{series_name}', an AI comedy series with deadpan, absurdist humor.
                
                Video Description: {video_description}
                
                Create a LinkedIn post:
                - Professional but absurdist opening
                - Industry insights with dry humor
                - Subtle call-to-action
                - 3-5 professional hashtags
                
                Tone: Deadpan, absurdist, but LinkedIn-appropriate
                """,
                
                "facebook": f"""
                You are writing copy for '{series_name}', an AI comedy series with deadpan, absurdist humor.
                
                Video Description: {video_description}
                
                Create a Facebook post:
                - Deadpan, shareable opening
                - 2-3 lines of dry humor
                - Call-to-action for engagement
                - 5-8 relevant hashtags
                
                Tone: Deadpan, absurdist, Facebook-friendly
                """
            }
            
            prompt = platform_prompts.get(platform, platform_prompts.get("youtube", f"Create a social media post about this video: {video_description}"))
            
            # Generate the copy using the comprehensive prompt
            copy = self.generate_copy(
                prompt=prompt,
                style=style,
                tone=tone,
                target_audience=brand_voice_guidelines.get('target_audience', 'comedy_ai_enthusiasts')
            )
            
            return copy
            
        except Exception as e:
            logger.error(f"Error generating social media copy: {e}")
            return f"Error generating social media copy: {str(e)}"

    def generate_social_media_post(self, 
                                 topic: str, 
                                 platform: str = "general",
                                 hashtags: bool = True) -> Dict[str, str]:
        """
        Generate social media posts for different platforms
        
        Args:
            topic: The topic or content for the post
            platform: Target platform (twitter, instagram, linkedin, facebook)
            hashtags: Whether to include hashtags
            
        Returns:
            Dictionary with post content and hashtags
        """
        try:
            platform_prompts = {
                "twitter": "Create a Twitter post (280 characters max) with engaging copy",
                "instagram": "Create an Instagram caption with engaging copy and call-to-action",
                "linkedin": "Create a professional LinkedIn post with industry insights",
                "facebook": "Create a Facebook post with engaging, shareable content",
                "general": "Create a social media post with engaging copy"
            }
            
            prompt = f"{platform_prompts.get(platform, platform_prompts['general'])} about: {topic}"
            
            post_content = self.generate_copy(prompt, style="casual", tone="engaging")
            
            result = {"content": post_content}
            
            if hashtags:
                hashtag_prompt = f"Generate 3-5 relevant hashtags for: {topic}"
                hashtags_text = self.generate_copy(hashtag_prompt, length="short")
                result["hashtags"] = hashtags_text
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating social media post: {e}")
            return {"content": f"Error: {str(e)}", "hashtags": ""}
    
    def generate_email_copy(self, 
                          subject: str,
                          purpose: str = "informational",
                          audience: str = "customers") -> Dict[str, str]:
        """
        Generate email copy including subject line and body
        
        Args:
            subject: Email subject or topic
            purpose: Email purpose (informational, promotional, transactional)
            audience: Target audience
            
        Returns:
            Dictionary with subject line and body content
        """
        try:
            # Generate subject line
            subject_prompt = f"Create an engaging email subject line for: {subject}"
            subject_line = self.generate_copy(subject_prompt, length="short", style="professional")
            
            # Generate email body
            body_prompt = f"Write an email about: {subject}. Purpose: {purpose}. Audience: {audience}"
            email_body = self.generate_copy(body_prompt, style="professional", tone="friendly")
            
            return {
                "subject": subject_line,
                "body": email_body
            }
            
        except Exception as e:
            logger.error(f"Error generating email copy: {e}")
            return {"subject": f"Error: {str(e)}", "body": ""}
    
    def optimize_copy(self, 
                     original_text: str, 
                     goal: str = "engagement",
                     target_length: Optional[int] = None) -> str:
        """
        Optimize existing copy for better performance
        
        Args:
            original_text: Original copy to optimize
            goal: Optimization goal (engagement, conversion, clarity)
            target_length: Target word count (optional)
            
        Returns:
            Optimized copy
        """
        try:
            optimization_prompt = f"""
            Optimize this copy for {goal}:
            
            Original: {original_text}
            
            Goal: {goal}
            """
            
            if target_length:
                optimization_prompt += f"\nTarget length: {target_length} words"
            
            return self.generate_copy(optimization_prompt, style="professional")
            
        except Exception as e:
            logger.error(f"Error optimizing copy: {e}")
            return f"Error optimizing copy: {str(e)}"
    
    def generate_satirical_skits(self, 
                                theme: str = "pop culture",
                                count: int = 5) -> List[Dict[str, str]]:
        """
        Generate satirical skit ideas for short-form comedy videos
        
        Args:
            theme: Theme or topic area (pop culture, politics, tech, etc.)
            count: Number of skit ideas to generate
            
        Returns:
            List of dictionaries containing skit details
        """
        try:
            skit_prompt = f"""
            You are a comedy writer for "We'll Be Right Back" - an AI comedy series known for deadpan, absurdist humor with highbrow wit and dark comedy.
            
            Generate {count} satirical skit ideas that poke fun at {theme} topics using:
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
            
            skits_text = self.generate_copy(skit_prompt, length="long")
            
            # Parse the response into structured skit data
            skits = self._parse_skit_response(skits_text, count)
            
            return skits
            
        except Exception as e:
            logger.error(f"Error generating satirical skits: {e}")
            return [{"error": f"Error generating skits: {str(e)}"}]

    def generate_content_ideas(self, 
                             topic: str, 
                             content_type: str = "blog",
                             count: int = 5) -> List[str]:
        """
        Generate content ideas for a given topic
        
        Args:
            topic: Main topic or industry
            content_type: Type of content (blog, video, social, etc.)
            count: Number of ideas to generate
            
        Returns:
            List of content ideas
        """
        try:
            prompt = f"Generate {count} {content_type} content ideas about: {topic}"
            ideas_text = self.generate_copy(prompt, length="long")
            
            # Split into individual ideas (simple approach)
            ideas = [idea.strip() for idea in ideas_text.split('\n') if idea.strip()]
            return ideas[:count]
            
        except Exception as e:
            logger.error(f"Error generating content ideas: {e}")
            return [f"Error generating ideas: {str(e)}"]

    def _parse_skit_response(self, skits_text: str, count: int) -> List[Dict[str, str]]:
        """
        Parse the LLM response into structured skit data
        
        Args:
            skits_text: Raw text response from LLM
            count: Expected number of skits
            
        Returns:
            List of structured skit dictionaries
        """
        try:
            skits = []
            lines = skits_text.split('\n')
            current_skit = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if line.startswith(('SKIT', '1.', '2.', '3.', '4.', '5.')) and current_skit:
                    if len(skits) < count:
                        skits.append(current_skit)
                    current_skit = {}
                    
                elif line.startswith('TITLE:'):
                    current_skit['title'] = line.replace('TITLE:', '').strip()
                elif line.startswith('SETTING:'):
                    current_skit['setting'] = line.replace('SETTING:', '').strip()
                elif line.startswith('CHARACTERS:'):
                    current_skit['characters'] = line.replace('CHARACTERS:', '').strip()
                elif line.startswith('PREMISE:'):
                    current_skit['premise'] = line.replace('PREMISE:', '').strip()
                elif line.startswith('DIALOGUE:'):
                    current_skit['dialogue'] = line.replace('DIALOGUE:', '').strip()
                elif line.startswith('CINEMATIC:'):
                    current_skit['cinematic'] = line.replace('CINEMATIC:', '').strip()
                elif line.startswith('PUNCHLINE:'):
                    current_skit['punchline'] = line.replace('PUNCHLINE:', '').strip()
                elif line.startswith('TIMING:'):
                    current_skit['timing'] = line.replace('TIMING:', '').strip()
                elif line.startswith('PROPS/COSTUMES:'):
                    current_skit['props_costumes'] = line.replace('PROPS/COSTUMES:', '').strip()
            
            # Add the last skit if we have one
            if current_skit and len(skits) < count:
                skits.append(current_skit)
            
            return skits[:count]
            
        except Exception as e:
            logger.error(f"Error parsing skit response: {e}")
            return [{"error": f"Error parsing skits: {str(e)}"}]
    
    def _build_system_prompt(self, style: str, tone: str, audience: str) -> str:
        """Build system prompt based on parameters"""
        return f"""You are a professional copywriter. Write in a {style} style with a {tone} tone for {audience} audience. 
        Focus on creating engaging, clear, and compelling copy that drives action."""
    
    def _make_api_request(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Make API request using unified client system"""
        if not self.openai_client.api_key:
            raise ValueError("OpenAI API key is required for API requests")
        
        try:
            response_text = self.openai_client.generate_text(
                messages=messages,
                model="gpt-3.5-turbo",
                max_tokens=1000,
                temperature=0.7
            )
            
            # Return in the expected format
            return {
                "choices": [{
                    "message": {
                        "content": response_text
                    }
                }]
            }
            
        except Exception as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def save_copy(self, copy: str, filename: str, metadata: Optional[Dict] = None):
        """
        Save generated copy to a file with metadata
        
        Args:
            copy: The generated copy text
            filename: Output filename
            metadata: Additional metadata to save
        """
        try:
            output_data = {
                "copy": copy,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Copy saved to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving copy: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Initialize the agent
    agent = CopywritingAgent()
    
    # Test copy generation
    test_copy = agent.generate_copy(
        prompt="Benefits of using AI for copywriting",
        style="professional",
        tone="friendly",
        length="medium"
    )
    
    print("Generated Copy:")
    print(test_copy)
    print("\n" + "="*50 + "\n")
    
    # Test social media post
    social_post = agent.generate_social_media_post(
        topic="AI copywriting tools",
        platform="linkedin"
    )
    
    print("Social Media Post:")
    print(f"Content: {social_post['content']}")
    print(f"Hashtags: {social_post.get('hashtags', 'N/A')}") 