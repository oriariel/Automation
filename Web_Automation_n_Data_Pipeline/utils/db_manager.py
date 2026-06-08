# utils/db_manager.py
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="data/pipeline_data.db"):
        self.db_name = db_name
        self.init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Creates the product tracking table if it doesn't already exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT,
                    price TEXT,
                    scraped_at TEXT
                )
            """)
            conn.commit()

    def save_products(self, product_list):
        """Saves a batch of scraped items with a current timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Map the dictionary list to tuple rows for efficient batch inserting
            rows_to_insert = [
                (item['item'], item['price'], timestamp) 
                for item in product_list
            ]
            
            cursor.executemany("""
                INSERT INTO product_history (item_name, price, scraped_at)
                VALUES (?, ?, ?)
            """, rows_to_insert)
            
            conn.commit()
            print(f" Successfully archived {len(product_list)} records into local SQLite database.")