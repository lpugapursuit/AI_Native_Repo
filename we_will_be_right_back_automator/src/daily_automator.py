"""
Daily Automator - Main script for running automated social media workflows
"""

import os
import sys
import logging
import argparse
from datetime import datetime
from pathlib import Path

from we_will_be_right_back_automator.src.workflow_manager import WorkflowManager
from we_will_be_right_back_automator.src.copywriting_agent import CopywritingAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_automator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DailyAutomator:
    """
    Main automation class that orchestrates the daily content creation and posting
    """
    
    def __init__(self, config_file: str = "workflow_config.json"):
        self.workflow_manager = WorkflowManager(config_file)
        self.copywriting_agent = CopywritingAgent()
        
    def setup_daily_workflows(self):
        """Set up default daily workflows for the week"""
        logger.info("Setting up daily workflows...")
        
        # Daily posting schedule for different platforms
        daily_schedule = [
            {
                "platforms": ["twitter", "instagram"],
                "time": "09:00",
                "prompt": "Morning AI humor - the absurdity of starting the day with artificial intelligence"
            },
            {
                "platforms": ["twitter", "linkedin"],
                "time": "12:00", 
                "prompt": "Lunch break with AI - when algorithms try to understand human meal times"
            },
            {
                "platforms": ["twitter", "instagram", "tiktok"],
                "time": "15:00",
                "prompt": "Afternoon AI chaos - the digital assistant's mid-day crisis"
            },
            {
                "platforms": ["twitter", "facebook"],
                "time": "18:00",
                "prompt": "Evening AI reflections - artificial intelligence contemplates human behavior"
            }
        ]
        
        created_workflows = []
        for i, schedule_item in enumerate(daily_schedule):
            workflow_id = self.workflow_manager.create_daily_workflow(
                platforms=schedule_item["platforms"],
                schedule_time=schedule_item["time"],
                content_prompt=schedule_item["prompt"]
            )
            created_workflows.append(workflow_id)
            logger.info(f"Created workflow {workflow_id} for {schedule_item['time']}")
        
        logger.info(f"Created {len(created_workflows)} daily workflows")
        return created_workflows
    
    def run_single_workflow(self, workflow_id: str):
        """Run a single workflow immediately"""
        logger.info(f"Running workflow: {workflow_id}")
        try:
            results = self.workflow_manager.execute_workflow(workflow_id)
            logger.info(f"Workflow {workflow_id} completed successfully")
            return results
        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed: {e}")
            return None
    
    def run_all_pending_workflows(self):
        """Run all workflows that are due"""
        logger.info("Checking for pending workflows...")
        
        workflows = self.workflow_manager.list_workflows()
        current_time = datetime.now()
        
        for workflow in workflows:
            if workflow["status"] == "pending":
                # Check if it's time to run this workflow
                schedule_time = datetime.strptime(workflow["schedule_time"], "%H:%M").time()
                current_time_only = current_time.time()
                
                # If it's within 5 minutes of the scheduled time, run it
                time_diff = abs((current_time_only.hour * 60 + current_time_only.minute) - 
                               (schedule_time.hour * 60 + schedule_time.minute))
                
                if time_diff <= 5:
                    logger.info(f"Running pending workflow: {workflow['workflow_id']}")
                    self.run_single_workflow(workflow['workflow_id'])
    
    def start_daily_automation(self):
        """Start the daily automation process"""
        logger.info("Starting daily automation...")
        
        try:
            # Start the workflow scheduler
            self.workflow_manager.start_scheduler()
        except KeyboardInterrupt:
            logger.info("Stopping automation...")
            self.workflow_manager.stop_scheduler()
        except Exception as e:
            logger.error(f"Automation failed: {e}")
            self.workflow_manager.stop_scheduler()
    
    def generate_weekly_content_plan(self):
        """Generate a weekly content plan"""
        logger.info("Generating weekly content plan...")
        
        weekly_themes = [
            "AI Monday - The struggle of artificial intelligence on Mondays",
            "Tech Tuesday - When algorithms meet human technology",
            "Weird Wednesday - The absurdity of mid-week AI behavior", 
            "Thoughtful Thursday - AI contemplates human existence",
            "Fun Friday - Artificial intelligence tries to have fun",
            "Social Saturday - AI attempts to understand human social behavior",
            "Sunday AI - Digital assistant's day of rest (or chaos)"
        ]
        
        content_plan = []
        for i, theme in enumerate(weekly_themes):
            day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][i]
            
            # Generate content ideas for each day
            ideas = self.copywriting_agent.generate_content_ideas(
                topic=theme,
                content_type="social_media",
                count=3
            )
            
            content_plan.append({
                "day": day_name,
                "theme": theme,
                "content_ideas": ideas
            })
        
        # Save the content plan
        plan_file = f"weekly_content_plan_{datetime.now().strftime('%Y%m%d')}.json"
        import json
        with open(plan_file, 'w') as f:
            json.dump(content_plan, f, indent=2)
        
        logger.info(f"Weekly content plan saved to {plan_file}")
        return content_plan
    
    def get_status_report(self):
        """Generate a status report of all workflows"""
        workflows = self.workflow_manager.list_workflows()
        
        report = {
            "total_workflows": len(workflows),
            "status_breakdown": {},
            "recent_activity": [],
            "next_scheduled": []
        }
        
        # Count statuses
        for workflow in workflows:
            status = workflow["status"]
            report["status_breakdown"][status] = report["status_breakdown"].get(status, 0) + 1
        
        # Get recent activity
        for workflow in workflows:
            if workflow["last_run"]:
                report["recent_activity"].append({
                    "workflow_id": workflow["workflow_id"],
                    "last_run": workflow["last_run"],
                    "status": workflow["status"]
                })
        
        # Sort by last run time
        report["recent_activity"].sort(key=lambda x: x["last_run"], reverse=True)
        
        return report


