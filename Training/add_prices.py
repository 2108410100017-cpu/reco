import os
import pandas as pd
import random

# Path to your metadata file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
META_PATH = os.path.join(BASE_DIR, "metadata.csv")

# Load the metadata
df = pd.read_csv(META_PATH)

# Define price ranges based on product categories (if you have category information)
# If not, we'll use a general pricing strategy
def assign_price(row):
    # If you have category information, you can use different price ranges
    # For now, we'll use a general strategy with some randomness
    
    # Base price range (you can adjust these values)
    min_price = 10.99
    max_price = 199.99
    
    # You can add more sophisticated pricing logic based on product attributes
    # For example, if you have a 'category' column:
    # if row['category'] == 'luxury':
    #     return round(random.uniform(100.0, 500.0), 2)
    # elif row['category'] == 'accessories':
    #     return round(random.uniform(10.0, 50.0), 2)
    
    # Random price within the range
    return round(random.uniform(min_price, max_price), 2)

# Add price column
df['price'] = df.apply(assign_price, axis=1)

# Save the updated metadata
df.to_csv(META_PATH, index=False)

print(f"Added prices to {len(df)} products")
print("Sample of updated metadata:")
print(df.head())