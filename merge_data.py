import pandas as pd
import json
import sqlite3
import os

# Define file paths
csv_path = r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\orders.csv'
json_path = r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\users.json'
sql_path = r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\restaurants.sql'

def load_csv(path):
    print(f"Loading CSV: {path}")
    return pd.read_csv(path)

def load_json(path):
    print(f"Loading JSON: {path}")
    return pd.read_json(path)

def load_sql(path):
    print(f"Loading SQL: {path}")
    # Read the SQL file
    with open(path, 'r') as f:
        sql_script = f.read()
    
    # Create an in-memory SQLite database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Execute the script (CREATE and INSERT statements)
    cursor.executescript(sql_script)
    
    # Read the table into a DataFrame
    df = pd.read_sql_query("SELECT * FROM restaurants", conn)
    conn.close()
    return df

def main():
    # Step 1: Load CSV Data
    orders_df = load_csv(csv_path)
    
    # Step 2: Load JSON Data
    users_df = load_json(json_path)
    
    # Step 3: Load SQL Data
    restaurants_df = load_sql(sql_path)
    
    # Step 4: Merge the Data
    # 1. Merge Orders with Users (Left Join)
    # orders.user_id -> users.user_id
    merged_df = orders_df.merge(users_df, on='user_id', how='left')
    
    # 2. Merge with Restaurants (Left Join)
    # orders.restaurant_id -> restaurants.restaurant_id
    # We use suffixes to handle duplicate restaurant_name columns if they exist
    merged_df = merged_df.merge(restaurants_df, on='restaurant_id', how='left', suffixes=('', '_master'))
    
    # Save the final dataset
    output_path = r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\final_food_delivery_dataset.csv'
    merged_df.to_csv(output_path, index=False)
    
    print(f"\nFinal dataset created successfully!")
    print(f"Total rows: {len(merged_df)}")
    print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()
