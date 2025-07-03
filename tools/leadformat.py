

import csv
import re

def normalize_name(name):
    name = name.strip().lower()
    name = re.sub(r'[^a-z ]+', '', name)
    return ' '.join(name.split())

def normalize_email(email):
    email = email.strip().lower()
    return email

def normalize_title(title):
    title = title.strip().title()
    return title

def process_leads(input_file, output_file):
    with open(input_file, newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if 'Name' in row:
                row['Name'] = normalize_name(row['Name'])
            if 'Email' in row:
                row['Email'] = normalize_email(row['Email'])
            if 'Title' in row:
                row['Title'] = normalize_title(row['Title'])
            writer.writerow(row)

if __name__ == "__main__":
    input_file = input("Enter input CSV filename: ")
    output_file = input("Enter output CSV filename: ")
    process_leads(input_file, output_file)
    print(f"Lead formatting complete. Output saved to {output_file}")
