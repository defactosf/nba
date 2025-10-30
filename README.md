# NBA Data Scraper

A command-line tool to scrape historical NBA data using the [nba_api](https://github.com/swar/nba_api) library.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

The scraper provides several commands to fetch different types of NBA data:

### Fetch Player Stats with Minimum Minutes Filter

Get all players who have played at least a specified number of minutes in the current season:

```bash
# Fetch players with at least 15 minutes of game time in 2024-25 season
python fetch_player_stats.py --season 2024-25 --min-minutes 15

# Export as CSV
python fetch_player_stats.py --season 2024-25 --min-minutes 15 --format csv

# Custom minimum minutes threshold
python fetch_player_stats.py --season 2024-25 --min-minutes 100
```

This will:
- Pull all player statistics for the specified season
- Filter to only players with at least the specified minutes played
- Display a summary and top 10 players by minutes
- Save results to the `data/` directory with a timestamp

### List All NBA Teams

```bash
python scraper.py list-teams
```

### Search for a Player

```bash
python scraper.py search-player --player-name "LeBron James"
```

### Scrape All Games for a Season

```bash
python scraper.py games --season 2023-24
```

### Scrape Games for a Specific Team

```bash
python scraper.py games --season 2023-24 --team-abbr LAL
```

### Scrape All Players for a Season

```bash
python scraper.py players --season 2023-24
```

### Scrape Player Statistics

First, find the player ID:
```bash
python scraper.py search-player --player-name "Stephen Curry"
```

Then scrape their stats:
```bash
python scraper.py player-stats --player-id 201939 --season 2023-24
```

### Scrape Team Statistics

First, list teams to get the team ID:
```bash
python scraper.py list-teams
```

Then scrape team stats:
```bash
python scraper.py team-stats --team-id 1610612744 --season 2023-24
```

### Scrape League Standings

```bash
python scraper.py standings --season 2023-24
```

## Output Formats

Data can be exported as JSON (default) or CSV:

```bash
python scraper.py games --season 2023-24 --format json
python scraper.py games --season 2023-24 --format csv
```

## Output Directory

By default, data is saved to the `data/` directory. You can specify a different location:

```bash
python scraper.py games --season 2023-24 --output-dir my_data
```

## Season Format

Seasons should be specified in the format: `YYYY-YY` (e.g., `2023-24`, `2022-23`, `2021-22`)

## Common Team Abbreviations

- LAL - Los Angeles Lakers
- BOS - Boston Celtics
- GSW - Golden State Warriors
- MIA - Miami Heat
- CHI - Chicago Bulls
- NYK - New York Knicks
- BKN - Brooklyn Nets
- PHI - Philadelphia 76ers
- MIL - Milwaukee Bucks
- DEN - Denver Nuggets

Use `python scraper.py list-teams` to see all teams.

## Examples

### Scrape all Lakers games from 2022-23 season
```bash
python scraper.py games --season 2022-23 --team-abbr LAL --format csv
```

### Get player stats for Kevin Durant
```bash
# First find the player ID
python scraper.py search-player --player-name "Kevin Durant"

# Then fetch stats (assuming ID is 201142)
python scraper.py player-stats --player-id 201142 --season 2023-24
```

### Get historical data from multiple seasons
```bash
python scraper.py games --season 2021-22
python scraper.py games --season 2022-23
python scraper.py games --season 2023-24
```
