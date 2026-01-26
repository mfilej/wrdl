# Wordle Solutions Fetcher

An idempotent Wordle solutions fetcher that automatically collects and maintains a comprehensive archive of New York Times Wordle solutions.

## Features

- **Automated daily fetching**: Runs at 2 AM UTC via GitHub Actions
- **Idempotent operation**: Safely skip already-fetched solutions
- **Gap detection**: Identifies and reports missing dates
- **Manual date fetching**: Fetch solutions for any specific date on demand
- **Sorted maintenance**: Automatically maintains chronological order

## Usage

### Automatic (GitHub Actions)

The workflow runs automatically every day at 2 AM UTC. No action needed.

### Manual Fetch

Run the workflow manually from the [Actions tab](https://github.com/mfilej/wrdl/actions/workflows/fetch-solutions.yml):

- **Without date**: Checks for missing solutions and fetches yesterday's
- **With date**: Fetches the solution for the specified date (YYYY-MM-DD format)

### Local Usage

```bash
# Default mode: check for gaps and fetch yesterday's solution
python3 fetch.py

# Fetch solution for a specific date
python3 fetch.py 2025-01-15
```

## Output

Solutions are stored in `solutions.txt` with one solution per line in the format:

```
YYYY-MM-DD WORD
```

Example:
```
2021-06-19 CIGAR
2021-06-20 REBUT
2021-06-21 SISSY
```

## How It Works

1. **Read existing solutions**: Loads all previously fetched solutions from `solutions.txt`
2. **Validate and repair**: Checks for sort order, automatically fixes if needed
3. **Detect gaps**: Identifies missing dates up to the day before yesterday
4. **Fetch from NYT**: Queries the New York Times Wordle API for missing solutions
5. **Maintain order**: Saves all solutions in chronological order

## Notes

- The script only fetches solutions up to the day before yesterday (solutions are publicly available the day after)
- All dates use UTC for consistency
- Solutions are fetched from the official New York Times Wordle API
