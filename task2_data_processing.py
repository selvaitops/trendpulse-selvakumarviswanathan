import pandas as pd
import csv
import os

filepath  = 'data/trends_20260407.json'
data_orig = pd.read_json(filepath)

df = data_orig.copy()

print(f"Loaded {len(df)} stories from {filepath}")

df = df.drop_duplicates(subset=['post_id'])
print("After removing duplicates:", len(df))

df = df.dropna(subset=['post_id', 'title', 'score'])
print("After removing null/missing values:", len(df))

df['score'] = df['score'].astype(int)
df['num_comments'] = df['num_comments'].fillna(0).astype(int)

df = df[df['score'] >=5 ]
print("After removing low scores:", len(df))

df['title'] = df['title'].str.strip()

output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print("Saved", len(df), "rows to", output_file)

print("Stories per category:")
print(df['category'].value_counts())