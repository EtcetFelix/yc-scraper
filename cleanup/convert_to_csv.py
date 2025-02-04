import json
import csv
import pandas as pd

MAX_FOUNDERS = 7

def jsonl_to_csv(input_jsonl, output_csv, max_founders=4):
    """
    Converts company data from JSONL to CSV format, flattening nested structures.
    
    Args:
        input_jsonl (str): Path to input JSONL file
        output_csv (str): Path where CSV data will be saved
        max_founders (int): Maximum number of founders to include in the CSV (default: 4)
    """
    # Read JSONL file
    data = []
    with open(input_jsonl, 'r') as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON line: {e}")
                continue

    # Process founders data
    for company in data:
        founders = company.get('founders', [])
        # Add founder count
        company['num_founders'] = len(founders)
        
        # Add founder details (up to max_founders)
        for i in range(max_founders):
            prefix = f'founder_{i+1}'
            if i < len(founders):
                founder = founders[i]
                company[f'{prefix}_name'] = founder.get('full_name', '')
                company[f'{prefix}_bio'] = founder.get('founder_bio', '')
                company[f'{prefix}_linkedin'] = founder.get('linkedin_url', '')
                company[f'{prefix}_twitter'] = founder.get('twitter_url', '')
            else:
                company[f'{prefix}_name'] = ''
                company[f'{prefix}_bio'] = ''
                company[f'{prefix}_linkedin'] = ''
                company[f'{prefix}_twitter'] = ''
        
        # Remove the original founders list
        del company['founders']
        
        # Convert tags list to string
        if 'tags' in company:
            company['tags'] = ', '.join(company['tags']) if company['tags'] else ''

    # Define base columns
    columns = [
        'company_id',
        'company_name',
        'batch',
        'status',
        'short_description',
        'long_description',
        'location',
        'country',
        'year_founded',
        'team_size',
        'num_founders',
        'tags',
        'website',
        'linkedin_url',
        'cb_url'
    ]
    
    # Add founder columns based on max_founders
    for i in range(max_founders):
        columns.extend([
            f'founder_{i+1}_name',
            f'founder_{i+1}_bio',
            f'founder_{i+1}_linkedin',
            f'founder_{i+1}_twitter'
        ])

    # Convert to DataFrame and reorder columns
    df = pd.DataFrame(data)
    df = df[columns]

    # Save to CSV
    df.to_csv(output_csv, index=False, encoding='utf-8')
    
    print(f"Converted {len(data)} companies to CSV")
    print(f"Output saved to {output_csv}")
    print(f"\nColumns in CSV:")
    for col in columns:
        print(f"- {col}")

# Usage
if __name__ == '__main__':
    # You can now specify the maximum number of founders when calling the function
    jsonl_to_csv('companies_deduplicated.jl', 'yc_companies.csv', max_founders=MAX_FOUNDERS)