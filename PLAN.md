# Wordle Archive Frontend - Behavioral Specification

## Overview
A lightweight search interface for exploring Wordle solution history. Users can search for 5-letter words and discover when they appeared as solutions in the Wordle game.

## Data Sources
- **solutions.txt**: Contains pairs of dates and corresponding Wordle solution words from GitHub repository
- **valid.txt**: Contains a list of valid 5-letter words acceptable in Wordle gameplay from GitHub repository

Both files are loaded once on application startup and remain in memory throughout the session.

## Core User Workflows

### 1. Search by Prefix
**Trigger**: User types a partial word (1-5 letters) in the search input  
**Behavior**:
- Display all solutions from the archive that start with the entered prefix (case-insensitive)
- Match is prefix-based, not substring or fuzzy
- Each match shows the word in the results list
- Results update in real-time as the user types

**Edge cases**:
- Empty input: Show no results (clear results display)
- No matches found: Display "No matches" message

### 2. Full Word Lookup
**Trigger**: User enters exactly 5 letters that form a complete word  
**Behavior**:
- If the word exists in solutions: Display the word and its associated date inline
- If the word is not in solutions but is in valid.txt: Display the word (without date)
- If the word is neither in solutions nor valid.txt: Display "Not a playable word" error message in red

### 3. Input Constraints
- Maximum length: 5 characters
- Input is automatically converted to uppercase for display and comparison
- Input field has visual distinction when focused

## Display Specifications

### Search Input
- Accepts up to 5 characters
- Auto-focuses on page load
- Placeholder text: "Search"
- Uppercase transformation applied visually

### Results List
- Displays as a scrollable vertical list (max-height with overflow)
- Each result shows:
  - The matched word
  - Date (only for exact 5-letter word matches that are solutions)
- Results are listed in the order they appear in solutions.txt
- Separator lines between results for visual clarity
- Last result has no separator line

### Messages
- **No matches**: Gray text, appears when search returns no results
- **Not a playable word**: Red text, appears when a 5-letter input is invalid
- **Empty state**: Results area is empty when no input is provided

### Layout & Styling
- Clean, minimal design
- Centered single-column layout
- Maximum content width: 300px
- Page title: "Wordle Archive"
- Responsive typography with focus on readability
- Light color scheme with subtle borders

## Technical Requirements (Framework-Agnostic)
- Data loading occurs on application startup with error handling
- Search filtering happens on the client side (in-memory)
- No server-side processing required
- Stateful: Maintains loaded data for session duration
- Real-time filtering as user types (no debounce needed for this dataset size)

## Accessibility & UX
- Autofocus input on page load for immediate interaction
- Clear visual feedback for invalid inputs (red error text)
- Monospace font for the input to match Wordle aesthetics
- Keyboard-friendly: Tab navigation and Enter key support expected
- Responsive to different screen sizes (mobile-first approach)
