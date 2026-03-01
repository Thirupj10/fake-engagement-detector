# Fake Engagement Detection System
## Model Explanation Document
**Behavioural Analytics Hackathon — Problem Statement 3**
**Author: Thiruchelvan P J**

---

## 1. Problem Understanding

Social media platforms face a growing challenge of fake engagement generated 
by bots and coordinated inauthentic accounts. This fake activity distorts 
genuine behavioural patterns, misleads advertisers, and manipulates content 
algorithms.

The goal of this project is to build a behavioural analytics system that:
- Differentiates organic users from bots
- Assigns an Authenticity Score (0-100) to each account
- Identifies key behavioural triggers behind the prediction
- Provides a visual dashboard for analysis

---

## 2. Dataset Description & Assumptions

**Dataset Type:** Synthetic  
**Total Records:** 1000 users (300 bots, 700 organic)  
**Reason for Synthetic Data:** No real labeled dataset was available with 
the required behavioural features at the granularity needed.

**How it was generated:**
- Bot accounts were simulated with high posting frequency, regular timing, 
  short comments, and high night activity — patterns consistent with 
  automated behaviour research
- Organic accounts were simulated with irregular posting times, longer 
  comments, varied language, and normal activity hours
- NumPy random distributions were used with a fixed seed (42) for 
  reproducibility

**Key Assumptions:**
- Bots post 50-200 times per day vs humans 1-10 times
- Bots have very regular posting times (low std deviation)
- Bots use repetitive language (low unique words ratio)
- Bots are more active at night (0.6-1.0 night activity ratio)
- Organic users have older, more complete accounts

---

## 3. Feature Engineering

| Feature | Type | Behavioural Insight |
|---------|------|-------------------|
| avg_posts_per_day | Continuous | Bots post significantly more than humans |
| posting_time_std | Continuous | Bots post at very regular intervals |
| engagement_burst_score | Continuous | Bots create sudden spikes in engagement |
| followers_following_ratio | Continuous | Bots follow many but have few followers |
| avg_comment_length | Continuous | Bot comments are short and repetitive |
| unique_words_ratio | Continuous | Bots reuse the same phrases repeatedly |
| account_age_days | Integer | Bot accounts are typically newer |
| profile_completeness | Continuous | Bots have incomplete profiles |
| night_activity_ratio | Continuous | Bots are active at unusual hours |

All features were scaled using StandardScaler before model training to 
ensure equal contribution from each feature.

---

## 4. Model Selection & Reasoning

**Algorithm:** Random Forest Classifier

**Why Random Forest?**
- Handles non-linear relationships between behavioural features well
- Provides feature importance scores for explainability
- Robust to outliers in behavioural data
- Works well with mixed feature types
- Easy to interpret for stakeholders

**Hyperparameters:**
- n_estimators: 100 trees
- max_depth: 10
- random_state: 42

**Train/Test Split:** 80% training, 20% testing with stratification to 
maintain class balance.

---

## 5. Evaluation Metrics

| Metric | Organic | Bot | Overall |
|--------|---------|-----|---------|
| Precision | 1.00 | 1.00 | 1.00 |
| Recall | 1.00 | 1.00 | 1.00 |
| F1-Score | 1.00 | 1.00 | 1.00 |
| ROC-AUC | - | - | 1.00 |
| Accuracy | - | - | 100% |

**Note:** Perfect scores are expected because the synthetic dataset was 
generated with clearly separated behavioural distributions for bots and 
organic users. In a real-world scenario with noisy, overlapping data, 
scores would typically range between 0.85-0.95.

---

## 6. Behavioural Insights Derived

**Top Behavioural Triggers (by Feature Importance):**

1. **engagement_burst_score** — The most powerful indicator. Bots create 
   sudden, unnatural spikes in engagement that organic users never exhibit.

2. **night_activity_ratio** — Bots operate around the clock without human 
   sleep patterns, making night activity a strong signal.

3. **avg_posts_per_day** — The volume of posts is dramatically higher for 
   bots, often 10-20x more than organic users.

4. **unique_words_ratio** — Bots reuse templated language, resulting in 
   very low linguistic diversity.

5. **account_age_days** — Newly created accounts are far more likely to 
   be bots, as organic accounts accumulate history over time.

**Output Labels:**
- **Bot** (bot_probability > 0.7) — High confidence automated account
- **Suspicious** (bot_probability 0.4-0.7) — Requires further review
- **Organic** (bot_probability < 0.4) — Likely genuine human account

---

## 7. System Output

Each user account receives:
- **Authenticity Score** (0-100): Higher = more likely organic
- **Bot Probability** (0-1): Confidence of being a bot
- **Risk Label**: Bot / Suspicious / Organic
- **Visual Dashboard**: Interactive Plotly Dash interface showing 
  distribution, feature importance, and filtering by risk label

