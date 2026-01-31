import nbformat as nbf

nb = nbf.v4.new_notebook()

# Cells definition
cells = [
    nbf.v4.new_markdown_cell("# Food Delivery Data Integration & Analysis\n"
                             "This notebook performs the integration of three disparate data sources (CSV, JSON, and SQL) and conducts a series of analyses to answer business-critical questions."),
    
    nbf.v4.new_markdown_cell("## Step 1: Initial Set-up and Data Loading"),
    nbf.v4.new_code_cell("import pandas as pd\n"
                         "import json\n"
                         "import sqlite3\n"
                         "import os\n\n"
                         "# File paths\n"
                         "csv_path = 'orders.csv'\n"
                         "json_path = 'users.json'\n"
                         "sql_path = 'restaurants.sql'"),
    
    nbf.v4.new_markdown_cell("### Load CSV (Transactional Data)"),
    nbf.v4.new_code_cell("orders_df = pd.read_csv(csv_path)\n"
                         "print(f'Orders loaded: {len(orders_df)} rows')\n"
                         "orders_df.head()"),
    
    nbf.v4.new_markdown_cell("### Load JSON (User Master Data)"),
    nbf.v4.new_code_cell("users_df = pd.read_json(json_path)\n"
                         "print(f'Users loaded: {len(users_df)} rows')\n"
                         "users_df.head()"),
    
    nbf.v4.new_markdown_cell("### Load SQL (Restaurant Master Data)\n"
                             "We will parse the SQL script and load it into a temporary SQLite database to extract the data into a DataFrame."),
    nbf.v4.new_code_cell("with open(sql_path, 'r') as f:\n"
                         "    sql_script = f.read()\n\n"
                         "conn = sqlite3.connect(':memory:')\n"
                         "cursor = conn.cursor()\n"
                         "cursor.executescript(sql_script)\n"
                         "restaurants_df = pd.read_sql_query('SELECT * FROM restaurants', conn)\n"
                         "conn.close()\n"
                         "print(f'Restaurants loaded: {len(restaurants_df)} rows')\n"
                         "restaurants_df.head()"),
    
    nbf.v4.new_markdown_cell("## Step 2: Data Merging\n"
                             "We perform left joins using `orders` as the base table to ensure all transactional data is preserved."),
    nbf.v4.new_code_cell("# Join orders with users (Key: user_id)\n"
                         "merged_df = orders_df.merge(users_df, on='user_id', how='left')\n\n"
                         "# Join previous result with restaurants (Key: restaurant_id)\n"
                         "final_df = merged_df.merge(restaurants_df, on='restaurant_id', how='left', suffixes=('', '_master'))\n\n"
                         "# Save the final dataset\n"
                         "final_df.to_csv('final_food_delivery_dataset.csv', index=False)\n"
                         "print('Final dataset saved successfully.')\n"
                         "final_df.head()"),
    
    nbf.v4.new_markdown_cell("## Step 3: Analytical Queries"),
    
    nbf.v4.new_markdown_cell("### 1. City with highest revenue from Gold members"),
    nbf.v4.new_code_cell("gold_members = final_df[final_df['membership'] == 'Gold']\n"
                         "q1 = gold_members.groupby('city')['total_amount'].sum().idxmax()\n"
                         "print(f'Answer: {q1}')"),
    
    nbf.v4.new_markdown_cell("### 2. Cuisine with highest average order value"),
    nbf.v4.new_code_cell("q2 = final_df.groupby('cuisine')['total_amount'].mean().idxmax()\n"
                         "print(f'Answer: {q2}')"),
    
    nbf.v4.new_markdown_cell("### 3. Distinct users with total orders > INR 1000"),
    nbf.v4.new_code_cell("q3 = (final_df.groupby('user_id')['total_amount'].sum() > 1000).sum()\n"
                         "print(f'Answer: {q3}')"),
    
    nbf.v4.new_markdown_cell("### 4. Rating range with highest revenue"),
    nbf.v4.new_code_cell("bins = [3.0, 3.55, 4.05, 4.55, 5.05]\n"
                         "labels = ['3.0 – 3.5', '3.6 – 4.0', '4.1 – 4.5', '4.6 – 5.0']\n"
                         "final_df['rating_range'] = pd.cut(final_df['rating'], bins=bins, labels=labels, include_lowest=True)\n"
                         "q4 = final_df.groupby('rating_range', observed=True)['total_amount'].sum().idxmax()\n"
                         "print(f'Answer: {q4}')"),
    
    nbf.v4.new_markdown_cell("### 5. Combination contributing highest revenue (Membership + Cuisine)"),
    nbf.v4.new_code_cell("target_combs = [\n"
                         "    ('Gold', 'Indian'),\n"
                         "    ('Gold', 'Italian'),\n"
                         "    ('Regular', 'Indian'),\n"
                         "    ('Regular', 'Chinese')\n"
                         "]\n"
                         "q5_stats = final_df.groupby(['membership', 'cuisine'])['total_amount'].sum().reset_index()\n"
                         "q5_results = q5_stats[q5_stats.apply(lambda x: (x.membership, x.cuisine) in target_combs, axis=1)]\n"
                         "answer_q5 = q5_results.sort_values(by='total_amount', ascending=False).iloc[0]\n"
                         "print(f'Answer: {answer_q5.membership} + {answer_q5.cuisine}')"),
    
    nbf.v4.new_markdown_cell("### 6. Percentage of orders by Gold members"),
    nbf.v4.new_code_cell("q6 = round((len(gold_members) / len(final_df)) * 100)\n"
                         "print(f'Answer: {q6}%')"),
    
    nbf.v4.new_markdown_cell("### 7. Total revenue from Hyderabad (Rounded)"),
    nbf.v4.new_code_cell("q7 = round(final_df[final_df['city'] == 'Hyderabad']['total_amount'].sum())\n"
                         "print(f'Answer: INR {q7}')"),
    
    nbf.v4.new_markdown_cell("### 8. Quarter with highest total revenue"),
    nbf.v4.new_code_cell("final_df['order_date'] = pd.to_datetime(final_df['order_date'], dayfirst=True)\n"
                         "q8 = final_df.groupby(final_df['order_date'].dt.to_period('Q'))['total_amount'].sum().idxmax()\n"
                         "print(f'Answer: {q8}')")
]

nb['cells'] = cells

with open(r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\Food_Delivery_Analysis.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook generated successfully.")
