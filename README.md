# 🚀 gnome-online-account-mail-calendar-contact-conky-xfce4-genmon-plugin

A Python-based productivity suite for Linux. Monitor mail and calendar via Conky, and interact with your Google Contacts directly from the XFCE panel—all protected by built-in "anti-zombie" timeout logic.

---

## 🌟 Key Features
* **🛡️ Zombie Process Protection: Every script uses socket.setdefaulttimeout() to ensure the process terminates if the network hangs, preventing system freezes or resource accumulation.
* **🕹️ XFCE Cockpit Module: Beyond passive monitoring, you can now search contacts and copy phone numbers directly from your system panel using the interactive Genmon integration.
* **🔐 Secure Authentication: Utilizes GOA's OAuth2 tokens. No need to hardcode your passwords into the scripts.
* **⚡ Lightweight & Minimalist: Designed for power users who value system efficiency and native functionality over heavy extensions.

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
sudo apt install -y python3-dbus python3-gi gir1.2-edataserver-1.2 libsecret-tools gnome-online-accounts-gtk
```
---

## 📖 Setup Instructions Mail and Calendar
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

## 🛠️ NEW: XFCE Desktop Integration (The Cockpit Module)

This is a standalone interactive module designed specifically for **XFCE Desktop** users. It allows you to search contacts and monitor mail directly from your system panel using the `Genmon` plugin.

### 📁 Cockpit Scripts
* **`contact.py`**: High-speed SQLite search for Google Contacts. Supports **Reverse Lookup** (search by name or phone number).
* **`contact_genmon.sh`**: Bash wrapper that triggers the Zenity interface and copies numbers to the clipboard via `xclip`.

### 📦 Installation (Prerequisites)
To use the Cockpit Module, run:
```bash
sudo apt install -y python3 sqlite3 zenity xclip libnotify-bin xfce4-genmon-plugin gnome-online-accounts-gtk evolution-data-server
```
## 📖 Setup Instructions Contact
1️⃣ GNOME Online Accounts (GOA) Login
Open your system Settings and navigate to Online Accounts.

Log in to your Google. The scripts will automatically detect these sessions.

2️⃣ Folder Configuration & Permissions
```bash
mkdir -p ~/.script
# Copy contacts.py and contacts_launcher.sh to this folder
chmod +x ~/.script/*.py
chmod +x ~/.script/*.sh
```
3️⃣Add to XFCE Panel:
Right-click XFCE Panel -> Add New Items -> Generic Monitor (Genmon).
Right-click the new icon -> Properties.
```bash
bash -c "~/.script/contact_genmon.sh"
```
Label: Uncheck (Hidden).
* **Period (s):** `3600` (Or set to `0` to trigger ONLY on manual click, preventing unexpected pop-ups).
## ⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer
This project is intended for personal use only. The scripts access accounts that are already logged in via GNOME Online Accounts on your own system. The author is not responsible for any misuse of the code, including attempts to gain unauthorized access to other people's accounts or data. Use at your own risk.
