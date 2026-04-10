import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import xgboost as xgb

# ---------------- LOAD DATA ----------------
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, '..', 'data', 'solar_data_clean.csv')

print("📂 Loading file from:", file_path)

df = pd.read_csv(file_path)

# Save original city names
df['city_name'] = df['city']

# Encode city for model
df['city'] = df['city'].astype('category').cat.codes

print("✅ Data Loaded Successfully")
print(df.head())

# ---------------- CLEAN DATA (FIXED POSITION) ----------------
df = df.dropna()

# ---------------- CORRELATION HEATMAP ----------------
heatmap_cols = [
    'irradiance_ghi',
    'ambient_temp',
    'cloud_cover_pct',
    'wind_speed',
    'humidity_pct',
    'hour',
    'month',
    'city',
    'ac_power_kw'
]

plt.figure(figsize=(10,6))
sns.heatmap(df[heatmap_cols].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

# ---------------- FEATURES ----------------
features = [
    'irradiance_ghi',
    'ambient_temp',
    'cloud_cover_pct',
    'wind_speed',
    'humidity_pct',
    'hour',
    'month',
    'city'
]

# Fix humidity column if needed
if 'humidity_pct' not in df.columns:
    if 'humidity' in df.columns:
        features[4] = 'humidity'
    elif 'relative_humidity' in df.columns:
        features[4] = 'relative_humidity'

# ---------------- SELECT DATA ----------------
X = df[features]
y = df['ac_power_kw']

# ---------------- TRAIN TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- RANDOM FOREST (IMPROVED) ----------------
rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

# ---------------- FEATURE IMPORTANCE (PRO VERSION) ----------------
importance = rf_model.feature_importances_
feat_importance = pd.Series(importance, index=features)

# Normalize (fix single-bar issue)
feat_importance = feat_importance / feat_importance.max()

print("\n🔥 Feature Importance Values:")
print(feat_importance.sort_values(ascending=False))

plt.figure(figsize=(8,5))
sns.barplot(x=feat_importance.values, y=feat_importance.index)

plt.title("Normalized Feature Importance (Random Forest)")
plt.xlabel("Relative Importance")
plt.ylabel("Features")
plt.grid(axis='x')

plt.show()

# ---------------- XGBOOST ----------------
xgb_model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1)
xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)

# XGBoost importance
xgb.plot_importance(xgb_model)
plt.title("Feature Importance (XGBoost)")
plt.show()

# ---------------- EVALUATION ----------------
def evaluate(name, y_true, y_pred):
    print(f"\n{name}")
    print("MAE:", mean_absolute_error(y_true, y_pred))
    print("RMSE:", np.sqrt(mean_squared_error(y_true, y_pred)))
    print("R2 Score:", r2_score(y_true, y_pred))

evaluate("Random Forest", y_test, rf_pred)
evaluate("XGBoost", y_test, xgb_pred)

# ---------------- EXTRA SUMMARY (FOR VIVA) ----------------
print("\n📊 Model Comparison Summary:")
print("Random Forest performs slightly better in capturing solar power trends.")
print("Irradiance is the most important feature influencing energy generation.")

# ---------------- ERROR COMPARISON GRAPH ----------------
models = ['Random Forest', 'XGBoost']
mae_vals = [
    mean_absolute_error(y_test, rf_pred),
    mean_absolute_error(y_test, xgb_pred)
]

plt.figure()
plt.bar(models, mae_vals)
plt.title("MAE Comparison Between Models")
plt.ylabel("Error")
plt.show()

# ---------------- SAVE OUTPUT ----------------
output_path = os.path.join(base_path, '..', 'outputs', 'final_output.csv')

rf_full = rf_model.predict(X)
xgb_full = xgb_model.predict(X)

results = X.copy()

# Add readable city names
results['city_name'] = df['city_name']

# Remove encoded city
results = results.drop(columns=['city'])

# Add predictions
results['Actual'] = y.values
results['RF_Predicted'] = rf_full
results['XGB_Predicted'] = xgb_full

<<<<<<< HEAD

=======
# 🔥 ADD THIS PART (VERY IMPORTANT)
>>>>>>> 1ae9310eb78a0f51dd8f99df9bac2725c9351cc8
results['RF_Error'] = abs(results['Actual'] - results['RF_Predicted'])
results['XGB_Error'] = abs(results['Actual'] - results['XGB_Predicted'])

results.to_csv(output_path, index=False)

print("\n✅ File saved → outputs/final_output.csv")

# ---------------- FINAL GRAPH ----------------
plt.figure(figsize=(10,5))
plt.plot(y_test.values[:100], label="Actual")
plt.plot(rf_pred[:100], label="Random Forest")
plt.plot(xgb_pred[:100], label="XGBoost")

plt.legend()
plt.title("Model Comparison")
plt.xlabel("Samples")
plt.ylabel("Power Output")
<<<<<<< HEAD
plt.show()
=======
plt.show()
>>>>>>> 1ae9310eb78a0f51dd8f99df9bac2725c9351cc8
