import time
from we_will_be_right_back_automator.src.api_clients import SocialMediaClient

class LinkedInClient(SocialMediaClient):
    def __init__(self, api_key=None, access_token=None):
        super().__init__(api_key, access_token)
        self.base_url = "https://api.linkedin.com/v2"

    def connect(self):
        if self.api_key and self.access_token:
            self.connected = True
            return True
        return False

    def post(self, content, **kwargs):
        if not self.connected:
            self.connect()
        
        # Extract LinkedIn-specific content
        post_text = content.get('content', content.get('caption', ''))
        hashtags = content.get('hashtags', '')
        
        # LinkedIn posts can be longer, so we can include more content
        full_post = f"{post_text}\n\n{hashtags}".strip()
        
        # Simulate LinkedIn posting
        print(f"[LinkedIn] Posting: {full_post[:100]}...")
        return {
            "status": "success", 
            "platform": "linkedin",
            "content": full_post,
            "post_id": f"li_{int(time.time())}"
        }

    def post_article(self, title, content, **kwargs):
        """Post a LinkedIn article"""
        if not self.connected:
            self.connect()
        
        print(f"[LinkedIn] Publishing article: {title}")
        print(f"[LinkedIn] Content preview: {content[:200]}...")
        
        return {
            "status": "success",
            "platform": "linkedin",
            "type": "article",
            "title": title,
            "content": content,
            "post_id": f"li_article_{int(time.time())}"
        }

    def get_stats(self, post_id):
        return {
            "post_id": post_id, 
            "likes": 45, 
            "comments": 12, 
            "shares": 8,
            "impressions": 1200
        } 