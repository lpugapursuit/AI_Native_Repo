import time
from we_will_be_right_back_automator.src.api_clients import SocialMediaClient

class TikTokClient(SocialMediaClient):
    def __init__(self, api_key=None, access_token=None):
        super().__init__(api_key, access_token)
        self.base_url = "https://open.tiktokapis.com/v2"

    def connect(self):
        if self.api_key and self.access_token:
            self.connected = True
            return True
        return False

    def post(self, content, **kwargs):
        if not self.connected:
            self.connect()
        
        # Extract TikTok-specific content
        caption = content.get('caption', content.get('content', ''))
        hashtags = content.get('hashtags', '')
        
        # TikTok has character limits, so we need to be concise
        full_caption = f"{caption} {hashtags}".strip()
        if len(full_caption) > 2200:  # TikTok's limit is 2200 characters
            full_caption = full_caption[:2197] + "..."
        
        # Simulate TikTok posting
        print(f"[TikTok] Posting: {full_caption[:100]}...")
        return {
            "status": "success", 
            "platform": "tiktok",
            "content": full_caption,
            "post_id": f"tt_{int(time.time())}"
        }

    def upload_video(self, video_path, caption="", **kwargs):
        """Upload a video to TikTok"""
        if not self.connected:
            self.connect()
        
        # Simulate video upload
        print(f"[TikTok] Uploading video: {video_path}")
        print(f"[TikTok] Caption: {caption[:100]}...")
        
        return {
            "status": "success",
            "platform": "tiktok",
            "video_path": video_path,
            "caption": caption,
            "post_id": f"tt_video_{int(time.time())}"
        }

    def get_stats(self, post_id):
        return {
            "post_id": post_id, 
            "likes": 892, 
            "comments": 67, 
            "shares": 234,
            "views": 15420
        } 