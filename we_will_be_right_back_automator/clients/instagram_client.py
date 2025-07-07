import time
from we_will_be_right_back_automator.src.api_clients import SocialMediaClient

class InstagramClient(SocialMediaClient):
    def __init__(self, api_key=None, access_token=None):
        super().__init__(api_key, access_token)
        self.base_url = "https://graph.instagram.com/v12.0"

    def connect(self):
        if self.api_key and self.access_token:
            self.connected = True
            return True
        return False

    def post(self, content, **kwargs):
        if not self.connected:
            self.connect()
        
        # Extract Instagram-specific content
        caption = content.get('caption', content.get('content', ''))
        hashtags = content.get('hashtags', '')
        
        # Combine caption and hashtags
        full_caption = f"{caption}\n\n{hashtags}"
        
        # Simulate Instagram posting
        print(f"[Instagram] Posting: {full_caption[:100]}...")
        return {
            "status": "success", 
            "platform": "instagram",
            "content": full_caption,
            "post_id": f"ig_{int(time.time())}"
        }

    def post_story(self, content, **kwargs):
        """Post to Instagram Stories"""
        if not self.connected:
            self.connect()
        
        story_text = content.get('story_text', content.get('content', ''))
        print(f"[Instagram Stories] Posting: {story_text[:50]}...")
        
        return {
            "status": "success",
            "platform": "instagram_stories", 
            "content": story_text,
            "post_id": f"ig_story_{int(time.time())}"
        }

    def get_stats(self, post_id):
        return {
            "post_id": post_id, 
            "likes": 156, 
            "comments": 23, 
            "shares": 8,
            "saves": 12
        } 