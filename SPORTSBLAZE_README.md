# SportsBlaze NBA API Client

A Python client for connecting to the SportsBlaze NBA API to fetch daily boxscores and game data.

## Files

- `sportsblaze_nba_client.py` - Main API client with comprehensive functionality
- `requirements.txt` - Python dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from sportsblaze_nba_client import SportsBlazeNBAClient

# Initialize the client
client = SportsBlazeNBAClient(api_key="your_api_key_here")

# Get today's boxscores
data = client.get_daily_boxscores()

# Get boxscores for a specific date
data = client.get_daily_boxscores("2024-10-30")

# Get boxscores for a date range
range_data = client.get_date_range_boxscores("2024-10-28", "2024-10-30")

# Print formatted summary
client.print_daily_summary("2024-10-30")
```

### Running the Examples

```bash
# Run the main examples
python sportsblaze_nba_client.py

# Run API configuration test mode
python sportsblaze_nba_client.py test
```

## Features

- Fetch daily NBA boxscores
- Get boxscores for specific dates
- Retrieve data for date ranges
- Support for multiple authentication methods
- Comprehensive error handling
- Flexible endpoint detection

## Current Issue: API Key Access Denied

The API key `sbfzua9rcwzj09qtc9ouzl3` is returning "Access denied" (403) for both NFL and NBA endpoints.

**Confirmed Endpoint Format:**
```
https://api.sportsblaze.com/nba/v1/boxscores/daily/{date}.json?key={api_key}
```

### Tested:
- ✓ Endpoint format is correct (matches NFL pattern)
- ✓ Multiple dates tested (2024-10-22 through 2025-02-09)
- ✗ Both NFL and NBA endpoints return 403
- ✗ Response: "Access denied"

### Possible Causes:

1. **API Key Not Activated**
   - The API key may need to be activated in your SportsBlaze account
   - New API keys sometimes require email verification or account setup

2. **API Key Invalid or Expired**
   - The API key may have expired
   - The API key may have been regenerated

3. **Subscription or Access Issue**
   - The API key may not have an active subscription
   - Your account may need to purchase API access
   - The API key may be limited to specific sports

4. **IP Restrictions**
   - The API may have IP whitelist restrictions
   - Check if your IP needs to be added to allowed list

### Troubleshooting Steps:

1. **Verify API Key**
   - Log in to your SportsBlaze account at www.sportsblaze.com
   - Check that your API key is active and has NBA access
   - Verify the API key is copied correctly (no extra spaces)

2. **Check Documentation**
   - Visit https://docs.sportsblaze.com/nba/core_endpoints/daily_boxscores
   - Look for the exact endpoint format
   - Check the authentication method (query parameter vs header)
   - Note any additional required parameters

3. **Test with cURL**
   ```bash
   # Test the endpoint directly
   curl -X GET "https://api.sportsblaze.com/nba/v1/boxscores/daily/2024-10-30.json?key=YOUR_API_KEY"
   ```

4. **Contact SportsBlaze Support**
   - If the API key is valid but still not working
   - They can verify your account permissions and endpoint access

## API Endpoints Tested

The client tested multiple endpoint patterns:

- `https://api.sportsblaze.com/nba/v1/boxscores/daily/{date}.json`
- `https://api.sportsblaze.com/nba/v1/games/daily/{date}.json`
- `https://api.sportsblaze.com/nba/v1/schedule/daily/{date}.json`
- Various other combinations

All returned 403 status codes with the provided API key.

## Next Steps

Once you have:
1. Verified your API key is correct
2. Confirmed the exact endpoint from the documentation
3. Checked your account has NBA access

You can update the client:

```python
# Update the base URL or endpoint pattern if needed
client.base_url = "https://api.sportsblaze.com/nba/v1"  # Update as needed
```

Or modify the `_make_request` method to match the exact authentication format from the documentation.

## License

This client was created for connecting to the SportsBlaze NBA API as requested.
