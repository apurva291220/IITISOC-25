import email # parsing email files
import re 
import os #interacting with the file system
import hashlib #calculating file hashes, which helps in detecting known malware signature 

# List of suspicious keywords commonly seen in phishing attempts
SUSPICIOUS_KEYWORDS = ['verify your account', 'urgent', 'login', 'password', 'click here']

# List of file extensions often associated with malware
SUSPICIOUS_EXTENSIONS = [ '.exe', '.js', '.scr', '.bat', '.vbs']

KNOWN_MALICIOUS_HASHES = {'e99a18c428cb38d5f260853678922e03', } # example md5 hash,detect malware

def is_suspicious_header(msg):
    #Check for header mismatches, eg.'Reply-To' differs from 'From'.
    from_addr = msg.get('From', '')
    reply_to = msg.get('Reply-To', '')
    # Header mismatch is a common phishing indicator
    return from_addr and reply_to and from_addr != reply_to

def contains_suspicious_keywords(text):
     #Check if email body contains suspicious phishing keywords.
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
    """
    Scan a single .eml file for signs of malicious content.
    Prints alerts for each suspicious finding.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f)

    issues_found = False
    # Header analysis
    if is_suspicious_header(msg):
        print("-> Suspicious header mismatch detected!")
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
        print("-> Suspicious phishing keywords detected in body!")
        issues_found = True
        
    if contains_suspicious_links(body):
        print("-> Suspicious links detected in body!")
        issues_found = True
        
    #  Attachment analysis
    if has_malicious_attachment(msg):
        print("-> Suspicious or malicious attachment detected!")
        issues_found = True
          
    if not issues_found:
        print("-> Provided mail looks safe,No threats detected!")

def scan_folder(folder_path):
    #Scan all .eml files in the specified folder.
    for filename in os.listdir(folder_path):
        if filename.endswith('.eml'):
            print(f"Scanning {filename}:")
            scan_email(os.path.join(folder_path, filename))
            print('-' * 100)

if __name__ == '__main__':
    scan_folder('emails')
    #scans all mail provided in folder
