"""
Example of how to securely load API keys from a .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Method 1: Direct access to environment variables
def get_api_key_direct():
    """Get API key directly from environment variable"""
    api_key = os.getenv('API_KEY_OPENAI')
    if not api_key:
        raise ValueError("API_KEY_OPENAI not found in environment variables")
    return api_key

# Method 2: Using a configuration class
class Config:
    """Configuration class to manage all environment variables"""
    
    def __init__(self):
        # Load .env file
        load_dotenv()
        
        # API Keys
        self.openai_api_key = os.getenv('API_KEY_OPENAI')
        self.google_api_key = os.getenv('API_KEY_GOOGLE')
        self.weather_api_key = os.getenv('API_KEY_WEATHER')
        
        # Database configuration
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = int(os.getenv('DB_PORT', 5432))
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        
        # Email configuration
        self.email_host = os.getenv('EMAIL_HOST')
        self.email_port = int(os.getenv('EMAIL_PORT', 587))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        
        # Other settings
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    def validate_required_keys(self):
        """Validate that all required API keys are present"""
        required_keys = [
            'openai_api_key',
            'google_api_key',
            'weather_api_key'
        ]
        
        missing_keys = []
        for key in required_keys:
            if not getattr(self, key):
                missing_keys.append(key)
        
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
        
        return True

# Method 3: Using a function-based approach
def load_config():
    """Load configuration from environment variables"""
    load_dotenv()
    
    config = {
        'api_keys': {
            'openai': os.getenv('API_KEY_OPENAI'),
            'google': os.getenv('API_KEY_GOOGLE'),
            'weather': os.getenv('API_KEY_WEATHER')
        },
        'database': {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'name': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        },
        'email': {
            'host': os.getenv('EMAIL_HOST'),
            'port': int(os.getenv('EMAIL_PORT', 587)),
            'user': os.getenv('EMAIL_USER'),
            'password': os.getenv('EMAIL_PASSWORD')
        },
        'settings': {
            'debug': os.getenv('DEBUG', 'False').lower() == 'true',
            'log_level': os.getenv('LOG_LEVEL', 'INFO')
        }
    }
    
    return config

# Example usage
if __name__ == "__main__":
    try:
        # Method 1: Direct access
        api_key = get_api_key_direct()
        print(f"OpenAI API Key loaded: {api_key[:10]}...")
        
        # Method 2: Using Config class
        config = Config()
        config.validate_required_keys()
        print(f"Google API Key loaded: {config.google_api_key[:10]}...")
        
        # Method 3: Using function-based approach
        app_config = load_config()
        print(f"Weather API Key loaded: {app_config['api_keys']['weather'][:10]}...")
        
        print("All API keys loaded successfully!")
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please check your .env file and ensure all required API keys are set.") 