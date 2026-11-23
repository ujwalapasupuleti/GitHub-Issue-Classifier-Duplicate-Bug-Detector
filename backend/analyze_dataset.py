import pandas as pd

df = pd.read_csv("dataset/issues.csv")

print("DATASET INFORMATION")

print("\nTotal records:", len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nCategory distribution:")
print(df["category"].value_counts())

print("\nSample records:")
print(df[["title", "category"]].head(10))