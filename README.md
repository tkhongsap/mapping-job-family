# Job Family Mapping Tool

This repository provides a set of scripts for processing job data. It can extract candidate records from an Excel file, map each position to a job family using Azure OpenAI, and finally consolidate all JSON results into a single CSV.

## Overview

The project is composed of three main tools:

1. **Excel Data Extraction Tool** (`extract_data.py`)
   - Converts rows from the spreadsheet in `data/` into individual JSON files.
2. **Job Family Mapping Tool** (`map_job_families.py`)
   - Calls the Azure OpenAI Responses API to assign the most relevant job family and sub-family defined in `job-category.json`.
3. **JSON to CSV Consolidation Tool** (`consolidate_json_to_csv.py`)
   - Merges all mapped JSON files into a single CSV while preserving column order and Thai characters.

## Features

- Convert Excel records to JSON files
- Automatic job family mapping using AI
- Batch processing of JSON data
- Data consolidation into a single CSV file
- Proper UTF-8 encoding for Thai characters
- Preservation of the original column order

## Setup

1. Ensure you have Python 3.8+ installed:
   ```bash
   python --version
   ```
2. Clone the repository:
   ```bash
   git clone https://github.com/tkhongsap/mapping-job-family.git
   cd mapping-job-family
   ```
3. Install required packages:
   ```bash
   pip install openai python-dotenv pandas
   ```
4. Create a `.env` file with your Azure OpenAI credentials:
   ```bash
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_API_VERSION=2025-03-01-preview
   AZURE_OPENAI_MODEL_NAME=gpt-4.1
   AZURE_OPENAI_DEPLOYMENT=gpt-4.1
   ```

## Directory Structure

```
mapping-job-family/
├── data/                     # Input files (Excel and PDF)
├── output/                   # Generated JSON and CSV files (ignored by Git)
├── scr/                      # Source code
│   ├── extract_data.py           # Excel to JSON extraction script
│   ├── map_job_families.py       # Job family mapping script
│   ├── consolidate_json_to_csv.py # JSON to CSV conversion script
│   ├── test_mapping.py           # Helper script for local testing
│   └── test-connection.py        # Simple environment check
├── job-category.json         # Job category definitions
├── .env.example              # Example environment file
└── README.md
```

## How to Run

### 1. Extract Data from Excel

The sample spreadsheet is expected at `data/Data.xlsx`.
Run the following command to create JSON files under `output/`:
```bash
python scr/extract_data.py --rows 20 --output output
```
Use `--rows -1` to process every row.

### 2. Map Job Families

After you have JSON files, execute the mapping script:
```bash
python scr/map_job_families.py
```
The script reads each `row_*.json` file, contacts Azure OpenAI, and writes back the mapped job family information.

### 3. Consolidate JSON to CSV

Finally, combine all JSON files into a single CSV:
```bash
python scr/consolidate_json_to_csv.py
```
Use `-h` to see available options for input directory, output path, and file limit.

## Output

### Mapping Output

- Each processed JSON file gains `job_family` and `job_sub_family` fields.

### CSV Output

- All mapped files are combined into `output/consolidated.csv`.
- The original column order is preserved and UTF‑8 with BOM is used so Thai characters appear correctly in spreadsheet applications.

## Technical Notes

- The mapping script uses the new Azure OpenAI Responses API and includes a short delay between requests to respect rate limits.
- Natural sorting ensures files are processed in numeric order (e.g., `row_10.json` after `row_9.json`).

