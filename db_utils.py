import mysql.connector
import pandas as pd

# Database connection function
def get_db_connection():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "prijags20",
        "database": "expense_tracker_db"
    }
    return mysql.connector.connect(**db_config)

# Function to run SQL queries
def run_query(query):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    df = pd.DataFrame(results) if results else pd.DataFrame()
    cursor.close()
    conn.close()
    return df