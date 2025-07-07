"""
Unified API Client System for We'll Be Right Back Automator
Manages different API clients with proper error handling and configuration
"""

import os
import requests
import json
import logging
from typing import Dict, List, Optional, Any, Union
from abc import ABC, abstractmethod
from datetime import datetime
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAPIClient(ABC):
    """Abstract base class for API clients"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = ""):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.rate_limit_delay = 1  # Default delay between requests
        
    @abstractmethod
    def make_request(self, endpoint: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """Make a request to the API"""
        pass
    
    def handle_rate_limit(self):
        """Handle rate limiting by adding delay"""
        time.sleep(self.rate_limit_delay)
    
    def validate_response(self, response: requests.Response) -> Dict[str, Any]:
        """Validate and parse API response"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise


class OpenAIClient(BaseAPIClient):
    """OpenAI API client for GPT models"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            api_key=api_key or os.getenv('API_KEY_OPENAI'),
            base_url="https://api.openai.com/v1"
        )
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def make_request(self, endpoint: str, method: str = "POST", **kwargs) -> Dict[str, Any]:
        """Make a request to OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            return self.validate_response(response)
        except Exception as e:
            logger.error(f"OpenAI API request failed: {e}")
            raise
    
    def generate_text(self, 
                     messages: List[Dict[str, str]], 
                     model: str = "gpt-3.5-turbo",
                     max_tokens: int = 1000,
                     temperature: float = 0.7) -> str:
        """Generate text using OpenAI's chat completion"""
        try:
            data = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = self.make_request("chat/completions", json=data)
            return response.get('choices', [{}])[0].get('message', {}).get('content', '')
            
        except Exception as e:
            logger.error(f"Text generation failed: {e}")
            return f"Error generating text: {str(e)}"


class GoogleAPIClient(BaseAPIClient):
    """Google API client for various Google services"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            api_key=api_key or os.getenv('API_KEY_GOOGLE'),
            base_url="https://www.googleapis.com"
        )
        
    def make_request(self, endpoint: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """Make a request to Google API"""
        if not self.api_key:
            raise ValueError("Google API key is required")
        
        # Add API key to params
        params = kwargs.get('params', {})
        params['key'] = self.api_key
        kwargs['params'] = params
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                **kwargs
            )
            return self.validate_response(response)
        except Exception as e:
            logger.error(f"Google API request failed: {e}")
            raise


class WeatherAPIClient(BaseAPIClient):
    """Weather API client (OpenWeatherMap)"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            api_key=api_key or os.getenv('API_KEY_WEATHER'),
            base_url="https://api.openweathermap.org/data/2.5"
        )
        
    def make_request(self, endpoint: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """Make a request to Weather API"""
        if not self.api_key:
            raise ValueError("Weather API key is required")
        
        # Add API key to params
        params = kwargs.get('params', {})
        params['appid'] = self.api_key
        kwargs['params'] = params
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                **kwargs
            )
            return self.validate_response(response)
        except Exception as e:
            logger.error(f"Weather API request failed: {e}")
            raise
    
    def get_weather(self, city: str, country_code: str = "US") -> Dict[str, Any]:
        """Get weather information for a city"""
        try:
            params = {
                'q': f"{city},{country_code}",
                'units': 'metric'
            }
            
            response = self.make_request("weather", params=params)
            return response
            
        except Exception as e:
            logger.error(f"Weather lookup failed: {e}")
            return {"error": f"Weather lookup failed: {str(e)}"}


