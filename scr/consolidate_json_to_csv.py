import os
import json
import csv
import re
import argparse
from collections import OrderedDict

def natural_sort_key(s):
    """
    Sort strings that contain numbers in natural order.
    For example, row_10.json comes after row_2.json, not after row_1.json.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def consolidate_json_to_csv(input_dir, output_file, max_files=None):
    """
    Consolidate JSON files from input_dir into a single CSV file.
    
    Args:
        input_dir (str): Directory containing JSON files.
        output_file (str): Output CSV file path.
        max_files (int, optional): Maximum number of files to process. Defaults to None (all files).
    """
    # Get all JSON files
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json') and f.startswith('row_')]
    
    # Sort files naturally
    json_files.sort(key=natural_sort_key)
    
    # Limit the number of files if specified
    if max_files is not None:
        json_files = json_files[:max_files]
    
    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return
    
    # First pass: Collect all unique keys while preserving order from first file
    ordered_headers = OrderedDict()
    all_data = []
    
    # Process first file to establish initial column order
    with open(os.path.join(input_dir, json_files[0]), 'r', encoding='utf-8') as f:
        first_data = json.load(f, object_pairs_hook=OrderedDict)
        for key in first_data.keys():
            ordered_headers[key] = None
    
    # Process all files
    for file_name in json_files:
        try:
            with open(os.path.join(input_dir, file_name), 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.append(data)
                
                # Add any new keys that weren't in the first file
                for key in data.keys():
                    if key not in ordered_headers:
                        ordered_headers[key] = None
                        
            print(f"Processed {file_name}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_name}, skipping...")
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")
    
    # Get final list of headers in the preserved order
    headers = list(ordered_headers.keys())
    
    # Write to CSV with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"Successfully consolidated {len(all_data)} JSON files into {output_file}")
    print(f"Used UTF-8 encoding with signature (BOM) to ensure Thai characters display correctly")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Consolidate JSON files into a single CSV file')
    parser.add_argument('-i', '--input', default='output', help='Input directory containing JSON files (default: output)')
    parser.add_argument('-o', '--output', default='output/consolidated.csv', help='Output CSV file path (default: output/consolidated.csv)')
    parser.add_argument('-m', '--max', type=int, help='Maximum number of files to process')
    
    args = parser.parse_args()
    
    consolidate_json_to_csv(args.input, args.output, args.max) 