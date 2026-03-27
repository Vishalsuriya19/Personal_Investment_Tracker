"""
Database connection module
"""
import mysql.connector
from mysql.connector import Error
import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))
from config import (
    DATABASE_HOST,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_NAME,
    DATABASE_PORT
)

class Database:
    """Database connection handler"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                database=DATABASE_NAME,
                port=DATABASE_PORT
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("✓ Database connected successfully")
            return True
        except Error as e:
            print(f"✗ Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("✓ Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Error executing query: {e}")
            return None
    
    def execute_insert(self, query, params=None):
        """Execute an INSERT/UPDATE/DELETE query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.conn.rollback()
            print(f"✗ Error executing insert: {e}")
            return None
    
    def execute_many(self, query, data):
        """Execute multiple INSERT queries"""
        try:
            self.cursor.executemany(query, data)
            self.conn.commit()
            return True
        except Error as e:
            self.conn.rollback()
            print(f"✗ Error executing batch insert: {e}")
            return False

# Create a singleton instance
db = Database()
