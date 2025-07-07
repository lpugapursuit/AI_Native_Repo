# Daily Social Media Automation System

A comprehensive AI-powered automation system for creating and posting content across multiple social media platforms daily. Built specifically for the "We'll Be Right Back" AI comedy series with deadpan, absurdist humor.

## 🚀 Features

### 🤖 AI-Powered Content Generation
- **Intelligent Copywriting**: Uses OpenAI GPT models to generate platform-specific content
- **Brand Voice Consistency**: Maintains deadpan, absurdist humor across all platforms
- **Contextual Content**: Generates content based on daily themes and prompts
- **Multi-Platform Optimization**: Tailors content for each social media platform

### 📅 Automated Scheduling
- **Daily Workflows**: Automatically creates and manages daily posting schedules
- **Flexible Timing**: Customizable posting times for each platform
- **Smart Scheduling**: Intelligent scheduling based on platform best practices
- **Workflow Management**: Create, edit, and monitor multiple workflows

### 📱 Multi-Platform Support
- **Twitter**: Tweet generation and posting
- **Instagram**: Posts and stories with optimized captions and hashtags
- **TikTok**: Video uploads and caption generation
- **YouTube**: Video uploads with titles, descriptions, and tags
- **LinkedIn**: Professional posts and articles
- **Facebook**: Posts and page management

### 📊 Analytics & Monitoring
- **Status Reporting**: Real-time workflow status and execution history
- **Performance Tracking**: Monitor engagement across platforms
- **Error Handling**: Comprehensive error logging and recovery
- **Content Analytics**: Track what content performs best

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- Social media platform API keys and access tokens

### Setup

1. **Clone the repository**
   ```bash
   cd we_will_be_right_back_automator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env with your API keys
   ```

4. **Set up your API keys**
   - OpenAI API key for content generation
   - Social media platform API keys and access tokens
   - See `env_example.txt` for all required variables

## 🎯 Quick Start

### 1. Set Up Daily Workflows
```bash
python src/daily_automator.py --action setup
```

This creates 4 daily workflows:
- **9:00 AM**: Twitter + Instagram (Morning AI humor)
- **12:00 PM**: Twitter + LinkedIn (Lunch break with AI)
- **3:00 PM**: Twitter + Instagram + TikTok (Afternoon AI chaos)
- **6:00 PM**: Twitter + Facebook (Evening AI reflections)

### 2. Generate Weekly Content Plan
```bash
python src/daily_automator.py --action plan
```

Creates a weekly content plan with themed content for each day.

### 3. Start Daily Automation
```bash
python src/daily_automator.py --action run
```

Starts the scheduler to automatically run workflows at their scheduled times.

### 4. Check Status
```bash
python src/daily_automator.py --action status
```

View the status of all workflows and recent activity.

## 📋 Usage Examples

### Create a Custom Workflow
```python
from src.daily_automator import DailyAutomator

automator = DailyAutomator()

# Create a custom workflow
workflow_id = automator.workflow_manager.create_daily_workflow(
    platforms=["twitter", "instagram", "tiktok"],
    schedule_time="14:30",
    content_prompt="AI trying to understand human coffee habits"
)

# Run immediately
results = automator.run_single_workflow(workflow_id)
```

### Generate Weekly Content Plan
```python
# Generate content ideas for the week
plan = automator.generate_weekly_content_plan()

for day_plan in plan:
    print(f"{day_plan['day']}: {day_plan['theme']}")
    for idea in day_plan['content_ideas']:
        print(f"  - {idea}")
```

### Monitor Workflows
```python
# Get status report
report = automator.get_status_report()
print(f"Total workflows: {report['total_workflows']}")
print(f"Status breakdown: {report['status_breakdown']}")
```

## 🏗️ Architecture

### Core Components

1. **DailyAutomator** (`src/daily_automator.py`)
   - Main orchestration class
   - Manages workflow setup and execution
   - Handles scheduling and monitoring

2. **WorkflowManager** (`src/workflow_manager.py`)
   - Manages individual workflows
   - Handles content generation and posting
   - Provides workflow lifecycle management

3. **CopywritingAgent** (`src/copywriting_agent.py`)
   - AI-powered content generation
   - Platform-specific content optimization
   - Brand voice consistency

4. **Social Media Clients** (`clients/`)
   - Platform-specific API clients
   - Handles posting and engagement
   - Error handling and rate limiting