def main():
    """Main function to run the daily automator"""
    parser = argparse.ArgumentParser(description="Daily Social Media Automator")
    parser.add_argument("--action", choices=["setup", "run", "status", "plan", "single"], 
                       default="run", help="Action to perform")
    parser.add_argument("--workflow-id", help="Workflow ID for single execution")
    parser.add_argument("--config", default="workflow_config.json", help="Configuration file path")
    
    args = parser.parse_args()
    
    automator = DailyAutomator(args.config)
    
    if args.action == "setup":
        logger.info("Setting up daily workflows...")
        automator.setup_daily_workflows()
        logger.info("Setup complete!")
        
    elif args.action == "run":
        logger.info("Starting daily automation...")
        automator.start_daily_automation()
        
    elif args.action == "status":
        report = automator.get_status_report()
        print("\n=== Daily Automator Status Report ===")
        print(f"Total Workflows: {report['total_workflows']}")
        print(f"Status Breakdown: {report['status_breakdown']}")
        print("\nRecent Activity:")
        for activity in report['recent_activity'][:5]:
            print(f"  {activity['workflow_id']}: {activity['status']} at {activity['last_run']}")
        
    elif args.action == "plan":
        logger.info("Generating weekly content plan...")
        plan = automator.generate_weekly_content_plan()
        print("\n=== Weekly Content Plan ===")
        for day_plan in plan:
            print(f"\n{day_plan['day']}: {day_plan['theme']}")
            for i, idea in enumerate(day_plan['content_ideas'], 1):
                print(f"  {i}. {idea}")
        
    elif args.action == "single":
        if not args.workflow_id:
            print("Error: --workflow-id is required for single execution")
            return
        
        logger.info(f"Running single workflow: {args.workflow_id}")
        results = automator.run_single_workflow(args.workflow_id)
        if results:
            print(f"Workflow completed successfully: {results}")
        else:
            print("Workflow failed")


if __name__ == "__main__":
    main() 