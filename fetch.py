#!/usr/bin/env python3
"""
Idempotent Wordle solutions fetcher.

Usage:
  python3 fetch_solutions.py
    - Reports missing dates (stops at day before yesterday)
    - Fetches and appends yesterday's solution if not present

  python3 fetch_solutions.py YYYY-MM-DD
    - Fetches solution for the given date
    - Stores it in the correct sorted position
    - Skips fetch if already present
"""

import requests
from datetime import datetime, timedelta
import os
import sys

OUTPUT_FILE = "/Users/miha/Developer/scries/2026-01-24-wordle/amp/solutions.txt"
START_DATE = datetime(2021, 6, 19)  # First Wordle date

def read_existing_solutions():
    """Read existing solutions and return as dict of date -> word."""
    solutions = {}
    is_sorted = True
    last_date = None
    
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        date, word = parts
                        solutions[date] = word
                        
                        # Check if file is sorted
                        if last_date is not None and date < last_date:
                            is_sorted = False
                        last_date = date
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
    
    # If not sorted, warn and fix
    if not is_sorted:
        print(f"⚠ Warning: {OUTPUT_FILE} is not sorted. Fixing...", file=sys.stderr)
        # Rewrite in sorted order
        with open(OUTPUT_FILE, 'w') as f:
            for date in sorted(solutions.keys()):
                f.write(f"{date} {solutions[date]}\n")
        print(f"✓ File has been sorted.", file=sys.stderr)
    
    return solutions

def find_missing_dates(existing_solutions):
    """Find missing dates up to day before yesterday."""
    yesterday = datetime.now() - timedelta(days=1)
    day_before_yesterday = yesterday - timedelta(days=1)
    
    missing = []
    current_date = START_DATE
    
    while current_date <= day_before_yesterday:
        date_str = current_date.strftime("%Y-%m-%d")
        if date_str not in existing_solutions:
            missing.append(date_str)
        current_date += timedelta(days=1)
    
    return missing, yesterday.strftime("%Y-%m-%d"), day_before_yesterday.strftime("%Y-%m-%d")

def fetch_solution(date_str):
    """Fetch solution for a given date from NYT API."""
    url = f"https://www.nytimes.com/svc/wordle/v2/{date_str}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'solution' in data and data['solution']:
                return data['solution'].upper()
    except Exception:
        pass
    return None

def save_solution(date_str, word, existing_solutions):
    """Save solution for a specific date, maintaining sorted order."""
    existing_solutions[date_str] = word
    
    # Write all solutions in sorted order
    with open(OUTPUT_FILE, 'w') as f:
        for date in sorted(existing_solutions.keys()):
            f.write(f"{date} {existing_solutions[date]}\n")

def main_daily_check():
    """Default mode: check missing dates and yesterday's solution."""
    existing = read_existing_solutions()
    missing_dates, yesterday_str, day_before_yesterday_str = find_missing_dates(existing)
    
    print(f"Existing solutions: {len(existing)}")
    print(f"Checking up to: {day_before_yesterday_str} (day before yesterday)")
    print()
    
    # Report missing dates
    if missing_dates:
        print(f"⚠ Missing {len(missing_dates)} solutions:")
        for date in missing_dates[:20]:
            print(f"  {date}")
        if len(missing_dates) > 20:
            print(f"  ... and {len(missing_dates) - 20} more")
        print()
    else:
        print("✓ No missing solutions (up to day before yesterday)")
        print()
    
    # Check and fetch yesterday
    print(f"Checking yesterday ({yesterday_str})...")
    
    if yesterday_str in existing:
        print(f"  ✓ Already present: {existing[yesterday_str]}")
    else:
        print(f"  Fetching...", end=" ", flush=True)
        solution = fetch_solution(yesterday_str)
        if solution:
            save_solution(yesterday_str, solution, existing)
            print(f"✓ {solution}")
        else:
            print("✗ Failed to fetch")
            return 1
    
    print()
    print(f"Current total: {len(existing) + (0 if yesterday_str in existing else 1)} solutions")
    return 0

def main_single_date(date_str):
    """Mode: fetch/check solution for a specific date."""
    # Validate date format
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Use YYYY-MM-DD", file=sys.stderr)
        return 1
    
    existing = read_existing_solutions()
    
    if date_str in existing:
        print(f"✓ Already present: {date_str} {existing[date_str]}")
        return 0
    
    print(f"Fetching solution for {date_str}...", end=" ", flush=True)
    solution = fetch_solution(date_str)
    
    if solution:
        save_solution(date_str, solution, existing)
        print(f"✓ {solution}")
        return 0
    else:
        print("✗ Failed to fetch")
        return 1

def main():
    if len(sys.argv) == 1:
        # Default mode
        return main_daily_check()
    elif len(sys.argv) == 2:
        # Single date mode
        return main_single_date(sys.argv[1])
    else:
        print(f"Usage: {sys.argv[0]} [YYYY-MM-DD]", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
