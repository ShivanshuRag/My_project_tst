import numpy as np
import pandas as pd

# Data setup
data = {
    "company_name": [
        "Alpha",
        "Beta",
        "Gamma",
        "Delta",
        "Omega",
        "Zeta",
        "Sigma",
    ],
    "employee_count": [45, 250, 1500, 12, 850, 3200, 110],
    "market_tier": [
        "SMB",
        "Mid-Market",
        "Enterprise",
        "SMB",
        "Mid-Market",
        "Enterprise",
        "Mid-Market",
    ],
}
df = pd.DataFrame(data)

# 1. Frequency count aur Percentage nikalna
# distribution = pd.DataFrame(
#     {
#         "company_count": df["market_tier"].value_counts(),
#         "percentage": (
#             df["market_tier"].value_counts(normalize=True) * 100
#         ).round(2),
#     }
# )

# print(distribution)

# =============================

# Har tier ke employee metrics aggregate karna
# tier_stats = (
#     df.groupby("market_tier")["employee_count"]
#     .agg(
#         company_count="count",
#         avg_employees="mean",
#         median_employees="median",
#         min_employees="min",
#         max_employees="max",
#         std_dev="std",
#     )
#     .reset_index()
# )

# # Overall share percentage column add karna
# tier_stats["share_percent"] = (
#     (tier_stats["company_count"] / len(df)) * 100
# ).round(2)

# print(tier_stats)


# --------------------------------------

stats_summary = df.groupby("market_tier")["employee_count"].describe()
print(stats_summary)
