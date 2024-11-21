# googlechat_export_recover
A Python script to export Google Chat data into organized HTML files with folder renaming

## Usage
1. Go to https://takeout.google.com/ and export all Google Chats
2. Once downloaded unzip all the content in one folder
3. Add googlechat_export_recover.py to the main Takeout folder
4. Run python googlechat_export_recover.py
5. You can now browse folders, that will have name for the Group or members of the chat
6. Inside each folder you will find an HTML file named as the folder which contains all the chat

# **Google Chat Export Recovery**

A Python script to export Google Chat data into organized HTML files, with automatic folder renaming based on chat participants or group names.

---

## **Features**
- Converts Google Chat data into HTML files for easy browsing.
- Includes thumbnail images in chat allowing to show them in full size
- Creates links to ease finding attachments that are not images
- Automatically renames folders to match the group or chat participants.
- Handles special cases:
  - Supports multi-level folder structures from Google Takeout.
  - Renames folders uniquely to avoid conflicts.
  - Adds "DeletedUser" for single-member chats.
  - Processes group entries by extracting names from email addresses.

---

## **Prerequisites**
- Python 3.7 or higher.
- [Jinja2](https://pypi.org/project/Jinja2/) library for templating.

Install dependencies with:
```bash
pip install jinja2
