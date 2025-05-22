import os
import streamlit as st
import psycopg2
from psycopg2 import pool

# Database configuration from Streamlit secrets
DB_CONFIG = {
    'host': st.secrets["postgres"]["host"],
    'database': st.secrets["postgres"]["database"],
    'user': st.secrets["postgres"]["user"],
    'password': st.secrets["postgres"]["password"],
    'port': st.secrets["postgres"]["port"]
}

# Create a connection pool
connection_pool = pool.SimpleConnectionPool(
    1,  # minconn
    10,  # maxconn
    **DB_CONFIG
)

def get_db_connection():
    return connection_pool.getconn()

def release_db_connection(conn):
    connection_pool.putconn(conn)

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Create users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id VARCHAR(50) PRIMARY KEY,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create summaries table with user_id foreign key
            cur.execute("""
                CREATE TABLE IF NOT EXISTS summaries (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(50) NOT NULL,
                    original_text TEXT NOT NULL,
                    casual_summary TEXT NOT NULL,
                    formal_summary TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        release_db_connection(conn)

def create_user(user_id):
    """Create a new user if they don't exist"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (user_id)
                VALUES (%s)
                ON CONFLICT (user_id) DO NOTHING
            """, (user_id,))
        conn.commit()
    except Exception as e:
        print(f"Error creating user: {e}")
        conn.rollback()
    finally:
        release_db_connection(conn) 