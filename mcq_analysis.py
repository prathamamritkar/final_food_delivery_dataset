import pandas as pd

# Load the dataset
file_path = r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\final_food_delivery_dataset.csv'
df = pd.read_csv(file_path)

results = []

results.append("--- Question 1 Analysis ---")
target_restaurants = [
    'Grand Cafe Punjabi', 
    'Grand Restaurant South Indian', 
    'Ruchi Mess Multicuisine', 
    'Ruchi Foods Chinese'
]

# Filter for the target restaurants
q1_df = df[df['restaurant_name'].isin(target_restaurants)]
q1_stats = q1_df.groupby('restaurant_name').agg({
    'total_amount': ['mean', 'count']
})
q1_stats.columns = ['aov', 'order_count']
results.append("Statistics for all potential answers:")
results.append(q1_stats.to_string())

filtered_q1 = q1_stats[q1_stats['order_count'] < 20]
results.append("\nFiltered (< 20 orders):")
results.append(filtered_q1.sort_values(by='aov', ascending=False).to_string())


results.append("\n--- Question 2 Analysis ---")
q2_stats = df.groupby(['membership', 'cuisine'])['total_amount'].sum().reset_index()

target_combs = [
    ('Gold', 'Indian'),
    ('Gold', 'Italian'),
    ('Regular', 'Indian'),
    ('Regular', 'Chinese')
]

results.append("Revenue for target combinations:")
for membership, cuisine in target_combs:
    revenue_row = q2_stats[(q2_stats['membership'] == membership) & (q2_stats['cuisine'] == cuisine)]
    if not revenue_row.empty:
        revenue = revenue_row['total_amount'].values[0]
        results.append(f"{membership} + {cuisine}: INR {revenue:,.2f}")

highest_q2 = q2_stats.sort_values(by='total_amount', ascending=False).iloc[0]
results.append(f"\nOverall Highest Combination: {highest_q2['membership']} + {highest_q2['cuisine']} (INR {highest_q2['total_amount']:,.2f})")

# Write results to file
with open(r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\mcq_results.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(results))

print("Results saved to mcq_results.txt")
