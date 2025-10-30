"""
Simple test script for SportsBlaze NBA API
Easily modify the variables below to test different configurations
"""

import requests
import json

# CONFIGURATION - Modify these variables based on the documentation
API_KEY = "sbfzua9rcwzj09qtc9ouzl3"
BASE_URL = "https://api.sportsblaze.com/nba/v1"
ENDPOINT = "boxscores/daily/2024-10-30.json"

# Different ways to pass the API key - try one at a time
AUTH_IN_QUERY = True  # Set to True to pass key as query parameter
AUTH_IN_HEADER = False  # Set to True to pass key in header

def test_simple_request():
    """Test a simple API request with current configuration."""

    url = f"{BASE_URL}/{ENDPOINT}"

    params = {}
    headers = {}

    if AUTH_IN_QUERY:
        # Try different query parameter names
        params['key'] = API_KEY
        # Uncomment to try other parameter names:
        # params['apikey'] = API_KEY
        # params['api_key'] = API_KEY

    if AUTH_IN_HEADER:
        # Try different header names
        headers['X-API-Key'] = API_KEY
        # Uncomment to try other header formats:
        # headers['Authorization'] = f'Bearer {API_KEY}'
        # headers['api-key'] = API_KEY

    print(f"Testing URL: {url}")
    print(f"Query params: {params}")
    print(f"Headers: {headers}")
    print("-" * 60)

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"\nResponse Body:")

        if response.status_code == 200:
            # Success!
            print("✓ SUCCESS!")
            data = response.json()
            print(json.dumps(data, indent=2))
        else:
            # Error
            print(f"✗ Error: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def test_alternative_endpoints():
    """Test several alternative endpoint formats."""

    endpoints = [
        "boxscores/daily/2024-10-30.json",
        "games/daily/2024-10-30.json",
        "schedule/daily/2024-10-30.json",
        "daily/2024-10-30.json",
        "boxscores/2024-10-30.json",
    ]

    print("\nTesting alternative endpoints...")
    print("=" * 60)

    for endpoint in endpoints:
        url = f"{BASE_URL}/{endpoint}"
        params = {'key': API_KEY}

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                print(f"✓ SUCCESS: {endpoint}")
                print(json.dumps(response.json(), indent=2)[:200])
                return
            else:
                print(f"✗ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"✗ {endpoint}: {type(e).__name__}")

    print("\nNo working endpoint found.")

if __name__ == "__main__":
    print("SportsBlaze NBA API Simple Test")
    print("=" * 60)
    print()

    # Test the main configuration
    test_simple_request()

    print("\n")

    # Uncomment to test alternative endpoints
    # test_alternative_endpoints()

    print("\n" + "=" * 60)
    print("Instructions:")
    print("1. Check the SportsBlaze documentation for the correct endpoint")
    print("2. Verify your API key is active and has NBA access")
    print("3. Modify the variables at the top of this script")
    print("4. Run again: python test_sportsblaze_simple.py")
