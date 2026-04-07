import pandas as pd
import numpy as np
import csv

filepath = 'data/trends_clean.csv'
data = pd.read_csv(filepath)

df = data.copy()


print(f"Loaded data: {np.shape(df)}")
print("First 5 rows:")
print(df.head())

avg_score = df['score'].mean()
avg_comments = df['num_comments'].mean()

print("Average score   :", int(avg_score))
print("Average comments:", int(avg_comments))


print("--- NumPy Stats ---")

scores = df['score'].values

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

max_score = np.max(scores)
min_score = np.min(scores)

print("Mean score   :", int(mean_score))
print("Median score :", int(median_score))
print("Std deviation:", int(std_score))
print("Max score    :", int(max_score))
print("Min score    :", int(min_score))


category_counts = df['category'].value_counts()

top_category = category_counts.idxmax()

top_category_count = category_counts.max()

print("Most stories in:", top_category, "(", top_category_count, "stories )")

max_comments = df['num_comments'].max()

top_story = df[df['num_comments'] == max_comments].iloc[0]

print("Most commented story:")
print("\"" + top_story['title'] + "\" -", top_story['num_comments'], "comments")

df['engagement'] = df['num_comments'] / (df['score'] + 1)

df['is_popular'] = df['score'] > avg_score

output_path = "data/trends_analysed.csv"

df.to_csv(output_path, index=False)

print("Saved to", output_path)