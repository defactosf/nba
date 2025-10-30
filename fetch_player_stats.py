#!/usr/bin/env python3
"""
Fetch NBA player statistics with minimum minutes filter.
Pulls all players who have played at least a specified number of minutes in the current season.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

try:
    from nba_api.stats.endpoints import leaguedashplayerstats
    import pandas as pd
except ImportError:
    print("Error: Required packages not installed. Run: pip install -r requirements.txt")
    sys.exit(1)


def fetch_player_stats(season="2024-25", min_minutes=15.0, output_format="json", output_dir="data"):
    """
    Fetch player statistics for players with minimum game time.

    Args:
        season: NBA season (e.g., "2024-25")
        min_minutes: Minimum minutes played (total across all games)
        output_format: "json" or "csv"
        output_dir: Directory to save output files
    """
    print(f"Fetching player stats for {season} season...")
    print(f"Filter: Players with at least {min_minutes} total minutes played")
    print("-" * 70)

    try:
        # Fetch player stats from the API
        player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            season_type_all_star="Regular Season",  # Regular Season, Playoffs, All Star
            per_mode_detailed="Totals",  # Totals gives us total minutes
            measure_type_detailed_defense="Base"
        )

        # Get the data as a DataFrame
        df = player_stats.get_data_frames()[0]

        print(f"✓ Retrieved {len(df)} total players from API")

        # Filter by minimum minutes (MIN column contains total minutes)
        if 'MIN' in df.columns:
            # Convert MIN to float if it's not already
            df['MIN'] = pd.to_numeric(df['MIN'], errors='coerce')
            df_filtered = df[df['MIN'] >= min_minutes].copy()
        else:
            print("Warning: MIN column not found, returning all players")
            df_filtered = df.copy()

        # Sort by minutes played (descending)
        df_filtered = df_filtered.sort_values('MIN', ascending=False)

        print(f"✓ Filtered to {len(df_filtered)} players with >={min_minutes} minutes")

        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Save the data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"player_stats_{season}_min{int(min_minutes)}mins_{timestamp}"

        if output_format == "json":
            filepath = output_path / f"{filename}.json"
            df_filtered.to_json(filepath, orient="records", indent=2)
        elif output_format == "csv":
            filepath = output_path / f"{filename}.csv"
            df_filtered.to_csv(filepath, index=False)
        else:
            raise ValueError(f"Unsupported format: {output_format}")

        print(f"✓ Saved to: {filepath}")
        print()

        # Display summary statistics
        print("Summary Statistics:")
        print("-" * 70)
        print(f"Total players: {len(df_filtered)}")
        if len(df_filtered) > 0:
            print(f"Total minutes range: {df_filtered['MIN'].min():.1f} - {df_filtered['MIN'].max():.1f}")
            print(f"Average minutes: {df_filtered['MIN'].mean():.1f}")
            print()
            print("Top 10 Players by Minutes Played:")
            print("-" * 70)
            top_players = df_filtered.head(10)[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'MIN', 'PTS', 'REB', 'AST']]
            print(top_players.to_string(index=False))

        return df_filtered

    except Exception as e:
        print(f"Error fetching player stats: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch NBA player statistics with minimum minutes filter"
    )

    parser.add_argument(
        "--season",
        default="2024-25",
        help="NBA season (e.g., 2024-25, 2023-24)"
    )

    parser.add_argument(
        "--min-minutes",
        type=float,
        default=15.0,
        help="Minimum total minutes played (default: 15.0)"
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
        help="Output directory for data (default: data)"
    )

    args = parser.parse_args()

    # Fetch and save player stats
    fetch_player_stats(
        season=args.season,
        min_minutes=args.min_minutes,
        output_format=args.format,
        output_dir=args.output_dir
    )


if __name__ == "__main__":
    main()
