"""
Test script for the daily automation system
Demonstrates how to set up and run automated workflows
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from we_will_be_right_back_automator.src.daily_automator import DailyAutomator
from we_will_be_right_back_automator.src.workflow_manager import WorkflowManager

def test_workflow_creation():
    """Test creating and running workflows"""
    print("=== Testing Workflow Creation ===")
    
    # Initialize the automator
    automator = DailyAutomator("test_workflow_config.json")
    
    # Create a test workflow
    workflow_id = automator.workflow_manager.create_daily_workflow(
        platforms=["twitter", "instagram"],
        schedule_time="14:30",
        content_prompt="AI trying to understand human coffee habits"
    )
    
    print(f"Created workflow: {workflow_id}")
    
    # Run the workflow immediately
    print("\n=== Running Workflow ===")
    results = automator.run_single_workflow(workflow_id)
    
    if results:
        print("Workflow executed successfully!")
        print(f"Content generated for {len(results['content_generation'])} platforms")
        print(f"Posted to {len(results['posting_results'])} platforms")
        
        if results['errors']:
            print(f"Errors encountered: {results['errors']}")
    else:
        print("Workflow failed!")
    
    return workflow_id

def test_weekly_planning():
    """Test weekly content planning"""
    print("\n=== Testing Weekly Content Planning ===")
    
    automator = DailyAutomator()
    plan = automator.generate_weekly_content_plan()
    
    print("Weekly content plan generated:")
    for day_plan in plan:
        print(f"\n{day_plan['day']}: {day_plan['theme']}")
        for i, idea in enumerate(day_plan['content_ideas'], 1):
            print(f"  {i}. {idea}")

def test_status_reporting():
    """Test status reporting"""
    print("\n=== Testing Status Reporting ===")
    
    automator = DailyAutomator()
    report = automator.get_status_report()
    
    print(f"Total Workflows: {report['total_workflows']}")
    print(f"Status Breakdown: {report['status_breakdown']}")
    
    if report['recent_activity']:
        print("\nRecent Activity:")
        for activity in report['recent_activity'][:3]:
            print(f"  {activity['workflow_id']}: {activity['status']}")

def test_setup_daily_workflows():
    """Test setting up default daily workflows"""
    print("\n=== Testing Daily Workflow Setup ===")
    
    automator = DailyAutomator("daily_workflows_config.json")
    workflow_ids = automator.setup_daily_workflows()
    
    print(f"Created {len(workflow_ids)} daily workflows:")
    for workflow_id in workflow_ids:
        print(f"  - {workflow_id}")

def main():
    """Main test function"""
    print("🚀 Testing Daily Social Media Automation System")
    print("=" * 50)
    
    try:
        # Test 1: Workflow creation and execution
        workflow_id = test_workflow_creation()
        
        # Test 2: Weekly content planning
        test_weekly_planning()
        
        # Test 3: Status reporting
        test_status_reporting()
        
        # Test 4: Daily workflow setup
        test_setup_daily_workflows()
        
        print("\n✅ All tests completed successfully!")
        print("\nTo run the automation system:")
        print("1. Set up your API keys in a .env file")
        print("2. Run: python src/daily_automator.py --action setup")
        print("3. Run: python src/daily_automator.py --action run")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 