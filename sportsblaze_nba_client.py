"""
SportsBlaze NBA API Client
Connects to the SportsBlaze API to fetch NBA daily boxscores and game data.
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json


class SportsBlazeNBAClient:
    """Client for interacting with the SportsBlaze NBA API."""

    def __init__(self, api_key: str):
        """
        Initialize the SportsBlaze NBA API client.

        Args:
            api_key: Your SportsBlaze API key
        """
        self.api_key = api_key
        self.base_url = "https://api.sportsblaze.com/nba/v1"
        self.session = requests.Session()

        # Set browser-like headers to avoid API blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://docs.sportsblaze.com/',
        })

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a request to the SportsBlaze API.

        Args:
            endpoint: API endpoint path
            params: Additional query parameters

        Returns:
            JSON response as a dictionary

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        if params is None:
            params = {}

        # Add API key to query parameters
        params['key'] = self.api_key

        url = f"{self.base_url}/{endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {response.text}")
            print(f"URL attempted: {response.url}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise

    def get_daily_boxscores(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get daily boxscores for NBA games.

        Args:
            date: Date in YYYY-MM-DD format (defaults to today)

        Returns:
            Dictionary containing boxscore data
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        endpoint = f"boxscores/daily/{date}.json"
        return self._make_request(endpoint)

    def get_date_range_boxscores(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Get boxscores for a range of dates.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            List of boxscore data for each date
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        results = []
        current = start

        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            try:
                data = self.get_daily_boxscores(date_str)
                results.append({
                    'date': date_str,
                    'data': data
                })
            except Exception as e:
                print(f"Error fetching data for {date_str}: {e}")

            current += timedelta(days=1)

        return results

    def get_game_boxscore(self, game_id: str) -> Dict[str, Any]:
        """
        Get boxscore for a specific game.

        Args:
            game_id: The game ID

        Returns:
            Dictionary containing game boxscore data
        """
        endpoint = f"boxscores/{game_id}.json"
        return self._make_request(endpoint)

    def print_daily_summary(self, date: Optional[str] = None):
        """
        Print a formatted summary of daily games.

        Args:
            date: Date in YYYY-MM-DD format (defaults to today)
        """
        data = self.get_daily_boxscores(date)

        if date:
            print(f"\n{'='*60}")
            print(f"NBA Games for {date}")
            print(f"{'='*60}\n")
        else:
            print(f"\n{'='*60}")
            print(f"NBA Games for Today")
            print(f"{'='*60}\n")

        # The exact structure depends on the API response
        # This is a flexible printer that handles various response formats
        print(json.dumps(data, indent=2))


def test_api_configurations():
    """Test different API endpoint and authentication configurations."""
    API_KEY = "sbfzua9rcwzj09qtc9ouzl3"
    date = "2024-10-30"

    # Different base URLs to try
    base_urls = [
        "https://api.sportsblaze.com/nba/v1",
        "https://api.sportsblaze.com/nba",
        "https://api.sportsblaze.com/v1/nba",
    ]

    # Different endpoint patterns
    endpoint_patterns = [
        f"boxscores/daily/{date}.json",
        f"boxscores/daily/{date}",
        f"games/daily/{date}.json",
        f"games/daily/{date}",
        f"schedule/daily/{date}.json",
        f"daily/{date}/boxscores.json",
        f"daily-boxscores/{date}.json",
    ]

    # Authentication methods
    auth_methods = ["query", "header", "both"]

    print("Testing different API configurations...\n")

    for base_url in base_urls:
        for endpoint in endpoint_patterns:
            for auth_method in auth_methods:
                url = f"{base_url}/{endpoint}"
                try:
                    print(f"Trying: {url} with auth: {auth_method}")

                    params = {}
                    headers = {}

                    if auth_method in ["query", "both"]:
                        params['key'] = API_KEY

                    if auth_method in ["header", "both"]:
                        headers['X-API-Key'] = API_KEY

                    response = requests.get(url, params=params, headers=headers, timeout=10)

                    if response.status_code == 200:
                        print(f"✓ SUCCESS! Found working configuration:")
                        print(f"  Base URL: {base_url}")
                        print(f"  Endpoint: {endpoint}")
                        print(f"  Auth method: {auth_method}")
                        print(f"\nResponse preview:")
                        print(json.dumps(response.json(), indent=2)[:500])
                        return base_url, endpoint, auth_method
                    else:
                        print(f"  Status: {response.status_code}")

                except Exception as e:
                    print(f"  Error: {type(e).__name__}")

    print("\nNo working configuration found.")
    return None, None, None


def main():
    """Example usage of the SportsBlaze NBA API client."""

    # Initialize the client with your API key
    API_KEY = "sbfzua9rcwzj09qtc9ouzl3"
    client = SportsBlazeNBAClient(API_KEY)

    # Example 1: Get today's boxscores
    print("Fetching today's NBA boxscores...")
    try:
        today_data = client.get_daily_boxscores()
        print("\nToday's Data:")
        print(json.dumps(today_data, indent=2))
    except Exception as e:
        print(f"Error fetching today's data: {e}")

    # Example 2: Get boxscores for a specific date
    print("\n" + "="*60)
    print("Fetching NBA boxscores for 2025-10-29...")
    try:
        specific_date_data = client.get_daily_boxscores("2025-10-29")
        client.print_daily_summary("2025-10-29")
    except Exception as e:
        print(f"Error fetching data for specific date: {e}")

    # Example 3: Get boxscores for a date range
    print("\n" + "="*60)
    print("Fetching NBA boxscores for date range (2025-10-27 to 2025-10-29)...")
    try:
        # Uncomment to test with a date range
        range_data = client.get_date_range_boxscores("2025-10-27", "2025-10-29")
        print(f"\nFetched data for {len(range_data)} dates")
        for item in range_data:
            print(f"\nDate: {item['date']}")
            if 'data' in item and 'games' in item['data']:
                print(f"  Games: {len(item['data']['games'])}")
    except Exception as e:
        print(f"Error fetching date range: {e}")


if __name__ == "__main__":
    import sys

    # Run in test mode to find the correct API configuration
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_api_configurations()
    else:
        main()
