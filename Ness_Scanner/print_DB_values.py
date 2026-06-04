import csv
import sqlite3


def clean_text(text):
    """Cleans up stray structural artifacts and trailing pipeline tokens."""
    if not text:
        return ""
    # Strip common visual separators that mess up alignments
    cleaned = text.replace("|", "").strip()
    return cleaned


def export_database_to_csv():
    db_name = "ness_jobs.db"
    output_filename = "ness_jobs_list.csv"

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Query the results
    cursor.execute("SELECT id, title, location FROM jobs ORDER BY id DESC")
    rows = cursor.fetchall()

    # Write out data directly into a clean UTF-8 CSV matrix
    # Using 'utf-8-sig' forces Excel to recognize Hebrew characters properly
    with open(
        output_filename, mode="w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.writer(file)

        # Write clean spreadsheet headers
        writer.writerow(["Job ID", "Job Title", "Location"])

        for row in rows:
            job_id = row[0]
            title = clean_text(row[1])
            location = clean_text(row[2])

            # Fix data leakage where location sneaks into the title column
            if location in title:
                title = title.replace(location, "").strip(" .-,/")

            # Write the cleaned row
            writer.writerow([job_id, title, location])

    conn.close()
    print(f"\nSuccess! Cleaned data written to '{output_filename}'")
    print(
        "You can now double-click this file to view it perfectly in Excel or Google Sheets!"
    )


if __name__ == "__main__":
    export_database_to_csv()