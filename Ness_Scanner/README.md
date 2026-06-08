# Ness Job Scanner

A Python-based job monitoring system that automatically tracks new job postings on the Ness Technologies careers website and sends email notifications whenever new positions are published.

## Features

* Retrieves all active job listings directly from the Ness Careers API.
* Stores job data locally in a SQLite database.
* Detects newly published jobs by comparing current listings with previously stored data.
* Sends formatted HTML email notifications for new jobs.
* Sends daily status emails when no new jobs are found.
* Exports the database into a clean CSV file for Excel or Google Sheets analysis.
* Can be scheduled to run automatically using Windows Task Scheduler.

---

## Project Structure

```text
.
├── Build_DB.py              # Initial database creation and population
├── check_daily_jobs.py      # Daily job scanner and email notification system
├── print_DB_values.py       # Export database contents to CSV
├── ness_jobs.db             # SQLite database
├── ness_jobs_list.csv       # Exported CSV file
├── run_scanner.bat          # Batch file for scheduled execution
└── README.md
```

---

## Requirements

Python 3.9+

Install dependencies:

```bash
pip install requests
```

Built-in modules used:

* sqlite3
* smtplib
* email
* datetime
* csv
* os

---

## How It Works

### Step 1: Initialize Database

Run:

```bash
python Build_DB.py
```

This script:

1. Creates a fresh SQLite database.
2. Downloads all current job listings from the Ness Careers API.
3. Stores them locally.

---

### Step 2: Configure Email Notifications

The project uses Gmail SMTP.

Create a Gmail App Password and set it as an environment variable:

#### Windows

```cmd
setx GMAIL_APP_PASSWORD "your_16_character_app_password"
```

#### PowerShell

```powershell
$env:GMAIL_APP_PASSWORD="your_16_character_app_password"
```

Update the following values if needed:

```python
SENDER_EMAIL = "your_email@gmail.com"
RECEIVER_EMAIL = "your_email@gmail.com"
```

---

### Step 3: Run Daily Scanner

Run:

```bash
python check_daily_jobs.py
```

The scanner will:

* Download current job listings.
* Compare them against the local database.
* Insert newly discovered jobs.
* Send an email notification if new jobs are found.

---

## Email Notifications

When new jobs are detected:

* A styled HTML email is sent.
* Each job contains:

  * Job ID
  * Job Title
  * Location
  * Direct link to the position

Example email subject:

```text
🔥 Found 3 New Jobs at Ness Technologies!
```

If no new jobs are found:

```text
✅ Ness Daily Scan – No New Jobs Found
```

---

## Export Jobs to CSV

Run:

```bash
python print_DB_values.py
```

This creates:

```text
ness_jobs_list.csv
```

The CSV contains:

| Job ID | Job Title | Location |
| ------ | --------- | -------- |

The file is encoded using UTF-8 BOM to ensure proper Hebrew support in Microsoft Excel.

---

## Scheduling

You can automate execution using Windows Task Scheduler.

Example command:

```cmd
python check_daily_jobs.py
```

Or use the provided batch file:

```cmd
run_scanner.bat
```

Schedule it daily to receive automatic updates whenever new jobs are posted.

---

## Data Source

Job listings are retrieved from the public Ness Technologies Careers API:

```text
https://www.ness-tech.co.il/careers/api/Careers/GetAllItems
```

---

## Database Schema

```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Example Workflow

```text
1. Run Build_DB.py once
2. Schedule check_daily_jobs.py daily
3. Receive email alerts when new jobs appear
4. Export results using print_DB_values.py whenever needed
```

---

## Author

Created as a personal job-monitoring automation project using Python, SQLite, REST APIs, and SMTP email notifications.
