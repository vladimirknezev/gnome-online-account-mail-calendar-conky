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
2.  **`calendar.py`**: Retrieves upcoming events from your synchronized Google or Microsoft calendars.

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
chmod +x ~/.conky/calendar.py
```
4️⃣ Activation
Open Conky Manager on your Linux distribution.

Refresh the list of widgets and scripts.

Select the scripts to display them on your desktop.

---

## ⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.
