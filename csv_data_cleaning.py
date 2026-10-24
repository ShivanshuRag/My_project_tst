import pandas as pd
import re

# Step 1: Messy CSV ko Pandas DataFrame me load karein
# na_values parameters se common placeholder values ko bhi NaN treat kiya jata hai
df = pd.read_csv("postman_loadtest_20_leads.csv", skipinitialspace=True)

# Step 2: Sabhi string columns se leading aur trailing whitespace strip karein
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

# Step 3: Email column ko clean aur validate karein
if "work_email" in df.columns:
    # 3a. Lowercase banayein aur spaces hatayein
    df["work_email"] = df["work_email"].astype(str).str.strip().str.lower()
    
    # 3b. Standard email regex pattern
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    
    # 3c. Jo emails format match na karein, unhe NaN mark karein
    df.loc[~df["work_email"].str.match(email_regex, na=False), "work_email"] = pd.NA

# Step 4: Null values wali rows ko drop karein
# Agar kisi bhi cell me missing value ho to poori row drop hogi:
df_cleaned = df.dropna().reset_index(drop=True)

# Agar sirf specific critical columns (jaise 'email', 'name') ke null hone par drop karna ho:
# df_cleaned = df.dropna(subset=['email', 'name']).reset_index(drop=True)

# Step 5: Cleaned data ko nayi CSV file me save karein
df_cleaned.to_csv("cleaned_leads.csv", index=False)

print(f"Original shape: {df.shape}")
print(f"Cleaned shape: {df_cleaned.shape}")