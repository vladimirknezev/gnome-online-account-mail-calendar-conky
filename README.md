# 🚀 gnome-online-account-mail-calendar-conky

**A Python script that fetches mail and calendar via GNOME Online Accounts for Conky, with built-in timeout protection against zombie processes.**

---

## 🌟 Key Features
* **🛡️ Zombie Process Protection:** Uses `socket.setdefaulttimeout()` to ensure the script terminates if the network hangs, preventing Conky from freezing or piling up background processes.
* **🔐 Secure Authentication:** Utilizes GOA's OAuth2 tokens. No need to hardcode your passwords into the scripts.
* **⚡ Lightweight:** Designed to run as a background hook for Conky with minimal resource usage.

---

## 📁 Scripts
1.  **`mail.py`**: Fetches the latest unread emails from your connected Gmail or Outlook accounts.
2.  **`email-to-password.py`**: (Alternative) Uses IMAP login with App Passwords. Use this for Yahoo, AOL, or providers that don't support GOA tokens.
3.  **`calendar.py`**: Retrieves upcoming events from your synchronized Google calendar.

---

## 🔑 Special Note for Yahoo/AOL Users (Added to Setup)
If you see an "Authentication Failed" or "Token Error" message for your account:

Use the email-to-password.py script.

Go to your provider's Account Security settings.

Select "Generate App Password".

Copy the 16-character code and paste it into the PASSWORD field in the script.

## 🛡️ Why it's Legal and Secure
Official Protocols: The scripts use standard IMAP and DBus interfaces provided by the OS and email providers.

Local Processing: Your credentials and emails never leave your computer; they are sent directly to the email server via SSL.

No Main Password: Using App Passwords ensures your primary account password remains private.

---

## 🛠️ Requirements
Make sure you have the following packages installed (example for Ubuntu/Debian):

```bash
sudo apt install python3-dbus python3-gi gir1.2-edataserver-1.2 libsecret-tools gnome-online-accounts-gtk
```
---

## 📖 Setup Instructions
Follow these steps to get the scripts running on your system:

1️⃣ GNOME Online Accounts (GOA) Login
Open your system Settings and navigate to Online Accounts.

Log in to your Google or Microsoft accounts. The scripts will automatically detect these sessions.

2️⃣ Folder Configuration
Create a folder named .conky in your Home directory: mkdir -p ~/.conky

Copy mail.py and calendar.py into the ~/.conky/ folder.

3️⃣ Grant Execution Permissions
You must allow the system to run these scripts as programs. Open your terminal and run:

```bash
chmod +x ~/.conky/mail.py
chmod +x ~/.conky/email-to-password.py
chmod +x ~/.conky/calendar.py
```
4️⃣ Activation
Open Conky Manager on your Linux distribution.

Refresh the list of widgets and scripts.

Select the scripts to display them on your desktop.

---

## Visual Overview (Screenshots)

### 📧 Email Overview
This shows how the script automatically groups unread emails by account (IMAP and Google OAuth2).
![Mail Preview](mail.png)

### 📅 Calendar and Holidays
Display of upcoming religious, national holidays, and personal reminders.
![Calendar Preview](calendar.png)
---
## ⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.
