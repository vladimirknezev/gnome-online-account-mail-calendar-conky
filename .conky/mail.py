import subprocess
import imaplib
import email
import dbus
import socket
from email.header import decode_header
from email.utils import parsedate_to_datetime

# KEY: If any network operation takes longer than 10 seconds, the script terminates.
# This prevents "zombie" processes and keeps Conky stable.
socket.setdefaulttimeout(10)

def get_online_accounts():
    accounts = []
    try:
        bus = dbus.SessionBus()
        manager_obj = bus.get_object('org.gnome.OnlineAccounts', '/org/gnome/OnlineAccounts')
        manager = dbus.Interface(manager_obj, 'org.freedesktop.DBus.ObjectManager')
        # Timeout for DBus communication
        managed_objects = manager.GetManagedObjects(timeout=5)
        
        for path, interfaces in managed_objects.items():
            if 'org.gnome.OnlineAccounts.Account' in interfaces:
                acc_props = interfaces['org.gnome.OnlineAccounts.Account']
                acc_id = path.split('/')[-1]
                email_addr = str(acc_props['PresentationIdentity'])
                
                server = None
                if "gmail.com" in email_addr:
                    server = "imap.gmail.com"
                elif "hotmail.com" in email_addr or "outlook.com" in email_addr:
                    server = "imap-mail.outlook.com"
                
                if server:
                    accounts.append({'id': acc_id, 'user': email_addr, 'server': server})
    except: pass
    return accounts

def get_goa_token(acc_id):
    try:
        cmd = ["gdbus", "call", "--session", "--dest", "org.gnome.OnlineAccounts",
               "--object-path", f"/org/gnome/OnlineAccounts/Accounts/{acc_id}",
               "--method", "org.gnome.OnlineAccounts.OAuth2Based.GetAccessToken"]
        return subprocess.check_output(cmd, text=True, timeout=5).split("'")[1]
    except: return None

def process_mail_engine(server, user, token, count=2):
    mail = None
    try:
        # IMAP connection with timeout
        mail = imaplib.IMAP4_SSL(server, timeout=10)
        auth_string = f"user={user}\x01auth=Bearer {token}\x01\x01"
        mail.authenticate('XOAUTH2', lambda x: auth_string)
        mail.select("INBOX", readonly=True)
        
        status, messages = mail.search(None, 'ALL') 
        mail_ids = messages[0].split()
        
        if not mail_ids: return

        # HEADER STYLE: Matches your provided screenshots
        print(f"--- {user.upper()} ---")

        for mail_id in reversed(mail_ids[-count:]):
            res, msg_data = mail.fetch(mail_id, "(RFC822)")
            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    # 1. FROM
                    from_header = decode_header(msg.get("From", "Unknown"))[0]
                    sender = from_header[0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(from_header[1] or "utf-8", errors='ignore')
                    
                    # 2. SUBJECT
                    subject_header = decode_header(msg.get("Subject", "No Subject"))[0]
                    subject = subject_header[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(subject_header[1] or "utf-8", errors='ignore')

                    # 3. TIME
                    date_str = msg.get("Date")
                    try:
                        dt = parsedate_to_datetime(date_str).astimezone()
                        # Clean date format: "05 Mar 13:33"
                        formatted_date = dt.strftime("%d %b %H:%M")
                    except: 
                        formatted_date = date_str

                    # 4. BODY (Filtering for plain text to avoid raw HTML)
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

                    clean_body = " ".join(body.replace("\n", " ").split())
                    short_body = (clean_body[:80] + "...") if len(clean_body) > 80 else clean_body

                    # OUTPUT: Standardized labels and separators
                    print(f"TIME: {formatted_date}")
                    print(f"FROM: {sender}")
                    print(f"SUBJ: {subject}")
                    print(f"BODY: {short_body}")
                    print("-" * 40) # Line separator matching your style
        
        mail.logout()
    except:
        if mail:
            try: mail.logout()
            except: pass

if __name__ == "__main__":
    nalozi = get_online_accounts()
    for nalog in nalozi:
        token = get_goa_token(nalog['id'])
        if token:
            process_mail_engine(nalog['server'], nalog['user'], token)
