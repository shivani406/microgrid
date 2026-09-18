import os
import pandas as pd

solar_path = os.path.join("model", "datasets", "solar_training_data.csv")
load_path = os.path.join("model", "datasets", "load_training_data.csv")

solar_df = pd.read_csv(solar_path)
load_df = pd.read_csv(load_path)

def verify_df(name, df, target_col):
    print(f"=== VERIFYING {name} ===")
    print(f"Total Rows: {len(df)}")
    
    null_counts = df.isnull().sum().sum()
    print(f"Total Null/NaN Values: {null_counts}")
    
    corr = df.corr(numeric_only=True)[target_col].sort_values(ascending=False)
    print(f"\nFeature Correlations with Target ({target_col}):")
    print(corr)
    print("\n" + "="*30 + "\n")

verify_df("Solar Dataset", solar_df, "solar_generation_kw")
verify_df("Load Dataset", load_df, "load_demand_kw")