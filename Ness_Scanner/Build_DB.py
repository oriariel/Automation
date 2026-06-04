import sqlite3
import requests

DB_NAME = "ness_jobs.db"
API_BASE = "https://www.ness-tech.co.il/careers/api/Careers"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.ness-tech.co.il/careers/",
    "Accept": "application/json, text/plain, */*",
}

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS jobs")
    cursor.execute("""
        CREATE TABLE jobs (
            id       INTEGER PRIMARY KEY,
            title    TEXT NOT NULL,
            location TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized.")

def fetch_jobs() -> list:
    """Call the site's own REST API and return all job listings."""
    url = f"{API_BASE}/GetAllItems"
    print(f"Fetching: {url}")
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data.get("allOrderDetailsList", [])

def store_jobs(jobs: list):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    added = 0

    for job in jobs:
        job_id   = job.get("index")        # e.g. "42770"
        title    = job.get("title", "").strip()
        location = job.get("posLocation", "").strip()

        if not job_id or not title:
            continue
        try:
            job_id = int(job_id)
        except ValueError:
            print(f"  Skipping non-numeric ID: {job_id}")
            continue

        cursor.execute(
            "INSERT OR IGNORE INTO jobs (id, title, location) VALUES (?, ?, ?)",
            (job_id, title, location)
        )
        if cursor.rowcount:
            added += 1
            print(f"  ID {job_id:>6} | {title[:55]:<55} | {location}")

    conn.commit()
    conn.close()
    print(f"\nDone! Saved {added} jobs to '{DB_NAME}'.")

def main():
    init_database()
    jobs = fetch_jobs()
    print(f"API returned {len(jobs)} jobs.\n")
    store_jobs(jobs)

if __name__ == "__main__":
    main()
