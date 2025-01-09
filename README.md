# Phisher Buff

Phisher Buff is an advanced email enumeration tool designed for penetration testers and cybersecurity researchers. It automates the process of verifying email addresses against a target domain using SOCKS5 proxies for anonymity.

## Features
- **Pattern Recognition** optimizes enumeration by identifying common email patterns
- **Multi-threaded execution** for faster enumeration
- **SOCKS5 proxy support** with automatic rotation from a provided proxy list
- **Smart enumeration**: stops checking name variations once a valid email is found
- **Customizable input files** for name lists and proxy lists
- **Output file** with valid emails found during the enumeration

## Installation
### Prerequisites
Ensure you have the following dependencies installed:

```bash
pip install requirements.txt
```

### Cloning the Repository
```bash
git clone https://github.com/Danilo-Mugnaini/phisher_buff.git
cd phisher_buff
```

## Usage
Run the script with the following command:

```bash
python3 phisher_buff.py
```

### Required Inputs
Upon execution, the script prompts for:
- **Path to names file** (e.g., `names.txt` containing possible usernames)
- **Target email domain** (e.g., `example.com`)
- **A known valid email and corresponding full name** (optional, used for refining formats)
- **Path to proxy list file** (e.g., `proxylist.txt` with SOCKS5 proxies in `host:port` format)

### Example Execution
```bash
$ python3 phisher_buff.py
Path to names file: names.txt
Target email domain: example.com
Known full name (or press Enter to skip): John Doe
Known email (or press Enter to skip): jdoe@example.com
Path to proxy list file: proxylist.txt
```

## Output
- **Valid emails** are saved in `valid_emails.txt`.
- Logs display errors or timeouts related to proxy connections.

## Contributing
Contributions are welcome! Feel free to submit a pull request or report issues.

## License
This project is licensed under the MIT License.

## Disclaimer
This tool is intended for **ethical cybersecurity research and authorized penetration testing only**. Misuse of this tool may result in legal consequences. The author is not responsible for any unethical or illegal activities conducted using this software.

