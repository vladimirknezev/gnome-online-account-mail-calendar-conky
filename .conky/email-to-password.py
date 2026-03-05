import imaplib
import email
import socket
from email.header import decode_header
from email.utils import parsedate_to_datetime

# --- GENERIC CONFIGURATION ---
# Use this script for accounts that don't support OAuth2 tokens in GOA.
# For services with 2-Step Verification, generate an "App Password" (16 chars).
EMAIL = "your_email@provider.com"
PASSWORD = "your_app_password_or_secret"
IMAP_SERVER = "imap.yourprovider.com" # e.g., imap.mail.yahoo.com or imap.aol.com
# -----------------------------

# Connection timeout to prevent Conky from freezing
socket.setdefaulttimeout(15)

def fetch_conky_emails(count=2):
    mail = None
    try:
        # Establish a secure connection to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("INBOX", readonly=True)

        # Search for all messages
        status, messages = mail.search(None, 'ALL')
        mail_ids = messages[0].split()
        
        if not mail_ids:
            return

        # HEADER - Identical to your GOA script style
        print(f"--- {EMAIL.upper()} ---")

        # Process the most recent emails
        for mail_id in reversed(mail_ids[-count:]):
            res, msg_data = mail.fetch(mail_id, "(RFC822)")

            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    # 1. DECODE SENDER
                    from_h = decode_header(msg.get("From", "Unknown"))[0]
                    sender = from_h[0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(from_h[1] or "utf-8", errors='ignore')
                    
                    # 2. DECODE SUBJECT
                    subj_h = decode_header(msg.get("Subject", "No Subject"))[0]
                    subject = subj_h[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(subj_h[1] or "utf-8", errors='ignore')

                    # 3. FORMAT DATE
                    date_raw = msg.get("Date")
                    try:
                        dt = parsedate_to_datetime(date_raw).astimezone()
                        # Matching the format from your successful tests: "05 Mar 13:58"
                        date_display = dt.strftime("%d %b %H:%M")
                    except: 
                        date_display = date_raw

                    # 4. EXTRACT BODY (Strictly Plain Text to avoid HTML code in Conky)
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                try:
                                    payload = part.get_payload(decode=True)
                                    body = payload.decode(part.get_content_charset() or 'utf-8', errors='ignore')
                                    break
                                except: pass
                    else:
                        payload = msg.get_payload(decode=True)
                        body = payload.decode(msg.get_content_charset() or 'utf-8', errors='ignore')

                    # Clean and truncate text for Conky layout
                    clean_text = " ".join(body.replace("\n", " ").split())
                    short_text = (clean_text[:100] + "...") if len(clean_text) > 100 else clean_text

                    # STANDARDIZED OUTPUT
                    print(f"TIME: {date_display}")
                    print(f"FROM: {sender}")
                    print(f"SUBJ: {subject}")
                    print(f"BODY: {short_text}")
                    print("-" * 40) # Standard separator length

        mail.logout()
    except Exception as e:
        # Silently fail or minimal error for Conky stability
        pass

if __name__ == "__main__":
    fetch_conky_emails(2)
