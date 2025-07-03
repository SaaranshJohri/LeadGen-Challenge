

import requests
from bs4 import BeautifulSoup
import csv
import re
import time

def search_domain(company_name):
    query = f"{company_name} official site"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            # Extract URL from DuckDuckGo's redirection format
            uddg_match = re.search(r'uddg=(https%3A%2F%2F[^&]+)', href)
            if uddg_match:
                decoded_url = requests.utils.unquote(uddg_match.group(1))
                domain_match = re.search(r'https?://(?:www\.)?([\w.-]+)', decoded_url)
                if domain_match:
                    domain = domain_match.group(1)
                    if not any(s in domain for s in ["duckduckgo.com", "linkedin.com", "crunchbase.com", "github.io"]):
                        return domain
        return "Not found"
    except Exception as e:
        print(f"Error fetching domain for {company_name}: {e}")
        return "Error"

def process_companies(input_file, output_file):
    with open(input_file, newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Domain']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            company = row['Company']
            row['Domain'] = search_domain(company)
            writer.writerow(row)
            time.sleep(2)  # delay to prevent rate-limiting

if __name__ == "__main__":
    mode = input("Choose mode - single (s) or batch from CSV (b): ").strip().lower()

    if mode == 's':
        company = input("Enter company name: ")
        domain = search_domain(company)
        print(f"\nDiscovered domain: {domain}")
    elif mode == 'b':
        input_file = input("Enter input CSV filename (with Company column): ")
        output_file = input("Enter output CSV filename: ")
        process_companies(input_file, output_file)
        print(f"Domain finding complete. Results saved to {output_file}")
    else:
        print("Invalid mode selected. Please choose 's' or 'b'.")