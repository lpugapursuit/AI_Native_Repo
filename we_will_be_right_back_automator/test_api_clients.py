#!/usr/bin/env python3
"""
Test script for the unified API client system
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from api_clients import APIClientManager, get_openai_client, get_google_client, get_weather_client

def test_api_client_system():
    """Test the unified API client system"""
    
    print("🔌 Testing Unified API Client System")
    print("=" * 50)
    
    # Test 1: Initialize manager
    print("\n1. Initializing API Client Manager...")
    manager = APIClientManager()
    
    # Test 2: List available clients
    print(f"\n2. Available clients: {manager.list_clients()}")
    
    # Test 3: Get status
    print("\n3. Client Status:")
    status = manager.get_status()
    print(f"   Total clients: {status['total_clients']}")
    
    for client_name, client_status in status['client_status'].items():
        print(f"   {client_name}:")
        print(f"     - Initialized: {client_status['initialized']}")
        print(f"     - API Key Present: {client_status['api_key_present']}")
        print(f"     - Connection Test: {client_status['connection_test']}")
    
    # Test 4: Test individual client getters
    print("\n4. Testing individual client getters...")
    
    openai_client = get_openai_client()
    if openai_client:
        print("   ✅ OpenAI client retrieved successfully")
    else:
        print("   ❌ OpenAI client not available")
    
    google_client = get_google_client()
    if google_client:
        print("   ✅ Google client retrieved successfully")
    else:
        print("   ❌ Google client not available")
    
    weather_client = get_weather_client()
    if weather_client:
        print("   ✅ Weather client retrieved successfully")
    else:
        print("   ❌ Weather client not available")
    
    # Test 5: Test client operations
    print("\n5. Testing client operations...")
    
    if openai_client:
        try:
            # Test with a simple prompt (will fail without real API key, but tests structure)
            response = openai_client.generate_text(
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            print(f"   OpenAI test response: {response[:50]}...")
        except Exception as e:
            print(f"   OpenAI test (expected error): {str(e)[:50]}...")
    
    if weather_client:
        try:
            # Test weather lookup (will fail without real API key, but tests structure)
            response = weather_client.get_weather("London", "UK")
            print(f"   Weather test response: {response}")
        except Exception as e:
            print(f"   Weather test (expected error): {str(e)[:50]}...")
    
    print("\n✅ API Client System test completed!")
    print("\n📝 To use with real APIs:")
    print("1. Add your API keys to .env file:")
    print("   API_KEY_OPENAI=your_openai_key")
    print("   API_KEY_GOOGLE=your_google_key")
    print("   API_KEY_WEATHER=your_weather_key")
    print("2. Run this test again to verify connections")

if __name__ == "__main__":
    test_api_client_system() 