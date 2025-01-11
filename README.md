# DISCLAIMER: This script is for ethical use only. The author holds no responsibility for misuse.


# Phisher Buff

**Phisher Buff** is an advanced email enumeration tool designed for penetration testers and cybersecurity researchers. It automates the process of verifying email addresses against a target domain using SOCKS5 proxies for anonymity.


## Features

- Generate possible email addresses based on names and patterns.
- Validate email addresses by checking their MX records.
- Supports SOCKS5 proxies for validation.
- Multithreaded email validation for faster processing.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/phisher-buff.git
cd phisher-buff
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python phisher_buff.py
```

### Menu Options:

1. **Generate Email Addresses**
   - Input: File containing names, target domain, and complexity level (or custom patterns).
   - Output: A file `generated_emails.txt` with possible email addresses.

2. **Validate Email Addresses**
   - Input: A file containing emails.
   - Output: A file `valid_emails.txt` with validated email addresses.

### Example

#### Generating Emails

Create a `names.txt` file with names:
```
John Doe
Jane Smith
```

Run the tool, select option 1, and enter:
```
Names file path: names.txt
Domain: example.com
Choose complexity: 2 (Medium)
```
This will generate emails like:
```
jdoe@example.com
jsmith@example.com
john.d@example.com
...
```

#### Validating Emails

Create an `emails.txt` file with email addresses:
```
jdoe@example.com
invalidemail@fake.com
```

Run the tool, select option 2, and enter:
```
Emails file: emails.txt
Proxy file (optional):
```
The tool will validate them and save valid ones to `valid_emails.txt`.

## Notes

- The tool does **not** send actual emails, it only checks MX records and responses from the mail server.
- Use responsibly and ensure compliance with ethical and legal guidelines.

## License

This project is licensed under the MIT License.

## Author

Developed by [99tea](https://github.com/yourusername).

