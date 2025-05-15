import pandas as pd
import json
import os
import argparse
from pathlib import Path
from datetime import datetime

def extract_data(num_rows=10, output_folder="output"):
    """
    Extract data from Excel file and convert each row to a JSON file
    
    Args:
        num_rows (int): Number of rows to extract. If -1, extract all rows.
        output_folder (str): Path to the output folder
    """
    # Define the correct column headers
    predefined_columns = [
        "No", "Id", "SalaryExpectation", "CurrencyType", "Age", 
        "State / Province", "Education Level", "Major", "Degree", "Institute",
        "Education From (Month/Year)", "Education To (Month/Year)", "FreshGraduate",
        "Work From (Month/Year)", "Work To (Month/Year) / Present", "CompanyName", 
        "Position", "Industry", "MonthlySalary", "Bonus", "CurrencyType2", 
        "labelTh", "TestType", "Score", "Edu", "Column1", "Column2", 
        "YOS-Y", "YOS-M", "YOS-Y หลังเรียนจบ", "YOS-M หลังเรียนจบ2", 
        "Job Family", "Sub-Job Family", "YOS-Y2", "YOS-Y หลังเรียนจบ2", 
        "YOS-Y หลังเรียนจบ3", "Final จับกลุ่ม", "Final Sub Job Family", 
        "Experience", "Age2", "Province", "Region", "30Focus"
    ]

    # Create output directory if it doesn't exist
    output_dir = Path(output_folder)
    output_dir.mkdir(exist_ok=True)

    # Read the Excel file - don't skip any rows since we'll manually assign column names
    excel_file = Path("data/Data.xlsx")
    df = pd.read_excel(excel_file)
    
    # Assign the predefined column names, handling case where Excel has fewer columns
    if len(df.columns) <= len(predefined_columns):
        # Use only as many predefined column names as there are columns in the dataframe
        df.columns = predefined_columns[:len(df.columns)]
    else:
        # If Excel has more columns than our predefined list, use predefined ones and keep extras as is
        new_columns = predefined_columns.copy()
        for i in range(len(predefined_columns), len(df.columns)):
            new_columns.append(f"Extra_Column_{i+1}")
        df.columns = new_columns
    
    # Determine how many rows to process
    total_rows = len(df)
    if num_rows == -1:
        row_limit = total_rows
    else:
        row_limit = min(num_rows, total_rows)

    print(f"Extracting {row_limit} rows from {excel_file}")

    # Process each row and convert to JSON
    for index in range(row_limit):
        # Extract row data
        row_data = df.iloc[index].to_dict()
        
        # Convert any pandas data types to Python native types
        # This handles NaN, timestamps, and other pandas-specific types
        clean_data = {}
        for key, value in row_data.items():
            # Ensure key is a string
            str_key = str(key) if key is not None else "None"
            
            # Handle duplicate keys by appending a suffix
            if str_key in clean_data:
                str_key = f"{str_key}_2"
                
            if pd.isna(value):
                clean_data[str_key] = None
            elif isinstance(value, (datetime, pd.Timestamp)):
                clean_data[str_key] = value.isoformat()
            else:
                clean_data[str_key] = value
        
        # Use "No" column as primary unique key if it exists, 
        # fall back to "Id" if "No" doesn't exist, 
        # and finally use index+1 if neither exists
        no_value = clean_data.get('No')
        if no_value is not None:
            identifier = no_value
        else:
            identifier = clean_data.get('Id', index + 1)
            
        json_filename = f"row_{identifier}.json"
        output_path = output_dir / json_filename
        
        # Save as JSON file
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(clean_data, json_file, indent=2, ensure_ascii=False)
        
        # Print progress every 100 rows when processing large datasets
        if (index + 1) % 100 == 0 or index == 0 or index == row_limit - 1:
            print(f"Processed {index + 1} of {row_limit} rows")

    print(f"Successfully created {row_limit} JSON files in the '{output_folder}' directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract data from Excel and convert to JSON files")
    parser.add_argument("--rows", type=int, default=20, help="Number of rows to extract. Use -1 for all rows.")
    parser.add_argument("--output", type=str, default="output", help="Output directory path")
    args = parser.parse_args()
    
    extract_data(args.rows, args.output) 