import pandas as pd

# Load the dataset
file_path = r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\final_food_delivery_dataset.csv'
df = pd.read_csv(file_path)

results = []

# 1. How many total orders were placed by users with Gold membership?
gold_orders_count = len(df[df['membership'] == 'Gold'])
results.append(f"Q1: Total orders by Gold members: {gold_orders_count}")

# 2. What is the total revenue (rounded to nearest integer) generated from orders placed in Hyderabad city?
hyd_revenue = round(df[df['city'] == 'Hyderabad']['total_amount'].sum())
results.append(f"Q2: Total revenue in Hyderabad: {hyd_revenue}")

# 3. How many distinct users placed at least one order?
distinct_users = df['user_id'].nunique()
results.append(f"Q3: Distinct users who ordered: {distinct_users}")

# 4. What is the average order value (rounded to 2 decimals) for Gold members?
gold_aov = round(df[df['membership'] == 'Gold']['total_amount'].mean(), 2)
results.append(f"Q4: Average order value for Gold members: {gold_aov}")

# 5. How many orders were placed for restaurants with rating >= 4.5?
high_rated_orders = len(df[df['rating'] >= 4.5])
results.append(f"Q5: Orders for restaurants with rating >= 4.5: {high_rated_orders}")

# 6. How many orders were placed in the top revenue city among Gold members only?
# Step A: Find the top city for Gold members by revenue
gold_members = df[df['membership'] == 'Gold']
top_gold_city = gold_members.groupby('city')['total_amount'].sum().idxmax()
# Step B: Count orders in that specific city among Gold members
top_city_gold_orders = len(gold_members[gold_members['city'] == top_gold_city])
results.append(f"Q6: Orders in the top gold-revenue city ({top_gold_city}): {top_city_gold_orders}")

# Output results
for res in results:
    print(res)

# Save to file for verification
with open(r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\numerical_results.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(results))
