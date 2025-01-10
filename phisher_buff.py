import smtplib
import socks
import dns.resolver
import threading
from collections import defaultdict
import os

def prompt_user():
    print("\nPhisher Buff! [by 99tea]\n")
    
    # Path to names file (default to names.txt)
    file_path = input("\nEnter path to names file: ")
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found. Please check the path.")
        exit(1)

    # Target email domain
    domain = input("\nEnter target email domain (e.g., company.com): ").strip()
    if not domain:
        print("Error: You must provide a domain.")
        exit(1)

    # Known full name (optional)
    known_name = input("\nEnter a known full name (or press Enter to skip): ").strip()

    # Corresponding known email (optional)
    known_email = input("\nEnter the corresponding known email (or press Enter to skip): ").strip()

    # Proxy list file (optional)
    proxy_list_path = input("\nEnter path to proxylist file (or press Enter to skip): ").strip()

    return file_path, domain, known_name, known_email, proxy_list_path

def read_names(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file]

def detect_pattern(full_name, email, domain):
    """Extracts and learns email pattern from a given known email."""
    if not email:
        return None
    
    name_parts = full_name.lower().split()
    email_prefix = email.split("@")[0]
    
    patterns = []
    
    if email_prefix == f"{name_parts[0][0]}{name_parts[-1]}":
        patterns.append("{first_initial}{last}")
    if email_prefix == f"{name_parts[0]}.{name_parts[-1]}":
        patterns.append("{first}.{last}")
    if email_prefix == f"{name_parts[0]}{name_parts[-1]}":
        patterns.append("{first}{last}")
    
    return patterns[0] if patterns else None

def generate_emails(full_name, domain, learned_pattern):
    name_parts = full_name.lower().split()
    first, last = name_parts[0], name_parts[-1]
    first_initial = first[0]
    
    email_variations = []
    
    if learned_pattern:
        email_variations.append(learned_pattern.format(first=first, last=last, first_initial=first_initial) + "@" + domain)
    
    email_variations.extend([
        f"{first}.{last}@{domain}",
        f"{first}{last}@{domain}",
        f"{first_initial}{last}@{domain}",
        f"{first}{last[0]}@{domain}",
        f"{first_initial}.{last}@{domain}",
        f"{first}_{last}@{domain}",
        f"{last}.{first}@{domain}"
    ])
    
    return email_variations

def get_mx_record(domain):
    """Finds the MX record for a given domain."""
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return str(records[0].exchange)
    except Exception as e:
        print(f"Error finding MX record for {domain}: {e}")
        return None

def validate_email(email, mx_server, results, proxy_host=None, proxy_port=None):
    """Checks if an email address is valid using SMTP RCPT TO through a SOCKS5 proxy if provided."""
    if not mx_server:
        results[email] = (False, "No MX record found")
        return
    
    try:
        if proxy_host and proxy_port:
            socks.setdefaultproxy(socks.SOCKS5, proxy_host, proxy_port)
            socks.wrapmodule(smtplib)
        
        server = smtplib.SMTP(mx_server, 25, timeout=10)
        server.helo()
        server.mail("me@example.com")  # Fake sender email
        code, message = server.rcpt(email)
        server.quit()
        results[email] = (code == 250, message.decode())
    except Exception as e:
        results[email] = (False, str(e))

def main():
    file_path, domain, known_name, known_email, proxy_list_path = prompt_user()
    names = read_names(file_path)
    
    learned_pattern = detect_pattern(known_name, known_email, domain) if known_name and known_email else None
    
    mx_server = get_mx_record(domain)
    valid_emails = []
    
    results = defaultdict(tuple)
    threads = []
    
    # Set to track already validated names
    processed_names = set()

    for name in names:
        if name in processed_names:  # Skip if we've already found a valid email for this name
            print(f"[✔] Skipping {name}, already found valid email.")
            continue

        email_variations = generate_emails(name, domain, learned_pattern)
        for email in email_variations:
            thread = threading.Thread(target=validate_email, args=(email, mx_server, results, proxy_list_path))
            thread.start()
            threads.append(thread)
        
        # After all emails are tested for this name, check if we found a valid one
        for email in email_variations:
            if email in results and results[email][0]:
                processed_names.add(name)  # Mark this name as processed
                print(f"[✔] Valid Email found for {name}: {email}")
                break  # No need to check further variations for this name

    for thread in threads:
        thread.join()
    
    for email, (valid, response) in results.items():
        if valid:
            valid_emails.append(email)
            print(f"[✔] Valid Email: {email} ✅")
        else:
            print(f"[✖] Invalid: {email} ({response})")
    
    with open("valid_emails.txt", "w") as f:
        f.writelines("\n".join(valid_emails))
    
    print("[✔] Finished. Valid emails saved in valid_emails.txt")

if __name__ == "__main__":
    main()