### Workflow Structure

```
ContentWorkflow
├── workflow_id: Unique identifier
├── content_type: "daily_post" | "video_upload" | "engagement"
├── platforms: List of target platforms
├── schedule_time: Daily execution time (HH:MM)
├── brand_voice: Brand voice guidelines
├── content_prompt: Content generation prompt
├── generated_content: Platform-specific content
└── posting_results: Posting results and analytics
```

## 🎨 Brand Voice Configuration

The system is configured for the "We'll Be Right Back" AI comedy series with:

- **Tone**: Deadpan, absurdist, sarcastic
- **Style**: Understated, ironic, subtly chaotic
- **Personality**: Sarcastic AI trying to understand humans
- **Call-to-Action**: Subscribe-focused
- **Series Name**: "We'll Be Right Back"

### Platform-Specific Optimization

Each platform gets optimized content:

- **Twitter**: Concise, deadpan tweets with relevant hashtags
- **Instagram**: Visual-first captions with strategic hashtag placement
- **TikTok**: Trend-aware but maintaining deadpan absurdist voice
- **YouTube**: Clickbait titles with deadpan humor, detailed descriptions
- **LinkedIn**: Professional but absurdist, industry insights with dry humor
- **Facebook**: Shareable content with engagement-focused calls-to-action

## 🔧 Configuration

### Environment Variables

Required API keys and tokens:

```bash
# OpenAI for content generation
API_KEY_OPENAI=your_openai_api_key

# Social Media Platforms
TWITTER_API_KEY=your_twitter_api_key
TWITTER_ACCESS_TOKEN=your_twitter_access_token

YOUTUBE_API_KEY=your_youtube_api_key
YOUTUBE_ACCESS_TOKEN=your_youtube_access_token

INSTAGRAM_API_KEY=your_instagram_api_key
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token

TIKTOK_API_KEY=your_tiktok_api_key
TIKTOK_ACCESS_TOKEN=your_tiktok_access_token

LINKEDIN_API_KEY=your_linkedin_api_key
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token

FACEBOOK_API_KEY=your_facebook_api_key
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
```

### Workflow Configuration

Workflows are stored in JSON format:

```json
{
  "workflow_id": {
    "content_type": "daily_post",
    "platforms": ["twitter", "instagram"],
    "schedule_time": "09:00",
    "brand_voice": {
      "tone": "deadpan",
      "style": "absurdist",
      "personality": "sarcastic"
    },
    "content_prompt": "Morning AI humor",
    "status": "completed",
    "last_run": "2024-01-15T09:00:00",
    "generated_content": {...},
    "posting_results": {...}
  }
}
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
python test_daily_automation.py
```

This will test:
- Workflow creation and execution
- Content generation
- Weekly planning
- Status reporting
- Daily workflow setup

## 📊 Monitoring & Analytics

### Log Files
- `daily_automator.log`: Main application logs
- `workflow_config.json`: Workflow configuration and history

### Status Commands
```bash
# View workflow status
python src/daily_automator.py --action status

# Check specific workflow
python src/daily_automator.py --action single --workflow-id WORKFLOW_ID
```

### Metrics Tracked
- Workflow execution success/failure rates
- Content generation performance
- Platform posting results
- Error rates and types
- Engagement metrics (when available)

## 🔒 Security & Best Practices

### API Key Management
- Store API keys in environment variables
- Never commit API keys to version control
- Use `.env` files for local development
- Rotate API keys regularly

### Rate Limiting
- Built-in rate limiting for API calls
- Respects platform-specific limits
- Automatic retry logic for failed requests

### Error Handling
- Comprehensive error logging
- Graceful failure handling
- Automatic workflow recovery
- Detailed error reporting

## 🚀 Deployment

### Local Development
```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_daily_automation.py

# Start automation
python src/daily_automator.py --action run
```

### Production Deployment
1. Set up a server with Python 3.8+
2. Install dependencies
3. Configure environment variables
4. Set up cron job or systemd service
5. Monitor logs and performance

### Docker Deployment (Coming Soon)
```bash
# Build and run with Docker
docker build -t daily-automator .
docker run -d --env-file .env daily-automator
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the logs in `daily_automator.log`
2. Review the configuration files
3. Run the test suite
4. Create an issue with detailed information

---

**Happy automating! 🤖📱** 