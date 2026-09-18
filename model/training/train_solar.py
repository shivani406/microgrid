import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.model_selection import train_test_split
from model.training.data_pipeline import generate_synthetic_solar_data, prepare_features

def train_solar_model():
    data_path = os.path.join("model", "datasets", "synthetic_seed.csv")
    if not os.path.exists(data_path):
        df = generate_synthetic_solar_data()
    else:
        import pandas as pd
        df = pd.read_csv(data_path)
    x, y = prepare_features(df, model_type="solar")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = root_mean_squared_error(y_test, preds)
    print(f"Solar Model Trained | MAE: {mae:.2f} kW | RMSE: {rmse:.2f} kW")
    artifacts_dir = os.path.join("model", "saved_models")
    os.makedirs(artifacts_dir, exist_ok=True)
    joblib.dump(model, os.path.join(artifacts_dir, "solar_model.pkl"))

if __name__ == "__main__":
    train_solar_model()