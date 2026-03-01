import pandas as pd
import numpy as np

np.random.seed(42)

NUM_USERS = 1000
BOT_RATIO = 0.3

num_bots = int(NUM_USERS * BOT_RATIO)
num_organic = NUM_USERS - num_bots

def generate_bots(n):
    return pd.DataFrame({
        'user_id': [f'BOT_{i}' for i in range(n)],
        'avg_posts_per_day': np.random.uniform(50, 200, n),
        'posting_time_std': np.random.uniform(0.1, 2.0, n),
        'engagement_burst_score': np.random.uniform(0.7, 1.0, n),
        'followers_following_ratio': np.random.uniform(0.01, 0.3, n),
        'avg_comment_length': np.random.uniform(1, 10, n),
        'unique_words_ratio': np.random.uniform(0.05, 0.2, n),
        'account_age_days': np.random.randint(1, 180, n),
        'profile_completeness': np.random.uniform(0.1, 0.5, n),
        'night_activity_ratio': np.random.uniform(0.6, 1.0, n),
        'label': 1
    })

def generate_organic(n):
    return pd.DataFrame({
        'user_id': [f'USER_{i}' for i in range(n)],
        'avg_posts_per_day': np.random.uniform(1, 10, n),
        'posting_time_std': np.random.uniform(3.0, 8.0, n),
        'engagement_burst_score': np.random.uniform(0.0, 0.4, n),
        'followers_following_ratio': np.random.uniform(0.5, 5.0, n),
        'avg_comment_length': np.random.uniform(10, 60, n),
        'unique_words_ratio': np.random.uniform(0.5, 1.0, n),
        'account_age_days': np.random.randint(180, 3000, n),
        'profile_completeness': np.random.uniform(0.6, 1.0, n),
        'night_activity_ratio': np.random.uniform(0.0, 0.3, n),
        'label': 0
    })

bots = generate_bots(num_bots)
organic = generate_organic(num_organic)
df = pd.concat([bots, organic], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv('data/synthetic_engagement_data.csv', index=False)

print(f"Dataset generated successfully!")
print(f"Total users: {len(df)}")
print(f"Bots: {len(df[df['label'] == 1])}")
print(f"Organic: {len(df[df['label'] == 0])}")
print(df.head())
