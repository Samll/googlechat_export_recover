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

---

## **Usage**

1. **Export your Google Chat data**:
   - Visit [Google Takeout](https://takeout.google.com/).
   - Select **Google Chat** from the list of services.
   - Export your data by following the on-screen instructions.

2. **Unzip the exported data**:
   - Once downloaded, unzip the Google Takeout archive into a folder of your choice.

3. **Run the script**:
   - Place the `googlechat_export_recover.py` script in the root of the unzipped folder.
   - Open a terminal or command prompt, navigate to the folder, and run the following command:
     ```bash
     python googlechat_export_recover.py
     ```

4. **Explore the results**:
   - The script will process all subfolders recursively and organize chats:
     - Each chat will have its own folder renamed based on the group name or participants' names.
     - Inside each folder, you will find an HTML file (e.g., `Group_Name_Chat.html`) containing the chat conversation.


