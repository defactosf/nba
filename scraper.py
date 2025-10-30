#!/usr/bin/env python3
"""
NBA Data Scraper using nba_api
Scrapes historical NBA data including games, players, and team statistics.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from nba_api.stats.endpoints import (
        leaguegamefinder,
        commonallplayers,
        playergamelog,
        teamgamelog,
        boxscoretraditionalv2,
        leaguestandings,
    )
    from nba_api.stats.static import teams, players
except ImportError:
    print("Error: nba_api not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

import pandas as pd


class NbaScraper:
    """NBA data scraper using the nba_api library."""

    def __init__(self, output_dir="data"):
        """Initialize scraper with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def scrape_games(self, season="2023-24", team_abbr=None, output_format="json"):
        """
        Scrape game data for a specific season.

        Args:
            season: NBA season (e.g., "2023-24")
            team_abbr: Team abbreviation (e.g., "LAL" for Lakers), None for all teams
            output_format: "json" or "csv"
        """
        print(f"Fetching games for {season} season...")

        try:
            game_finder = leaguegamefinder.LeagueGameFinder(
                season_nullable=season,
                league_id_nullable="00"  # NBA
            )
            games_df = game_finder.get_data_frames()[0]

            if team_abbr:
                games_df = games_df[games_df['TEAM_ABBREVIATION'] == team_abbr]
                filename = f"games_{season}_{team_abbr}"
            else:
                filename = f"games_{season}"

            self._save_data(games_df, filename, output_format)
            print(f"✓ Scraped {len(games_df)} games")
            return games_df

        except Exception as e:
            print(f"Error scraping games: {e}")
            return None

    def scrape_players(self, season="2023-24", output_format="json"):
        """
        Scrape all players for a specific season.

        Args:
            season: NBA season (e.g., "2023-24")
            output_format: "json" or "csv"
        """
        print(f"Fetching players for {season} season...")

        try:
            all_players = commonallplayers.CommonAllPlayers(
                is_only_current_season=0,
                league_id="00",
                season=season
            )
            players_df = all_players.get_data_frames()[0]

            filename = f"players_{season}"
            self._save_data(players_df, filename, output_format)
            print(f"✓ Scraped {len(players_df)} players")
            return players_df

        except Exception as e:
            print(f"Error scraping players: {e}")
            return None

    def scrape_player_stats(self, player_id, season="2023-24", output_format="json"):
        """
        Scrape game log for a specific player.

        Args:
            player_id: NBA player ID
            season: NBA season (e.g., "2023-24")
            output_format: "json" or "csv"
        """
        print(f"Fetching stats for player {player_id} in {season}...")

        try:
            player_log = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=season
            )
            stats_df = player_log.get_data_frames()[0]

            filename = f"player_{player_id}_{season}"
            self._save_data(stats_df, filename, output_format)
            print(f"✓ Scraped {len(stats_df)} games for player {player_id}")
            return stats_df

        except Exception as e:
            print(f"Error scraping player stats: {e}")
            return None

    def scrape_team_stats(self, team_id, season="2023-24", output_format="json"):
        """
        Scrape game log for a specific team.

        Args:
            team_id: NBA team ID
            season: NBA season (e.g., "2023-24")
            output_format: "json" or "csv"
        """
        print(f"Fetching stats for team {team_id} in {season}...")

        try:
            team_log = teamgamelog.TeamGameLog(
                team_id=team_id,
                season=season
            )
            stats_df = team_log.get_data_frames()[0]

            filename = f"team_{team_id}_{season}"
            self._save_data(stats_df, filename, output_format)
            print(f"✓ Scraped {len(stats_df)} games for team {team_id}")
            return stats_df

        except Exception as e:
            print(f"Error scraping team stats: {e}")
            return None

    def scrape_standings(self, season="2023-24", output_format="json"):
        """
        Scrape league standings for a specific season.

        Args:
            season: NBA season (e.g., "2023-24")
            output_format: "json" or "csv"
        """
        print(f"Fetching standings for {season} season...")

        try:
            standings = leaguestandings.LeagueStandings(
                league_id="00",
                season=season
            )
            standings_df = standings.get_data_frames()[0]

            filename = f"standings_{season}"
            self._save_data(standings_df, filename, output_format)
            print(f"✓ Scraped standings for {len(standings_df)} teams")
            return standings_df

        except Exception as e:
            print(f"Error scraping standings: {e}")
            return None

    def list_teams(self):
        """List all NBA teams with their IDs and abbreviations."""
        all_teams = teams.get_teams()
        print("\nAvailable NBA Teams:")
        print("-" * 60)
        for team in all_teams:
            print(f"{team['abbreviation']:4} | {team['full_name']:30} | ID: {team['id']}")
        return all_teams

    def search_player(self, player_name):
        """Search for a player by name."""
        all_players = players.find_players_by_full_name(player_name)

        if not all_players:
            print(f"No players found matching '{player_name}'")
            return None

        print(f"\nFound {len(all_players)} player(s):")
        print("-" * 60)
        for player in all_players:
            print(f"{player['full_name']:30} | ID: {player['id']}")

        return all_players

    def _save_data(self, df, filename, output_format):
        """Save DataFrame to file in specified format."""
        if output_format == "json":
            filepath = self.output_dir / f"{filename}.json"
            df.to_json(filepath, orient="records", indent=2)
        elif output_format == "csv":
            filepath = self.output_dir / f"{filename}.csv"
            df.to_csv(filepath, index=False)
        else:
            raise ValueError(f"Unsupported format: {output_format}")

        print(f"✓ Saved to: {filepath}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="NBA Data Scraper - Fetch historical NBA data using nba_api"
    )

    parser.add_argument(
        "command",
        choices=["games", "players", "player-stats", "team-stats", "standings", "list-teams", "search-player"],
        help="Command to execute"
    )

    parser.add_argument(
        "--season",
        default="2023-24",
        help="NBA season (e.g., 2023-24, 2022-23)"
    )

    parser.add_argument(
        "--team-abbr",
        help="Team abbreviation (e.g., LAL, BOS, GSW)"
    )

    parser.add_argument(
        "--team-id",
        type=int,
        help="Team ID for team-stats command"
    )

    parser.add_argument(
        "--player-id",
        type=int,
        help="Player ID for player-stats command"
    )

    parser.add_argument(
        "--player-name",
        help="Player name for search-player command"
    )

    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json)"
    )

    parser.add_argument(
        "--output-dir",
        default="data",
        help="Output directory for scraped data (default: data)"
    )

    args = parser.parse_args()

    scraper = NbaScraper(output_dir=args.output_dir)

    # Execute command
    if args.command == "games":
        scraper.scrape_games(
            season=args.season,
            team_abbr=args.team_abbr,
            output_format=args.format
        )

    elif args.command == "players":
        scraper.scrape_players(
            season=args.season,
            output_format=args.format
        )

    elif args.command == "player-stats":
        if not args.player_id:
            print("Error: --player-id required for player-stats command")
            print("Use 'search-player' command to find player IDs")
            sys.exit(1)
        scraper.scrape_player_stats(
            player_id=args.player_id,
            season=args.season,
            output_format=args.format
        )

    elif args.command == "team-stats":
        if not args.team_id:
            print("Error: --team-id required for team-stats command")
            print("Use 'list-teams' command to see team IDs")
            sys.exit(1)
        scraper.scrape_team_stats(
            team_id=args.team_id,
            season=args.season,
            output_format=args.format
        )

    elif args.command == "standings":
        scraper.scrape_standings(
            season=args.season,
            output_format=args.format
        )

    elif args.command == "list-teams":
        scraper.list_teams()

    elif args.command == "search-player":
        if not args.player_name:
            print("Error: --player-name required for search-player command")
            sys.exit(1)
        scraper.search_player(args.player_name)


if __name__ == "__main__":
    main()
