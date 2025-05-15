# Job Family Mapping Tool

This project provides tools for processing job data, mapping job positions to job families, and consolidating data into CSV format.

## Overview

The project consists of two main tools:

1. **Job Family Mapping Tool**: Maps job positions to job families using OpenAI's GPT-4.1-mini model
2. **JSON to CSV Consolidation Tool**: Consolidates multiple JSON files into a single CSV file with proper encoding

## Features

- Automatic job family mapping using AI
- Batch processing of JSON files
- Data consolidation into a single CSV file
- Proper UTF-8 encoding for Thai characters
- Preservation of original data structure and column order

## Setup

1. Ensure you have Python 3.8+ installed:
   ```
   python --version
   ```

2. Clone the repository:
   ```
   git clone https://github.com/tkhongsap/mapping-job-family.git
   cd mapping-job-family
   ```

3. Install required packages:
   ```
   pip install openai python-dotenv
   ```

4. Configure OpenAI API key:
   - Create a `.env` file in the root directory with your API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
   - Alternatively, you can pass it as a command-line argument when running the mapping script

## Directory Structure

```
mapping-job-family/
├── data/             # Input data directory
├── output/           # Output directory for JSON files
├── scr/              # Source code
│   ├── map_job_families.py      # Job family mapping script
│   └── consolidate_json_to_csv.py # JSON to CSV conversion script
├── .env              # Environment variables (API keys)
├── .env.example      # Example environment file
├── job-category.json # Job category definitions
└── README.md         # This file
```

## How to Run

### Job Family Mapping

1. Place your job-category.json file in the root directory (already done)
2. Ensure your output JSON files are in the `output/` directory with names matching `row_*.json`
3. Run the script:
   ```
   python scr/map_job_families.py
   ```
   
   Or with API key as argument:
   ```
   python scr/map_job_families.py --api-key=your_api_key_here
   ```

### JSON to CSV Consolidation

After the mapping process is complete, you can consolidate all JSON files into a single CSV file:

1. Run the consolidation script:
   ```
   python scr/consolidate_json_to_csv.py
   ```

2. The script will:
   - Read all JSON files from the `output/` directory
   - Combine them into a single CSV file
   - Save the result to `output/consolidated.csv`

3. Command-line options:
   ```
   python scr/consolidate_json_to_csv.py -h
   ```
   Available options:
   - `-i`, `--input`: Specify input directory (default: "output")
   - `-o`, `--output`: Specify output CSV path (default: "output/consolidated.csv")
   - `-m`, `--max`: Limit maximum number of files to process

4. Examples:
   ```
   # Process only the first 10 files
   python scr/consolidate_json_to_csv.py -m 10
   
   # Specify custom input and output locations
   python scr/consolidate_json_to_csv.py -i custom_input_dir -o results.csv
   ```

## Output

### Job Family Mapping Output

The mapping script will:
1. Process each JSON file in the output directory
2. Use OpenAI's API to map the "position" and "Industry" fields to a job family and sub-family
3. Add "job_family" and "job_sub_family" fields to each JSON file
4. Save the updated files back to the same location

### CSV Consolidation Output

The consolidation script will:
1. Combine all mapped JSON files into a single CSV file
2. Preserve the original column order from the JSON files
3. Ensure proper UTF-8 encoding for Thai characters
4. Add any new fields found in later files to the end of the column list

## Technical Implementation

- The mapping script uses OpenAI's new Responses API (instead of the older Chat Completions API)
- The consolidation script uses OrderedDict to maintain the original JSON structure
- Both scripts properly handle UTF-8 encoding to support Thai characters
- Natural sorting is used to ensure files are processed in numerical order (e.g., row_10.json comes after row_9.json)

## Notes

- The mapping script includes a 1-second delay between API calls to respect rate limits
- Invalid mappings will be logged but processing will continue
- Progress is displayed in the console for both scripts
- The consolidation script uses UTF-8 with BOM (Byte Order Mark) to ensure proper display of Thai characters in applications like Microsoft Excel 