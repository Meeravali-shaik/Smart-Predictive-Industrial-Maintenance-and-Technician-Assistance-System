"""Scikit-learn training pipeline for predictive maintenance (Phase 2)."""

import os
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

MODEL_DIR = Path(__file__).parent / "models"
MODEL_DIR.mkdir(exist_ok=True)


class MLPredictorPipeline:
    """Phase 2: ML training pipeline ready for future rule-based replacement."""

    FEATURE_COLUMNS = ["temperature", "vibration", "current", "humidity", "pressure", "rpm"]

    def __init__(self):
        self.scaler = StandardScaler()
        self.models = {
            "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "gradient_boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
            "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
        }
        self.trained_model = None
        self.model_name: str | None = None

    def generate_synthetic_training_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """Generate synthetic labeled data for initial model training."""
        rng = np.random.default_rng(42)
        data = {
            "temperature": rng.normal(55, 8, n_samples),
            "vibration": rng.normal(2.5, 1.0, n_samples),
            "current": rng.normal(10, 2, n_samples),
            "humidity": rng.normal(45, 10, n_samples),
            "pressure": rng.normal(100, 8, n_samples),
            "rpm": rng.normal(2400, 200, n_samples),
        }
        df = pd.DataFrame(data)

        # Label failures based on rules similar to rule-based engine
        df["failure"] = 0
        df.loc[(df["temperature"] > 85) | (df["vibration"] > 7), "failure"] = 1
        df.loc[(df["temperature"] > 90) & (df["vibration"] > 8), "failure"] = 1
        df.loc[df["current"] > 18, "failure"] = 1

        return df

    def train(self, df: pd.DataFrame | None = None, model_name: str = "random_forest") -> dict[str, Any]:
        if df is None:
            df = self.generate_synthetic_training_data()

        X = df[self.FEATURE_COLUMNS]
        y = df["failure"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        model = self.models[model_name]
        model.fit(X_train_scaled, y_train)
        predictions = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, predictions)

        self.trained_model = model
        self.model_name = model_name

        model_path = MODEL_DIR / f"{model_name}_model.joblib"
        scaler_path = MODEL_DIR / f"{model_name}_scaler.joblib"
        joblib.dump(model, model_path)
        joblib.dump(self.scaler, scaler_path)

        return {
            "model_name": model_name,
            "accuracy": round(accuracy, 4),
            "report": classification_report(y_test, predictions, output_dict=True),
            "model_path": str(model_path),
        }

    def load_model(self, model_name: str = "random_forest") -> bool:
        model_path = MODEL_DIR / f"{model_name}_model.joblib"
        scaler_path = MODEL_DIR / f"{model_name}_scaler.joblib"
        if not model_path.exists() or not scaler_path.exists():
            return False
        self.trained_model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.model_name = model_name
        return True

    def predict_failure_probability(self, reading: dict[str, float]) -> float:
        if self.trained_model is None:
            if not self.load_model():
                return 0.0

        features = np.array([[reading[col] for col in self.FEATURE_COLUMNS]])
        scaled = self.scaler.transform(features)
        if hasattr(self.trained_model, "predict_proba"):
            return float(self.trained_model.predict_proba(scaled)[0][1])
        return float(self.trained_model.predict(scaled)[0])
