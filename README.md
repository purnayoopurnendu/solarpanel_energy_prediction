# 🌞 Solar Energy Prediction using Machine Learning

## 📌 Project Overview
This project predicts solar panel energy output using weather data such as irradiance, temperature, humidity, and cloud cover.

---

## ⚙️ Technologies Used
- Python
- Pandas, NumPy
- Scikit-learn
- XGBoost
- Docker
- Power BI

---

## 📊 Model Performance

### 🌳 Random Forest
- MAE: ~0.00015  
- RMSE: ~0.00034  
- R² Score: ~0.99998  

### ⚡ XGBoost
- MAE: ~0.00018  
- RMSE: ~0.00033  
- R² Score: ~0.99998  

👉 Random Forest performed slightly better.

---

## 🔥 Key Insight
- Irradiance is the most important factor affecting solar energy generation.

---

## 🐳 Run using Docker

```bash
docker build -t solar-project .
docker run solar-project
