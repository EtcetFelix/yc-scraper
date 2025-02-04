import json

def filter_scraped_urls(input_urls_file, output_urls_file, jsonl_file):
    """
    Reads URLs from a text file, removes already scraped ones, and writes remaining URLs to a new file.
    
    Args:
        input_urls_file (str): Path to text file containing original URL list
        output_urls_file (str): Path where filtered URLs will be saved
        jsonl_file (str): Path to JSONL file containing scraped data
    """
    # Read original URLs list
    try:
        with open(input_urls_file, 'r') as f:
            urls = json.loads(f.read())
    except FileNotFoundError:
        print(f"Input file {input_urls_file} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error parsing URLs from {input_urls_file}")
        return

    # Read scraped companies from JSONL file
    scraped_companies = set()
    try:
        with open(jsonl_file, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    company_name = data.get('company_name', '').lower()
                    scraped_companies.add(company_name)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"JSONL file {jsonl_file} not found. Will process all URLs.")

    # Filter out already scraped URLs
    def get_company_name(url):
        return url.split('/')[-1]

    unscraped_urls = [
        url for url in urls 
        if get_company_name(url).lower() not in scraped_companies
    ]

    # Write remaining URLs to new file
    with open(output_urls_file, 'w') as f:
        json.dump(unscraped_urls, f)

    print(f"Total URLs: {len(urls)}")
    print(f"Already scraped: {len(scraped_companies)}")
    print(f"Remaining to scrape: {len(unscraped_urls)}")
    print(f"Filtered URLs written to {output_urls_file}")

# Usage
filter_scraped_urls(
    input_urls_file='./output/start_urls-pre-first-scrape.txt',
    output_urls_file='./output/start_urls-post-first-scrape.txt',
    jsonl_file='output/first1865companies.jl'
)