class APIClientManager:
    """Manager class for handling multiple API clients"""
    
    def __init__(self):
        self.clients: Dict[str, BaseAPIClient] = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize all available API clients"""
        try:
            # Initialize OpenAI client
            if os.getenv('API_KEY_OPENAI'):
                self.clients['openai'] = OpenAIClient()
                logger.info("OpenAI client initialized")
            else:
                logger.warning("OpenAI API key not found")
            
            # Initialize Google client
            if os.getenv('API_KEY_GOOGLE'):
                self.clients['google'] = GoogleAPIClient()
                logger.info("Google client initialized")
            else:
                logger.warning("Google API key not found")
            
            # Initialize Weather client
            if os.getenv('API_KEY_WEATHER'):
                self.clients['weather'] = WeatherAPIClient()
                logger.info("Weather client initialized")
            else:
                logger.warning("Weather API key not found")
                
        except Exception as e:
            logger.error(f"Error initializing API clients: {e}")
    
    def get_client(self, client_name: str) -> Optional[BaseAPIClient]:
        """Get a specific API client by name"""
        return self.clients.get(client_name.lower())
    
    def add_client(self, name: str, client: BaseAPIClient):
        """Add a new API client"""
        self.clients[name.lower()] = client
        logger.info(f"Added {name} client")
    
    def remove_client(self, name: str):
        """Remove an API client"""
        if name.lower() in self.clients:
            del self.clients[name.lower()]
            logger.info(f"Removed {name} client")
    
    def list_clients(self) -> List[str]:
        """List all available clients"""
        return list(self.clients.keys())
    
    def test_connection(self, client_name: str) -> bool:
        """Test connection to a specific API client"""
        client = self.get_client(client_name)
        if not client:
            logger.error(f"Client {client_name} not found")
            return False
        
        try:
            if isinstance(client, OpenAIClient):
                # Test with a simple prompt
                response = client.generate_text(
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=10
                )
                return "Error" not in response
            elif isinstance(client, WeatherAPIClient):
                # Test with a simple weather lookup
                response = client.get_weather("London", "UK")
                return "error" not in response
            else:
                # Generic test for other clients
                return True
        except Exception as e:
            logger.error(f"Connection test failed for {client_name}: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all API clients"""
        status = {
            "total_clients": len(self.clients),
            "available_clients": self.list_clients(),
            "client_status": {}
        }
        
        for name, client in self.clients.items():
            status["client_status"][name] = {
                "initialized": True,
                "api_key_present": bool(client.api_key),
                "connection_test": self.test_connection(name)
            }
        
        return status


# Convenience functions for easy access
def get_openai_client() -> Optional[OpenAIClient]:
    """Get OpenAI client instance"""
    manager = APIClientManager()
    return manager.get_client('openai')

def get_google_client() -> Optional[GoogleAPIClient]:
    """Get Google client instance"""
    manager = APIClientManager()
    return manager.get_client('google')

def get_weather_client() -> Optional[WeatherAPIClient]:
    """Get Weather client instance"""
    manager = APIClientManager()
    return manager.get_client('weather')

def get_api_manager() -> APIClientManager:
    """Get API client manager instance"""
    return APIClientManager()


# Example usage and testing
if __name__ == "__main__":
    # Test the API client system
    manager = APIClientManager()
    
    print("🔌 API Client System Test")
    print("=" * 40)
    
    # Show available clients
    print(f"Available clients: {manager.list_clients()}")
    
    # Show status
    status = manager.get_status()
    print(f"Total clients: {status['total_clients']}")
    
    # Test each client
    for client_name in manager.list_clients():
        print(f"\nTesting {client_name} client...")
        if manager.test_connection(client_name):
            print(f"✅ {client_name} connection successful")
        else:
            print(f"❌ {client_name} connection failed")
    
    print("\n✅ API Client System initialized!")


class SocialMediaClient(ABC):
    """Generic base class for social media clients"""
    def __init__(self, api_key: Optional[str] = None, access_token: Optional[str] = None):
        self.api_key = api_key
        self.access_token = access_token
        self.connected = False

    @abstractmethod
    def connect(self) -> bool:
        """Connect/authenticate to the social media platform"""
        pass

    @abstractmethod
    def post(self, content: str, **kwargs) -> Any:
        """Post content to the platform"""
        pass

    @abstractmethod
    def get_stats(self, post_id: str) -> Dict[str, Any]:
        """Get statistics/analytics for a post"""
        pass

    def is_connected(self) -> bool:
        return self.connected

# Example implementation for Twitter (pseudo-implementation)
class TwitterClient(SocialMediaClient):
    """Twitter API client (example)"""
    def __init__(self, api_key: Optional[str] = None, access_token: Optional[str] = None):
        super().__init__(api_key, access_token)
        self.base_url = "https://api.twitter.com/2"

    def connect(self) -> bool:
        # Pseudo-authentication logic (replace with real OAuth2 flow)
        if self.api_key and self.access_token:
            self.connected = True
            logger.info("Connected to Twitter API")
            return True
        logger.warning("Twitter API key or access token missing")
        return False

    def post(self, content: str, **kwargs) -> Dict[str, Any]:
        if not self.connected:
            raise RuntimeError("Not connected to Twitter API")
        # Pseudo-post logic (replace with real API call)
        logger.info(f"Posting to Twitter: {content}")
        return {"status": "success", "content": content, "platform": "twitter"}

    def get_stats(self, post_id: str) -> Dict[str, Any]:
        if not self.connected:
            raise RuntimeError("Not connected to Twitter API")
        # Pseudo-get stats logic (replace with real API call)
        logger.info(f"Getting stats for Twitter post: {post_id}")
        return {"post_id": post_id, "likes": 42, "retweets": 7, "replies": 3} 