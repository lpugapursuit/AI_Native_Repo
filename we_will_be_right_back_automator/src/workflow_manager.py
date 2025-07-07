"""
Daily Workflow Manager for Social Media Automation
Handles scheduling, content generation, and automated posting
"""

import os
import json
import logging
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import random

from we_will_be_right_back_automator.src.copywriting_agent import CopywritingAgent
from we_will_be_right_back_automator.clients.twitter_client import TwitterClient
from we_will_be_right_back_automator.clients.youtube_client import YoutubeClient
from we_will_be_right_back_automator.clients.instagram_client import InstagramClient
from we_will_be_right_back_automator.clients.tiktok_client import TikTokClient
from we_will_be_right_back_automator.clients.linkedin_client import LinkedInClient
from we_will_be_right_back_automator.clients.facebook_client import FacebookClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentWorkflow:
    """Represents a single content workflow with generation and posting"""
    
    def __init__(self, 
                 workflow_id: str,
                 content_type: str,
                 platforms: List[str],
                 schedule_time: str,
                 brand_voice: Dict[str, str],
                 content_prompt: str = None):
        self.workflow_id = workflow_id
        self.content_type = content_type  # 'daily_post', 'video_upload', 'engagement'
        self.platforms = platforms
        self.schedule_time = schedule_time  # "HH:MM" format
        self.brand_voice = brand_voice
        self.content_prompt = content_prompt
        self.last_run = None
        self.next_run = None
        self.status = "pending"
        self.generated_content = {}
        self.posting_results = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary for storage"""
        return {
            "workflow_id": self.workflow_id,
            "content_type": self.content_type,
            "platforms": self.platforms,
            "schedule_time": self.schedule_time,
            "brand_voice": self.brand_voice,
            "content_prompt": self.content_prompt,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "status": self.status,
            "generated_content": self.generated_content,
            "posting_results": self.posting_results
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContentWorkflow':
        """Create workflow from dictionary"""
        workflow = cls(
            workflow_id=data["workflow_id"],
            content_type=data["content_type"],
            platforms=data["platforms"],
            schedule_time=data["schedule_time"],
            brand_voice=data["brand_voice"],
            content_prompt=data.get("content_prompt")
        )
        workflow.last_run = datetime.fromisoformat(data["last_run"]) if data.get("last_run") else None
        workflow.next_run = datetime.fromisoformat(data["next_run"]) if data.get("next_run") else None
        workflow.status = data.get("status", "pending")
        workflow.generated_content = data.get("generated_content", {})
        workflow.posting_results = data.get("posting_results", {})
        return workflow


class WorkflowManager:
    """
    Manages daily automated workflows for content creation and posting
    """
    
    def __init__(self, config_path: str = "workflow_config.json"):
        self.config_path = Path(config_path)
        self.workflows: Dict[str, ContentWorkflow] = {}
        self.copywriting_agent = CopywritingAgent()
        self.social_clients = {}
        self.is_running = False
        
        # Initialize social media clients
        self._initialize_clients()
        
        # Load existing workflows
        self.load_workflows()
        
        # Default brand voice for "We'll Be Right Back"
        self.default_brand_voice = {
            "tone": "deadpan",
            "style": "absurdist", 
            "personality": "sarcastic",
            "call_to_action": "subscribe",
            "series_name": "We'll Be Right Back"
        }
    
    def _initialize_clients(self):
        """Initialize social media clients"""
        try:
            # Initialize Twitter client
            twitter_api_key = os.getenv('TWITTER_API_KEY')
            twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            self.social_clients['twitter'] = TwitterClient(twitter_api_key, twitter_access_token)
            
            # Initialize YouTube client
            youtube_api_key = os.getenv('YOUTUBE_API_KEY')
            youtube_access_token = os.getenv('YOUTUBE_ACCESS_TOKEN')
            self.social_clients['youtube'] = YoutubeClient(youtube_api_key, youtube_access_token)
            
            # Initialize Instagram client
            instagram_api_key = os.getenv('INSTAGRAM_API_KEY')
            instagram_access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
            self.social_clients['instagram'] = InstagramClient(instagram_api_key, instagram_access_token)
            
            # Initialize TikTok client
            tiktok_api_key = os.getenv('TIKTOK_API_KEY')
            tiktok_access_token = os.getenv('TIKTOK_ACCESS_TOKEN')
            self.social_clients['tiktok'] = TikTokClient(tiktok_api_key, tiktok_access_token)
            
            # Initialize LinkedIn client
            linkedin_api_key = os.getenv('LINKEDIN_API_KEY')
            linkedin_access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
            self.social_clients['linkedin'] = LinkedInClient(linkedin_api_key, linkedin_access_token)
            
            # Initialize Facebook client
            facebook_api_key = os.getenv('FACEBOOK_API_KEY')
            facebook_access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
            self.social_clients['facebook'] = FacebookClient(facebook_api_key, facebook_access_token)
            
            logger.info(f"Initialized {len(self.social_clients)} social media clients")
            
        except Exception as e:
            logger.warning(f"Some social media clients failed to initialize: {e}")
    
    def create_daily_workflow(self, 
                            platforms: List[str],
                            schedule_time: str = "09:00",
                            content_prompt: str = None) -> str:
        """
        Create a new daily content workflow
        
        Args:
            platforms: List of platforms to post to
            schedule_time: Time to run daily (HH:MM format)
            content_prompt: Optional specific prompt for content generation
            
        Returns:
            Workflow ID
        """
        workflow_id = f"daily_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate content prompt if not provided
        if not content_prompt:
            content_prompt = self._generate_daily_prompt()
        
        workflow = ContentWorkflow(
            workflow_id=workflow_id,
            content_type="daily_post",
            platforms=platforms,
            schedule_time=schedule_time,
            brand_voice=self.default_brand_voice,
            content_prompt=content_prompt
        )
        
        self.workflows[workflow_id] = workflow
        self.save_workflows()
        
        logger.info(f"Created daily workflow: {workflow_id}")
        return workflow_id
    
    def create_video_workflow(self,
                            video_path: str,
                            platforms: List[str],
                            schedule_time: str = "15:00") -> str:
        """
        Create a workflow for video upload and promotion
        
        Args:
            video_path: Path to the video file
            platforms: List of platforms to post to
            schedule_time: Time to run (HH:MM format)
            
        Returns:
            Workflow ID
        """
        workflow_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        workflow = ContentWorkflow(
            workflow_id=workflow_id,
            content_type="video_upload",
            platforms=platforms,
            schedule_time=schedule_time,
            brand_voice=self.default_brand_voice,
            content_prompt=f"Create promotional content for video: {video_path}"
        )
        
        # Store video path in workflow
        workflow.generated_content['video_path'] = video_path
        
        self.workflows[workflow_id] = workflow
        self.save_workflows()
        
        logger.info(f"Created video workflow: {workflow_id}")
        return workflow_id
    
    def _generate_daily_prompt(self) -> str:
        """Generate a random daily content prompt"""
        daily_prompts = [
            "AI trying to understand human humor",
            "The absurdity of daily life with artificial intelligence",
            "When algorithms meet human chaos",
            "Digital assistant existential crisis",
            "Tech support for the technologically challenged",
            "AI attempts to cook human food",
            "Virtual assistant vs real-world problems",
            "Machine learning meets human learning",
            "AI tries to understand memes",
            "Digital life in an analog world"
        ]
        
        return random.choice(daily_prompts)
    
    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Execute a specific workflow
        
        Args:
            workflow_id: ID of the workflow to execute
            
        Returns:
            Execution results
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        workflow.status = "running"
        workflow.last_run = datetime.now()
        
        results = {
            "workflow_id": workflow_id,
            "start_time": workflow.last_run.isoformat(),
            "content_generation": {},
            "posting_results": {},
            "errors": []
        }
        
        try:
            # Step 1: Generate content for each platform
            logger.info(f"Generating content for workflow {workflow_id}")
            for platform in workflow.platforms:
                try:
                    if workflow.content_type == "video_upload":
                        content = self._generate_video_content(workflow, platform)
                    else:
                        content = self._generate_platform_content(workflow, platform)
                    
                    workflow.generated_content[platform] = content
                    results["content_generation"][platform] = content
                    
                except Exception as e:
                    error_msg = f"Content generation failed for {platform}: {str(e)}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
            
            # Step 2: Post content to platforms
            logger.info(f"Posting content for workflow {workflow_id}")
            for platform in workflow.platforms:
                try:
                    if platform in workflow.generated_content:
                        posting_result = self._post_to_platform(platform, workflow.generated_content[platform])
                        workflow.posting_results[platform] = posting_result
                        results["posting_results"][platform] = posting_result
                        
                except Exception as e:
                    error_msg = f"Posting failed for {platform}: {str(e)}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
            
            workflow.status = "completed"
            
        except Exception as e:
            workflow.status = "failed"
            error_msg = f"Workflow execution failed: {str(e)}"
            logger.error(error_msg)
            results["errors"].append(error_msg)
        
        # Save updated workflow state
        self.save_workflows()
        
        return results
    
    def _generate_platform_content(self, workflow: ContentWorkflow, platform: str) -> Dict[str, str]:
        """Generate content for a specific platform"""
        video_description = workflow.content_prompt or "Daily AI comedy content"
        
        return self.copywriting_agent.generate_social_media_copy(
            video_description=video_description,
            platform=platform,
            brand_voice_guidelines=workflow.brand_voice
        )
    
    def _generate_video_content(self, workflow: ContentWorkflow, platform: str) -> Dict[str, str]:
        """Generate content for video upload"""
        video_path = workflow.generated_content.get('video_path', 'Unknown video')
        video_description = f"New video upload: {video_path}"
        
        return self.copywriting_agent.generate_social_media_copy(
            video_description=video_description,
            platform=platform,
            brand_voice_guidelines=workflow.brand_voice
        )
    
    def _post_to_platform(self, platform: str, content: Dict[str, str]) -> Dict[str, Any]:
        """Post content to a specific platform"""
        if platform not in self.social_clients:
            raise ValueError(f"No client configured for platform: {platform}")
        
        client = self.social_clients[platform]
        
        if platform == "youtube":
            # For YouTube, we need to handle video upload
            video_path = content.get('video_path')
            title = content.get('title', 'Untitled')
            return client.upload_video(video_path, title)
        else:
            # For other platforms, post the content
            post_content = content.get('content', content.get('caption', ''))
            return client.post(post_content)
    
    def schedule_workflow(self, workflow_id: str):
        """Schedule a workflow to run at its specified time"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        
        # Schedule the workflow to run daily at the specified time
        schedule.every().day.at(workflow.schedule_time).do(
            self.execute_workflow, workflow_id
        )
        
        logger.info(f"Scheduled workflow {workflow_id} to run daily at {workflow.schedule_time}")
    
    def start_scheduler(self):
        """Start the scheduler to run all workflows"""
        self.is_running = True
        
        # Schedule all workflows
        for workflow_id in self.workflows:
            self.schedule_workflow(workflow_id)
        
        logger.info("Scheduler started. Running workflows...")
        
        # Run the scheduler
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.is_running = False
        schedule.clear()
        logger.info("Scheduler stopped")
    
    def load_workflows(self):
        """Load workflows from configuration file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                
                self.workflows = {
                    workflow_id: ContentWorkflow.from_dict(workflow_data)
                    for workflow_id, workflow_data in data.items()
                }
                
                logger.info(f"Loaded {len(self.workflows)} workflows from {self.config_path}")
                
            except Exception as e:
                logger.error(f"Failed to load workflows: {e}")
    
    def save_workflows(self):
        """Save workflows to configuration file"""
        try:
            data = {
                workflow_id: workflow.to_dict()
                for workflow_id, workflow in self.workflows.items()
            }
            
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {len(self.workflows)} workflows to {self.config_path}")
            
        except Exception as e:
            logger.error(f"Failed to save workflows: {e}")
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of a specific workflow"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        return workflow.to_dict()
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows"""
        return [
            {
                "workflow_id": workflow_id,
                "content_type": workflow.content_type,
                "platforms": workflow.platforms,
                "schedule_time": workflow.schedule_time,
                "status": workflow.status,
                "last_run": workflow.last_run.isoformat() if workflow.last_run else None
            }
            for workflow_id, workflow in self.workflows.items()
        ]
    
    def delete_workflow(self, workflow_id: str):
        """Delete a workflow"""
        if workflow_id in self.workflows:
            del self.workflows[workflow_id]
            self.save_workflows()
            logger.info(f"Deleted workflow: {workflow_id}")
        else:
            raise ValueError(f"Workflow {workflow_id} not found") 