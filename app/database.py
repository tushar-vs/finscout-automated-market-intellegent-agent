import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name="market_data.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Creates the table if it doesn't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                name TEXT,
                price REAL,
                change TEXT,
                volume REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        logger.info("Database initialized.")

    def save_bulk(self, records):
        """Saves a list of dictionaries to the database."""
        if not records:
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Prepare the query
        query = '''
            INSERT INTO stocks (symbol, name, price, change, volume)
            VALUES (?, ?, ?, ?, ?)
        '''
        
        # Convert list of dicts to list of tuples for SQLite
        data_tuples = [
            (r['symbol'], r['name'], r['price'], r['change'], r['volume']) 
            for r in records
        ]
        
        cursor.executemany(query, data_tuples)
        conn.commit()
        conn.close()
        logger.info(f"Saved {len(records)} records to DB.")

    def get_all(self):
        """Retrieves all records."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stocks ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        
        # Convert back to dicts
        results = []
        for row in rows:
            results.append({
                "id": row[0],
                "symbol": row[1],
                "name": row[2],
                "price": row[3],
                "change": row[4],
                "volume": row[5],
                "timestamp": row[6]
            })
        return results

# Singleton instance
db = Database()