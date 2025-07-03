

import csv
import re

def score_title(title):
    score = 0
    title = title.lower()
    if any(keyword in title for keyword in ['ceo', 'founder', 'co-founder']):
        score += 40
    if any(keyword in title for keyword in ['head', 'director', 'vp']):
        score += 30
    if 'manager' in title:
        score += 20
    if 'intern' in title or 'assistant' in title:
        score -= 10
    return score

def score_domain(domain):
    # Example scoring for SaaS/AI focused domains
    score = 0
    if any(keyword in domain for keyword in ['ai', 'tech', 'saas', 'cloud']):
        score += 20
    return score

def score_lead(row):
    score = 0
    score += score_title(row['Title'])
    score += score_domain(row['Domain'])
    if row.get('Email Verified', '').lower() == 'yes':
        score += 30
    return score

def process_leads(input_file, output_file):
    with open(input_file, newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Lead Score']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row['Lead Score'] = score_lead(row)
            writer.writerow(row)

if __name__ == "__main__":
    input_file = input("Enter input CSV filename (with Title, Domain, Email Verified): ")
    output_file = input("Enter output CSV filename: ")
    process_leads(input_file, output_file)
    print(f"Lead scoring complete. Results saved to {output_file}")
