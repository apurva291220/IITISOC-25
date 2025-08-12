# Cybersecurity Suite for Enhanced Digital Security (IITISOC-25)

A beginner-friendly, multi-module cybersecurity suite designed to help users understand and mitigate digital threats such as weak passwords, phishing emails, credential harvesting, and unauthorized file modifications.

---

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Module Details](#module-details)
    - [Password Checker](#password-checker)
    - [Malicious Mail Identifier](#malicious-mail-identifier)
    - [Keylogger & Phishing Page Demo](#keylogger--phishing-page-demo)
    - [File Integrity Checker](#file-integrity-checker)
- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
- [Deliverables](#deliverables)
- [License](#license)
- [About Team Members](#team-memberdetails)
- [Contact](#contact)

---

## Description

This is a comprehensive cybersecurity learning suite comprising four integrated modules:
- Password Checker
- Malicious Mail Identifier
- Keylogger & Phishing Page Demo
- File Integrity Checker

The suite equips beginners with hands-on tools and knowledge to better secure digital data, detect threats, and understand common vulnerabilities.

---

## Features

- Unified command-line or GUI-based interface for all modules
- Real-time feedback (e.g., live password strength)
- In-depth user documentation and code comments
- Modular and extensible design for learning and experimentation

---

## Module Details

### Password Checker

- Evaluates the strength of user-chosen passwords
- Assesses length, variety, patterns; classifies password strength (Weak, Moderate, Strong)
- Offers actionable recommendations for improvement
- [Directory: `/passwordchecker/`]

### Malicious Mail Identifier

- Analyzes email headers, body text, and attachments for phishing, malware, or suspicious links
- Uses heuristics such as header mismatches, suspicious keywords/URLs, file-signature checks
- [Directory: `/malicious_mail_identifier/`]

### Keylogger & Phishing Page Demo

- Demonstrates how credential harvesting works for educational purposes
- Includes a basic keylogger to log sample keystrokes
- Provides an educational login page clone for demo purposes, with ethical usage warnings
- [Directory: `/Keylogger&Phishing_Demo/`]

### File Integrity Checker

- Detects unauthorized changes to files by computing/comparing SHA-256 hashes
- **Snapshot Mode**: Save baseline hashes for specified files/folders
- **Verify Mode**: Compare current hashes and flag changes or missing files
- Supports exclusions and CSV/text reporting
- [Directory: `/File_Integrity_Checker/`]

---

## Installation

1. **Clone the Repository**
```
     git clone https://github.com/apurva291220/IITISOC-25.git
     cd IITISOC-25
   ```
2. **Install Requirements (if needed)**
```
pip install -r requirements.txt
```
*Note: Some modules may not require external libraries.*

3. **Launch GUI Interface**
```
python gui.py
```
You can also run individual modules:
```
python passwordchecker/passwordchecker.py
python malicious_mail_identifier/mail_scanner.py
```

---

## Directory Structure
```

- IITISOC-25/
├── File_Integrity_Checker/ # Module for file integrity verification using SHA-256 hashes
├── Keylogger&Phishing_Demo/ # Educational demo for keylogging and phishing techniques
├── malicious_mail_identifier/ # Module to detect phishing and malicious emails
├── passwordchecker/ # Password strength checking module
├── src/ # Source files (shared/common code and utilities)
├── gui.py # Main GUI interface script
├── user_manual 
├── README.md # Project documentation and overview
├── LICENSE # License information for the project
└── requirements.txt # Python dependencies list

```
---

## Usage

- **Run Main Interface:**
 ```
 python gui.py
 ```
- **Run Individual Modules:**  
 Check the respective module directories for more specific usage instructions and example commands.

---

## Deliverables

- A working suite integrating all four tools
- User manuals with example workflows and setup instructions
- Test cases and sample results for each tool
- Password Checker: Sample password strength classification
- Mail Identifier: Tests with safe, phishing, and malicious emails
- Keylogger Demo: Simulated keystroke/event logging
- File Integrity Checker: Change detection reports

---

## License

Distributed under the MIT License.

---

## About Team Members
Team Leader: APURVA BAVISKAR
Implemented password checker & malicious mail identifier.
Integrated into GUI.

Team Member: APURVA CHIPTE
Implemented keylogger,phishing demo & file integrity checker.

---



## Contact

For questions, issues, or suggestions, please open an issue on GitHub or reach out to the repository maintainers.





