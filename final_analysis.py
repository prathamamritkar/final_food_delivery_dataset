import pandas as pd
import numpy as np

# Load the dataset
file_path = r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\final_food_delivery_dataset.csv'
df = pd.read_csv(file_path)

# Convert order_date to datetime
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True)

# Q1: Which city has the highest total revenue (total_amount) from Gold members?
gold_members = df[df['membership'] == 'Gold']
q1_result = gold_members.groupby('city')['total_amount'].sum().idxmax()
q1_value = gold_members.groupby('city')['total_amount'].sum().max()

# Q2: Which cuisine has the highest average order value across all orders?
q2_result = df.groupby('cuisine')['total_amount'].mean().idxmax()
q2_value = df.groupby('cuisine')['total_amount'].mean().max()

# Q3: How many distinct users placed orders worth more than ₹1000 in total (sum of all their orders)?
user_totals = df.groupby('user_id')['total_amount'].sum()
q3_result = (user_totals > 1000).sum()

# Q4: Which restaurant rating range generated the highest total revenue?
bins = [3.0, 3.55, 4.05, 4.55, 5.05]
labels = ['3.0 – 3.5', '3.6 – 4.0', '4.1 – 4.5', '4.6 – 5.0']
df['rating_range'] = pd.cut(df['rating'], bins=bins, labels=labels, include_lowest=True)
q4_result = df.groupby('rating_range', observed=True)['total_amount'].sum().idxmax()
q4_value = df.groupby('rating_range', observed=True)['total_amount'].sum().max()

# Q5: Among Gold members, which city has the highest average order value?
q5_result = gold_members.groupby('city')['total_amount'].mean().idxmax()
q5_value = gold_members.groupby('city')['total_amount'].mean().max()

# Q6: Which cuisine has the lowest number of distinct restaurants but still contributes significant revenue?
cuisine_stats = df.groupby('cuisine').agg({
    'restaurant_id': 'nunique',
    'total_amount': 'sum'
}).rename(columns={'restaurant_id': 'distinct_restaurants', 'total_amount': 'total_revenue'})
q6_result = cuisine_stats['distinct_restaurants'].idxmin()

# Q7: What percentage of total orders were placed by Gold members?
gold_orders = len(gold_members)
total_orders = len(df)
q7_result = round((gold_orders / total_orders) * 100)

# Q8: Which restaurant has the highest average order value but less than 20 total orders?
rest_stats = df.groupby('restaurant_name_master').agg({
    'total_amount': ['mean', 'count']
})
rest_stats.columns = ['aov', 'order_count']
filtered_rests = rest_stats[rest_stats['order_count'] < 20]
q8_result = filtered_rests['aov'].idxmax()
q8_value = filtered_rests['aov'].max()

# Q9: Which combination contributes the highest revenue? (City + Cuisine)
comb_revenue = df.groupby(['city', 'cuisine'])['total_amount'].sum()
q9_result = comb_revenue.idxmax()
q9_value = comb_revenue.max()

# Q10: During which quarter of the year is the total revenue highest?
df['quarter'] = df['order_date'].dt.to_period('Q')
q10_result = df.groupby('quarter')['total_amount'].sum().idxmax()
q10_value = df.groupby('quarter')['total_amount'].sum().max()

# Save results to a file
output_file = r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\analysis_results.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("--- Analysis Results ---\n\n")
    f.write(f"Q1: {q1_result} (₹{q1_value:,.2f})\n")
    f.write(f"Q2: {q2_result} (₹{q2_value:,.2f})\n")
    f.write(f"Q3: {q3_result}\n")
    f.write(f"Q4: {q4_result} (₹{q4_value:,.2f})\n")
    f.write(f"Q5: {q5_result} (₹{q5_value:,.2f})\n")
    f.write(f"Q6: {q6_result} (Dist. Rests: {cuisine_stats.loc[q6_result, 'distinct_restaurants']}, Revenue: ₹{cuisine_stats.loc[q6_result, 'total_revenue']:,.2f})\n")
    f.write(f"Q7: {q7_result}%\n")
    f.write(f"Q8: {q8_result} (₹{q8_value:,.2f})\n")
    f.write(f"Q9: {q9_result} (₹{q9_value:,.2f})\n")
    f.write(f"Q10: {q10_result} (₹{q10_value:,.2f})\n")

print(f"Analysis complete. Results saved to {output_file}")
