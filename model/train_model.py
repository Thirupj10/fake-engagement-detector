import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
import pickle
import json

# Load dataset
df = pd.read_csv('data/synthetic_engagement_data.csv')

# Features and label
X = df.drop(columns=['user_id', 'label'])
y = df['label']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Train Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("=== Model Evaluation ===")
print(classification_report(y_test, y_pred, target_names=['Organic', 'Bot']))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")

# Feature importance
features = X.columns.tolist()
importances = model.feature_importances_
feature_importance_dict = dict(zip(features, importances.tolist()))
sorted_features = dict(sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True))

print("\n=== Feature Importances ===")
for feat, imp in sorted_features.items():
    print(f"{feat}: {imp:.4f}")

# Add scores to full dataset
df['bot_probability'] = model.predict_proba(scaler.transform(X_scaled))[:, 1]
df['authenticity_score'] = (1 - df['bot_probability']) * 100
df['risk_label'] = df['bot_probability'].apply(
    lambda x: 'Bot' if x > 0.7 else ('Suspicious' if x > 0.4 else 'Organic')
)

# Save results
df.to_csv('data/results.csv', index=False)

# Save model and scaler
pickle.dump(model, open('model/model.pkl', 'wb'))
pickle.dump(scaler, open('model/scaler.pkl', 'wb'))

# Save feature importances
with open('model/feature_importance.json', 'w') as f:
    json.dump(sorted_features, f, indent=4)

print("\n=== Files Saved ===")
print("✓ data/results.csv")
print("✓ model/model.pkl")
print("✓ model/scaler.pkl")
print("✓ model/feature_importance.json")
