# gnome-online-account-mail-calendar-conky
A Python script that fetches mail and calendar via GNOME Online Accounts for Conky, with built-in timeout protection against zombie processes.
# GNOME Online Accounts - Mail & Calendar for Conky

This repository contains Python scripts designed to fetch data from **GNOME Online Accounts (GOA)** and display them in **Conky**.

## 🚀 Key Features
- **Zombie Process Protection:** Uses `socket.setdefaulttimeout()` to ensure the script terminates if the network hangs, preventing Conky from freezing or piling up background processes.
- **Secure Authentication:** Utilizes GOA's OAuth2 tokens. No need to hardcode your passwords into the scripts.
- **Lightweight:** Designed to run as a background hook for Conky with minimal resource usage.

## 📁 Scripts
1. **`mail_check.py`**: Fetches the latest unread emails from your connected Gmail or Outlook accounts.
2. **`calendar.py`**: Retrieves upcoming events from your synchronized Google or Microsoft calendars.

## 🛠️ Requirements
Make sure you have the following packages installed (example for Ubuntu/Debian):
```bash
sudo apt install python3-dbus python3-gi gir1.2-edataserver-1.2 libsecret-tools gnome-online-accounts-gtk
