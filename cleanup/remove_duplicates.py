import json
from collections import defaultdict

def remove_duplicates(input_jsonl, output_jsonl):
    """
    Removes duplicate company entries from a JSONL file, keeping the latest entry
    for each company_id.
    
    Args:
        input_jsonl (str): Path to input JSONL file
        output_jsonl (str): Path where deduplicated data will be saved
    """
    # Dictionary to store latest entry for each company_id
    companies = {}
    duplicates_count = 0

    # Read all entries, keeping only the latest for each company_id
    try:
        with open(input_jsonl, 'r') as f:
            line_number = 0
            for line in f:
                line_number += 1
                try:
                    data = json.loads(line.strip())
                    company_id = data.get('company_id')
                    
                    if company_id is None:
                        print(f"Warning: Missing company_id at line {line_number}")
                        continue
                        
                    if company_id in companies:
                        duplicates_count += 1
                    
                    # Always keep the latest entry
                    companies[company_id] = data
                    
                except json.JSONDecodeError:
                    print(f"Warning: Invalid JSON at line {line_number}")
                    continue

        # Write deduplicated data to new file
        with open(output_jsonl, 'w') as f:
            for company in companies.values():
                f.write(json.dumps(company) + '\n')

        print(f"Original entries: {line_number}")
        print(f"Duplicate entries removed: {duplicates_count}")
        print(f"Final unique companies: {len(companies)}")
        print(f"Deduplicated data written to {output_jsonl}")

    except FileNotFoundError:
        print(f"Error: Input file {input_jsonl} not found.")
        return

# Usage
if __name__ == '__main__':
    remove_duplicates('./output/all_companies.jl', './output/companies_deduplicated.jl')