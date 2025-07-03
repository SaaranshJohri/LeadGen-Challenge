

import re
import smtplib
import dns.resolver
import csv
from itertools import product

def generate_email_patterns(name, domain):
    first, last = name.lower().split()
    patterns = [
        f"{first}@{domain}",
        f"{last}@{domain}",
        f"{first}.{last}@{domain}",
        f"{first[0]}{last}@{domain}",
        f"{first}{last}@{domain}"
    ]
    return patterns

def verify_email(email):
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange)

        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail('test@example.com')
        code, message = server.rcpt(email)
        server.quit()

        return code == 250
    except Exception:
        return False

def discover_and_verify(name, domain):
    candidates = generate_email_patterns(name, domain)
    results = {}
    for email in candidates:
        results[email] = verify_email(email)
    return results

def process_csv(input_file, output_file):
    with open(input_file, newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['Name', 'Domain', 'Generated Email', 'Valid']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            name = row['Name']
            domain = row['Domain']
            result = discover_and_verify(name, domain)
            for email, valid in result.items():
                writer.writerow({
                    'Name': name,
                    'Domain': domain,
                    'Generated Email': email,
                    'Valid': 'Yes' if valid else 'No'
                })

if __name__ == "__main__":
    mode = input("Choose mode - single (s) or batch from CSV (b): ").strip().lower()

    if mode == 's':
        name = input("Enter full name (e.g., John Doe): ")
        domain = input("Enter domain (e.g., example.com): ")
        result = discover_and_verify(name, domain)
        print("\nVerification Results:")
        for email, is_valid in result.items():
            print(f"{email}: {'Valid' if is_valid else 'Invalid'}")
    elif mode == 'b':
        input_file = input("Enter input CSV filename: ")
        output_file = input("Enter output CSV filename: ")
        process_csv(input_file, output_file)
        print(f"Batch processing complete. Results saved to {output_file}")
    else:
        print("Invalid mode selected. Please choose 's' or 'b'.")
