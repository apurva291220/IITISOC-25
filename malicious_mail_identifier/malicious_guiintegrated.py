import email # parsing email file
import re 
import os #interacting with the file system 
import hashlib #calculating file hashes, which helps in detecting known malware signature 
import tkinter as tk
from tkinter import filedialog, scrolledtext


# List of suspicious words often found in phishing emails
SUSPICIOUS_KEYWORDS = ['verify your account', 'urgent', 'login', 'password', 'click here']
# File types commonly used as malicious attachments
SUSPICIOUS_EXTENSIONS = ['.exe', '.js', '.scr', '.bat', '.vbs']
# Example hash set; replace with known real hashes as you wish
KNOWN_MALICIOUS_HASHES = {'e99a18c428cb38d5f260853678922e03'}

def is_suspicious_header(msg):
   #Check for header mismatches, eg.'Reply-To' differs from 'From'.
    from_addr = msg.get('From', '')
    reply_to = msg.get('Reply-To', '')
    # Header mismatch is a common phishing indicator
    return from_addr and reply_to and from_addr != reply_to

def contains_suspicious_keywords(text):
   # Header mismatch is a common phishing indicator
    for kw in SUSPICIOUS_KEYWORDS:
        if kw.lower() in text.lower():
            return True
    return False

def contains_suspicious_links(text):
     #Search for suspicious URLs in the email body using heuristics.
    urls = re.findall(r'https?://\S+', text)
    for url in urls:
       # Heuristic: check for keywords in URLs often used in phishing
        if any(word in url for word in ['login', 'secure', 'update']):
            return True
    return False

def has_malicious_attachment(msg):
   #Check for attachments with suspicious extensions or known malicious signatures.
    for part in msg.walk():
        if part.get_content_disposition() == 'attachment':
            filename = part.get_filename()
             # Check for risky file extensions
            if filename and any(filename.lower().endswith(ext) for ext in SUSPICIOUS_EXTENSIONS):
                return True
            # File-signature (hash) check
            payload = part.get_payload(decode=True)
            if payload:
                file_hash = hashlib.md5(payload).hexdigest()
                if file_hash in KNOWN_MALICIOUS_HASHES:
                    return True
    return False

def scan_email(file_path):
    results = []
    """
    Scan a single .eml file for signs of malicious content.
    Prints alerts for each suspicious finding.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f)
    issues_found = False
    # Header analysis
    if is_suspicious_header(msg):
        results.append("-> Suspicious header mismatch detected!")
        issues_found = True
    # Body analysis
    body = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            try:
                body += part.get_payload(decode=True).decode(errors='ignore')
            except Exception:
                continue
    if contains_suspicious_keywords(body):
        results.append("-> Suspicious phishing keywords detected in body!")
        issues_found = True

    if contains_suspicious_links(body):
        results.append("-> Suspicious links detected in body!")
        issues_found = True
    #  Attachment analysis
    if has_malicious_attachment(msg):
        results.append("-> Suspicious or malicious attachment detected!")
        issues_found = True

    if not issues_found:
        results.append("-> Provided mail looks safe, No threats detected!")
    return results

def scan_folder(folder_path):
    output = []
     #Scan all .eml files in the specified folder.
    for filename in os.listdir(folder_path):
        if filename.endswith('.eml'):
            output.append(f"Scanning {filename}:")
            results = scan_email(os.path.join(folder_path, filename))
            output.extend(results)
            output.append('-' * 100)
    return "\n".join(output)

# GUI part
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        results_box.delete('1.0', tk.END)
        output = scan_folder(folder_selected) #scans all mail provided in folder
        results_box.insert(tk.END, output)

root = tk.Tk()
root.title("Malicious Mail Identifier")

browse_btn = tk.Button(root, text="Select Emails Folder", command=browse_folder)
browse_btn.pack(pady=10)

results_box = scrolledtext.ScrolledText(root, width=100, height=30, font=("Consolas", 15))
results_box.pack(padx=10, pady=10)

root.mainloop()

