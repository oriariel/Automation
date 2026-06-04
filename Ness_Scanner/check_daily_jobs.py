import os
import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

DB_NAME = "ness_jobs.db"
API_BASE = "https://www.ness-tech.co.il/careers/api/Careers"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.ness-tech.co.il/careers/",
    "Accept": "application/json, text/plain, */*",
}

# --- הגדרות שליחת המייל ---
SENDER_EMAIL = "oriariel0@gmail.com"
RECEIVER_EMAIL = "oriariel0@gmail.com"
# החלף את המחרוזת הבאה בסיסמת האפליקציה בת 16 האותיות שקיבלת מגוגל:
SENDER_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

def get_existing_job_ids() -> set:
    """שולף את כל ה-IDs שכבר קיימים במסד הנתונים."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
    if not cursor.fetchone():
        conn.close()
        return set()
    cursor.execute("SELECT id FROM jobs")
    existing_ids = {row[0] for row in cursor.fetchall()}
    conn.close()
    return existing_ids

def fetch_live_jobs() -> list:
    """שולף את המשרות הנוכחיות מהאתר."""
    url = f"{API_BASE}/GetAllItems"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return resp.json().get("allOrderDetailsList", [])
    except Exception as e:
        print(f"שגיאה בתקשורת עם ה-API: {e}")
        return []

def send_email_notification(new_jobs: list):
    """מנסח ושולח אימייל מעוצב ב-HTML עם רשימת המשרות החדשות."""
    print("מכין את שליחת המייל...")
    
    # יצירת אובייקט המייל
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🔥 נמצאו {len(new_jobs)} משרות חדשות בנס טכנולוגיות!"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    # בניית טבלת משרות מעוצבת ב-HTML (נראה מעולה גם בנייד)
    table_rows = ""
    for job_id, title, location in new_jobs:
        job_url = f"https://www.ness-tech.co.il/careers/job/{job_id}"
        table_rows += f"""
        <tr style="border-bottom: 1px solid #dddddd;">
            <td style="padding: 12px; text-align: right; font-weight: bold; color: #333;">{job_id}</td>
            <td style="padding: 12px; text-align: right;"><a href="{job_url}" style="color: #0066cc; text-decoration: none; font-weight: bold;">{title}</a></td>
            <td style="padding: 12px; text-align: right; color: #666;">{location}</td>
        </tr>
        """

    html_content = f"""
    <html dir="rtl">
    <head>
        <meta charset="utf-8">
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f9; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.05); border-top: 5px solid #0066cc;">
            <h2 style="color: #333333; text-align: center;">הסורק האוטומטי זיהה עדכון!</h2>
            <p style="font-size: 16px; color: #555555; text-align: center;">להלן המשרות החדשות שנוספו לאתר נס היום ({datetime.now().strftime('%d/%m/%Y')}):</p>
            
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <thead>
                    <tr style="background-color: #0066cc; color: white;">
                        <th style="padding: 12px; text-align: right;">קוד משרה</th>
                        <th style="padding: 12px; text-align: right;">תפקיד</th>
                        <th style="padding: 12px; text-align: right;">מיקום</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
            
            <hr style="border: 0; border-top: 1px solid #eeeeee; margin-top: 30px;">
            <p style="font-size: 12px; color: #999999; text-align: center;">הודעה זו נשלחה באופן אוטומטי על ידי Ness_Scanner הפועל על המחשב שלך.</p>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # התחברות לשרת ה-SMTP של גוגל ושליחה מאובטחת
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # הצפנת TLS להעברה מאובטחת
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("האימייל נשלח בהצלחה רבה!")
    except Exception as e:
        print(f"שגיאה בשליחת המייל: {e}")

def process_daily_updates():
    print(f"--- בדיקת משרות יומית: {datetime.now().strftime('%d/%m/%Y %H:%M')} ---")
    
    existing_ids = get_existing_job_ids()
    if not existing_ids:
        print("מסד הנתונים ריק או לא מאותחל. מריץ סריקה ראשונית שקטה כדי לא להציף במייל...")
        
    live_jobs = fetch_live_jobs()
    if not live_jobs:
        print("לא התקבלו נתונים מהאתר. הבדיקה נעצרה.")
        return

    new_jobs_to_add = []
    for job in live_jobs:
        raw_id = job.get("index")
        title = job.get("title", "").strip()
        location = job.get("posLocation", "").strip()
        
        if not raw_id or not title:
            continue
            
        try:
            job_id = int(raw_id)
        except ValueError:
            continue
            
        if job_id not in existing_ids:
            new_jobs_to_add.append((job_id, title, location))

    if not new_jobs_to_add:
        print("\nסריקה הושלמה: אין משרות חדשות. הכל מעודכן!")
        if existing_ids:  # only if DB was already populated (not first run)
            send_no_new_jobs_email()
        return

    # עדכון מסד הנתונים
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

# Create the table if it doesn't exist yet
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id         INTEGER PRIMARY KEY,
            title      TEXT NOT NULL,
            location   TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """ )
    
    for job_id, title, location in new_jobs_to_add:
        cursor.execute(
            "INSERT INTO jobs (id, title, location) VALUES (?, ?, ?)",
            (job_id, title, location)
        )
        print(f"  [חדש ב-DB] ID: {job_id:>6} | {title[:40]:<40} | {location}")
        
    conn.commit()
    conn.close()
    
    # **שליחת המייל מתבצעת רק אם מסד הנתונים לא היה ריק לחלוטין מלכתחילה**
    # זה מונע מצב שבהרצה הראשונה תקבל מייל ענק עם 190 משרות ישנות.
    if existing_ids:
        send_email_notification(new_jobs_to_add)
    else:
        print("\nמסד הנתונים אותחל מחדש עם כל משרות האתר. הודעות מייל ישלחו החל מהמשרה החדשה הבאה!")

def send_no_new_jobs_email():
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"✅ סריקת נס – {datetime.now().strftime('%d/%m/%Y')} – אין משרות חדשות"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    html_content = f"""
    <html dir="rtl">
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f9; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.05); border-top: 5px solid #28a745;">
            <h2 style="color: #333333; text-align: center;">✅ לא עודכנו משרות חדשות</h2>
            <p style="font-size: 16px; color: #555555; text-align: center;">הסריקה היומית הושלמה בהצלחה – אין משרות חדשות באתר נס נכון להיום ({datetime.now().strftime('%d/%m/%Y %H:%M')}).</p>
            <hr style="border: 0; border-top: 1px solid #eeeeee; margin-top: 30px;">
            <p style="font-size: 12px; color: #999999; text-align: center;">הודעה זו נשלחה באופן אוטומטי על ידי Ness_Scanner.</p>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("נשלח מייל: אין משרות חדשות.")
    except Exception as e:
        print(f"שגיאה בשליחת המייל: {e}")

if __name__ == "__main__":
    process_daily_updates()
    #send_email_notification([(99999, "משרת בדיקה", "אזור המרכז")])