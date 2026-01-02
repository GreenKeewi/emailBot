"""
Persistent state management using SQLite database.
Tracks searches, businesses, and run history.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os


class HistoryStore:
    """Manages persistent state for the email outreach bot."""
    
    def __init__(self, db_path: str = "outreach_bot.db"):
        """Initialize the history store with SQLite database."""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Searches table - tracks search coverage
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                province TEXT NOT NULL,
                city TEXT NOT NULL,
                category TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                radius INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                last_run_timestamp TEXT,
                businesses_found INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                UNIQUE(province, city, category, latitude, longitude, radius)
            )
        """)
        
        # Businesses table - tracks discovered businesses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                website TEXT,
                email TEXT,
                city TEXT NOT NULL,
                category TEXT NOT NULL,
                province TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                latitude REAL,
                longitude REAL,
                email_sent BOOLEAN DEFAULT 0,
                email_sent_timestamp TEXT,
                site_analysis TEXT,
                created_at TEXT NOT NULL,
                UNIQUE(name, city, province)
            )
        """)
        
        # Runs table - tracks execution history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_timestamp TEXT NOT NULL,
                province TEXT NOT NULL,
                category TEXT NOT NULL,
                cities_processed INTEGER DEFAULT 0,
                businesses_discovered INTEGER DEFAULT 0,
                emails_sent INTEGER DEFAULT 0,
                errors INTEGER DEFAULT 0,
                status TEXT NOT NULL,
                error_log TEXT
            )
        """)
        
        # Create indices for faster queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_searches_province_category ON searches(province, category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_searches_status ON searches(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_businesses_province_category ON businesses(province, category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_businesses_email_sent ON businesses(email_sent)")
        
        conn.commit()
        conn.close()
    
    def create_run(self, province: str, category: str) -> int:
        """Create a new run record and return its ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO runs (run_timestamp, province, category, status)
            VALUES (?, ?, ?, 'running')
        """, (timestamp, province, category))
        
        run_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return run_id
    
    def update_run(self, run_id: int, cities_processed: int = 0, 
                   businesses_discovered: int = 0, emails_sent: int = 0, 
                   errors: int = 0, status: str = 'running', error_log: str = None):
        """Update run statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE runs
            SET cities_processed = cities_processed + ?,
                businesses_discovered = businesses_discovered + ?,
                emails_sent = emails_sent + ?,
                errors = errors + ?,
                status = ?,
                error_log = ?
            WHERE id = ?
        """, (cities_processed, businesses_discovered, emails_sent, errors, status, error_log, run_id))
        
        conn.commit()
        conn.close()
    
    def add_search(self, province: str, city: str, category: str, 
                   latitude: float, longitude: float, radius: int) -> int:
        """Add or get a search record."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        try:
            cursor.execute("""
                INSERT INTO searches (province, city, category, latitude, longitude, radius, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (province, city, category, latitude, longitude, radius, timestamp))
            search_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Record already exists, get its ID
            cursor.execute("""
                SELECT id FROM searches
                WHERE province = ? AND city = ? AND category = ? 
                AND latitude = ? AND longitude = ? AND radius = ?
            """, (province, city, category, latitude, longitude, radius))
            search_id = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        return search_id
    
    def update_search(self, search_id: int, status: str, businesses_found: int):
        """Update search status and results."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        cursor.execute("""
            UPDATE searches
            SET status = ?, businesses_found = ?, last_run_timestamp = ?
            WHERE id = ?
        """, (status, businesses_found, timestamp, search_id))
        
        conn.commit()
        conn.close()
    
    def get_next_search(self, province: str, category: str) -> Optional[Dict]:
        """Get the next uncompleted search location."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM searches
            WHERE province = ? AND category = ? AND status != 'complete'
            ORDER BY last_run_timestamp ASC NULLS FIRST, created_at ASC
            LIMIT 1
        """, (province, category))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def add_business(self, name: str, city: str, province: str, category: str,
                     website: str = None, email: str = None, address: str = None,
                     phone: str = None, latitude: float = None, longitude: float = None,
                     site_analysis: str = None) -> Optional[int]:
        """Add a new business or return existing ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        try:
            cursor.execute("""
                INSERT INTO businesses (name, city, province, category, website, email, 
                                       address, phone, latitude, longitude, site_analysis, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, city, province, category, website, email, address, phone, 
                  latitude, longitude, site_analysis, timestamp))
            business_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return business_id
        except sqlite3.IntegrityError:
            # Business already exists
            conn.close()
            return None
    
    def mark_email_sent(self, business_id: int):
        """Mark a business as having received an email."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        cursor.execute("""
            UPDATE businesses
            SET email_sent = 1, email_sent_timestamp = ?
            WHERE id = ?
        """, (timestamp, business_id))
        
        conn.commit()
        conn.close()
    
    def get_unemailed_businesses(self, province: str, category: str, limit: int = 100) -> List[Dict]:
        """Get businesses that haven't been emailed yet."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM businesses
            WHERE province = ? AND category = ? AND email_sent = 0 AND email IS NOT NULL
            ORDER BY created_at ASC
            LIMIT ?
        """, (province, category, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_province_status(self, province: str, category: str) -> Dict:
        """Get overall status for a province and category."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count searches by status
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM searches
            WHERE province = ? AND category = ?
            GROUP BY status
        """, (province, category))
        
        status_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Count businesses
        cursor.execute("""
            SELECT COUNT(*) as total, 
                   SUM(CASE WHEN email_sent = 1 THEN 1 ELSE 0 END) as emailed,
                   SUM(CASE WHEN email IS NOT NULL THEN 1 ELSE 0 END) as has_email
            FROM businesses
            WHERE province = ? AND category = ?
        """, (province, category))
        
        business_row = cursor.fetchone()
        
        conn.close()
        
        return {
            'searches': status_counts,
            'total_businesses': business_row[0] or 0,
            'businesses_emailed': business_row[1] or 0,
            'businesses_with_email': business_row[2] or 0
        }
    
    def is_province_complete(self, province: str, category: str) -> bool:
        """Check if all cities in a province are complete."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM searches
            WHERE province = ? AND category = ? AND status != 'complete'
        """, (province, category))
        
        incomplete_count = cursor.fetchone()[0]
        conn.close()
        
        return incomplete_count == 0
    
    def reset_province(self, province: str, category: str):
        """Reset all data for a province and category."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM searches WHERE province = ? AND category = ?", (province, category))
        cursor.execute("DELETE FROM businesses WHERE province = ? AND category = ?", (province, category))
        
        conn.commit()
        conn.close()
    
    def get_city_stats(self, province: str, city: str, category: str) -> Dict:
        """Get statistics for a specific city."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) as total, 
                   SUM(CASE WHEN status = 'complete' THEN 1 ELSE 0 END) as complete
            FROM searches
            WHERE province = ? AND city = ? AND category = ?
        """, (province, city, category))
        
        search_row = cursor.fetchone()
        
        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN email_sent = 1 THEN 1 ELSE 0 END) as emailed
            FROM businesses
            WHERE province = ? AND city = ? AND category = ?
        """, (province, city, category))
        
        business_row = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_searches': search_row[0] or 0,
            'complete_searches': search_row[1] or 0,
            'total_businesses': business_row[0] or 0,
            'emailed_businesses': business_row[1] or 0
        }
