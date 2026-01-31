import pandas as pd
import matplotlib.pyplot as plt

# Load the final dataset
file_path = r'c:\Users\Pratham\OneDrive\Desktop\scratch\Innomatics\final_food_delivery_dataset.csv'
df = pd.read_csv(file_path)

# Convert order_date to datetime
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True)

# 1. Order Trends Over Time (Monthly Revenue)
monthly_revenue = df.groupby(df['order_date'].dt.to_period('M'))['total_amount'].sum()

# 2. City-wise Performance
city_performance = df.groupby('city')['total_amount'].sum().sort_values(ascending=False)

# 3. Cuisine-wise Performance
cuisine_performance = df.groupby('cuisine')['total_amount'].sum().sort_values(ascending=False)

# 4. Membership Impact
membership_stats = df.groupby('membership').agg({
    'total_amount': ['sum', 'mean', 'count']
})

# 5. Peak Seasonality (Day of Week)
df['day_of_week'] = df['order_date'].dt.day_name()
day_of_week_performance = df.groupby('day_of_week')['total_amount'].count().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
])

print("--- Data Insights Summary ---")
print("\n1. Top 3 Performing Cities (Revenue):")
print(city_performance.head(3))

print("\n2. Top 3 Popular Cuisines (Revenue):")
print(cuisine_performance.head(3))

print("\n3. Membership Impact (Average Order Value):")
print(membership_stats['total_amount']['mean'])

print("\n4. Total Orders by Membership:")
print(membership_stats['total_amount']['count'])

print("\n5. Weekend vs Weekday Orders (Sample Check):")
print(day_of_week_performance)
