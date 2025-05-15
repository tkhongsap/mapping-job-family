# Job Family Mapping Tool

This tool automatically maps job positions to job families and sub-families using OpenAI's GPT-4.1-mini model.

## Overview

The tool:
1. Processes JSON files containing job data from the `output/` directory
2. For each file, it extracts the position and industry information
3. Uses OpenAI's GPT-4.1-mini model to determine the appropriate job family and sub-family based on the categories in `job-category.json`
4. Updates each JSON file with the mapping results

## Setup

1. Make sure you have Python 3.8+ installed
2. Install required packages:
   ```
   pip install openai python-dotenv
   ```

## How to Run

1. Place your job-category.json file in the root directory (already done)
2. Ensure your output JSON files are in the `output/` directory with names matching `row_*.json`
3. Run the script with your OpenAI API key:
   ```
   python scr/map_job_families.py --api-key=your_api_key_here
   ```
   
   Alternatively, you can create a `.env` file in the root directory with your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   And then run:
   ```
   python scr/map_job_families.py
   ```

## Output

The script will:
1. Process each JSON file in the output directory
2. Use OpenAI's API to map the "position" and "Industry" fields to a job family and sub-family
3. Add "job_family" and "job_sub_family" fields to each JSON file
4. Save the updated files back to the same location

## Technical Implementation

- This script uses OpenAI's new Responses API (instead of the older Chat Completions API)
- The Responses API provides a simpler interface for working with the latest OpenAI models
- We properly handle UTF-8 encoding to support international text characters

## Notes

- The script includes a 1-second delay between API calls to respect rate limits
- Invalid mappings will be logged but processing will continue
- Progress is displayed in the console
- The script handles UTF-8 encoding to properly process international text 