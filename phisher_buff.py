import smtplib, socks, dns.resolver, threading, os, itertools
from collections import defaultdict

# DISCLAIMER: This script is for ethical use only. The author holds no responsibility for misuse.
def read_file(path): return [line.strip() for line in open(path, 'r', encoding='utf-8') if line.strip()] if os.path.exists(path) else []

def get_mx(domain):
    try: return str(dns.resolver.resolve(domain, 'MX')[0].exchange)
    except: return None

def validate(email, mx, results, proxy):
    if not mx: results[email] = (False, "No MX"); return
    try:
        if proxy: socks.setdefaultproxy(socks.SOCKS5, proxy[0], int(proxy[1])); socks.wrapmodule(smtplib)
        s = smtplib.SMTP(mx, 25, timeout=10); s.helo(); s.mail("test@example.com")
        code, _ = s.rcpt(email); s.quit(); results[email] = (code == 250, "Valid" if code == 250 else "Invalid")
    except Exception as e: results[email] = (False, str(e))

def generate_patterns(level):
    easy = [
        "{first}@{domain}", "{first}.{last}@{domain}", "{first_initial}{last}@{domain}",
        "{first}{last}@{domain}", "{first}-{last}@{domain}"
    ]
    medium = easy + [
        "{last}.{first}@{domain}", "{first_initial}.{last}@{domain}", "{first}{last_initial}@{domain}",
        "{first}.{middle}.{last}@{domain}", "{first_initial}{middle_initial}{last}@{domain}"
    ]
    hard = medium + [
        "{first}{middle}{last}@{domain}", "{first}-{middle}-{last}@{domain}", "{last}{first_initial}@{domain}",
        "{first}{middle_initial}{last}@{domain}", "{first}.{middle_initial}.{last}@{domain}"
    ]
    return easy if level == 1 else medium if level == 2 else hard

def generate_emails(names, patterns, domain):
    emails = set()
    for name in names:
        parts = name.lower().split()
        if len(parts) < 2: continue  # Ensure at least first and last name exist
        ph = {
            "first": parts[0], "last": parts[-1], "first_initial": parts[0][0], "last_initial": parts[-1][0],
            "middle": "".join(parts[1:-1]), "middle_initial": "".join(p[0] for p in parts[1:-1]), "domain": domain
        }
        emails.update([p.format(**ph) for p in patterns if "{middle}" not in p or ph["middle"]])
    return list(emails)

def menu():
    print("""
\n# DISCLAIMER: This script is for ethical use only. The author holds no responsibility for misuse.\n
Phisher Buff [by 99tea]
1. Generate Email Addresses
2. Validate Email Addresses
3. Exit
""")

def main():
    while True:
        menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            names_file = input("Names file path: ").strip()
            if not os.path.exists(names_file):
                print("File not found.")
                continue

            names = read_file(names_file)
            if not names:
                print("File is empty.")
                continue

            domain = input("Domain (e.g., company.com): ").strip()
            if not domain:
                print("Invalid domain.")
                continue

            complexity = input("1: Easy\n2: Medium\n3: Hard\n0: Custom\nChoose complexity: ").strip()
            if complexity in "123":
                patterns = generate_patterns(int(complexity))
            else:
                print("Supported placeholders: {first}, {last}, {middle}, {first_initial}, {last_initial}, {domain}")
                patterns = [input("Custom pattern: ").strip()]

            try:
                output = "generated_emails.txt"
                mode = "a" if os.path.exists(output) else "w"
                with open(output, mode, encoding="utf-8") as f:
                    f.write("\n".join(generate_emails(names, patterns, domain)) + "\n")
                print(f"Emails saved to {output}.")
            except ValueError as e:
                print(e)

        elif choice == "2":
            file = input("Emails file: ").strip()
            if not os.path.exists(file):
                print("File not found.")
                continue

            proxy_file = input("Proxy file (optional, press Enter to skip): ").strip()
            emails = read_file(file)
            proxies = [p.split(":") for p in read_file(proxy_file)] if proxy_file else []

            results, threads, proxy_idx = defaultdict(tuple), [], 0
            for email in emails:
                mx = get_mx(email.split("@")[1])
                proxy = proxies[proxy_idx] if proxies else None
                threads.append(threading.Thread(target=validate, args=(email, mx, results, proxy)))
                threads[-1].start()
                proxy_idx = (proxy_idx + 1) % len(proxies) if proxies else 0

            [t.join() for t in threads]
            valid_emails = [email for email, (valid, _) in results.items() if valid]
            print("\n".join([f"[✔] {email}" if valid else f"[✖] {email} ({resp})" for email, (valid, resp) in results.items()]))
            output = "valid_emails.txt"
            mode = "a" if os.path.exists(output) else "w"
            with open(output, mode, encoding="utf-8") as f:
                f.writelines(e + "\n" for e in valid_emails)

        elif choice == "3":
            print("Exiting Phisher Buff. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__": main()
