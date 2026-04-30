import sqlite3
import pandas as pd
from datetime import datetime
import os
import streamlit as st

# ==========================================
# CLOUD DATABASE PREP (Configuration)
# ==========================================
# To switch from local SQLite to a Cloud Database (e.g., Supabase, Neon PostgreSQL):
# 1. Add sqlalchemy and psycopg2-binary to requirements.txt.
# 2. Add your connection string to Streamlit Cloud secrets (.streamlit/secrets.toml):
#    DATABASE_URL = "postgresql://user:password@host:port/dbname"
# 3. Uncomment and use the SQLAlchemy engine instead of sqlite3.
# 
# Example Cloud Connection:
# from sqlalchemy import create_engine
# def get_cloud_engine():
#     try:
#         if "DATABASE_URL" in st.secrets:
#             return create_engine(st.secrets["DATABASE_URL"])
#     except Exception:
#         pass
#     return None
# 
# NOTE: If moving to PostgreSQL, remember to update query parameter bindings from '?' to '%s'.
# ==========================================

DB_NAME = "my_store.db"
# Ensure the db file is stored in the same directory as this file
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

def get_connection():
    # Currently uses local SQLite. 
    # To use cloud, swap this out with get_cloud_engine().connect()
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Create products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    # Create sales table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            sale_date TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_product(name, price, quantity):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_connection()
    df = pd.read_sql_query("SELECT id, name, price, quantity FROM products", conn)
    conn.close()
    return df

def get_product_by_id(product_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, price, quantity FROM products WHERE id=?", (product_id,))
    product = c.fetchone()
    conn.close()
    return product

def sell_product(product_id, quantity, total_price):
    conn = get_connection()
    c = conn.cursor()
    
    # Insert sale record
    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO sales (product_id, quantity, total_price, sale_date) VALUES (?, ?, ?, ?)",
              (product_id, quantity, total_price, sale_date))
              
    # Update inventory
    c.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))
    
    conn.commit()
    conn.close()

def get_sales_report():
    conn = get_connection()
    query = '''
        SELECT s.id, p.name as product_name, s.quantity, s.total_price, s.sale_date
        FROM sales s
        JOIN products p ON s.product_id = p.id
        ORDER BY s.sale_date DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
