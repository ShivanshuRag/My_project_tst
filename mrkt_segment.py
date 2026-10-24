import numpy as np
import pandas as pd

# 1. Sample Data create karte hain (Aap pd.read_csv('your_file.csv') use kar sakte hain)
data = {
    "company_name": [
        "Alpha Tech",
        "Beta Solutions",
        "Gamma Global",
        "Delta Retail",
        "Omega Corp",
        "Appwrite",
        "depso"
    ],
    "employee_count": [45, 250, 1500, 12, 850,140,230],
}

df = pd.DataFrame(data)

# 2. Conditions define karein
conditions = [
    (df["employee_count"] > 0) & (df["employee_count"] < 100),
    (df["employee_count"] >= 100) & (df["employee_count"] < 1000),
    (df["employee_count"] >= 1000),
]

# 3. Corresponding Tiers (Labels) define karein
tiers = ["SMB", "Mid-Market", "Enterprise"]

# 4. Market Tier assign karein (np.select handles multiple conditions efficiently)
df["market_tier"] = np.select(conditions, tiers, default="Unknown")

# 5. Output check karein
print(df)

# Output ko new CSV me save karne ke liye:
# df.to_csv('segmented_companies.csv', index=False)