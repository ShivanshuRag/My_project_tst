import numpy as np
import pandas as pd

# 1. Sample DataFrame
data = {
    "company_name": [
        "Alpha Tech",
        "Beta Solutions",
        "Gamma Global",
        "Delta Retail",
        "Omega Corp",
        "Null Co",
    ],
    "employee_count": [45, 250, 1500, 12, 850, np.nan],
}

df = pd.DataFrame(data)


# 2. Tier decide karne ke liye custom function
def assign_market_tier(count):
    # Null ya missing values check
    if pd.isna(count) or count <= 0:
        return "Unknown"
    elif count < 100:
        return "SMB"
    elif count < 1000:
        return "Mid-Market"
    else:
        return "Enterprise"


# 3. .apply() ke through naya column create karein
df["market_tier"] = df["employee_count"].apply(assign_market_tier)

# 4. Result display
print(df)