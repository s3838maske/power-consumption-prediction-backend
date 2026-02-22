"""
Machine Learning Model Training Script
Trains Linear Regression and Random Forest models for power consumption prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_regression import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
from datetime import datetime

class PowerConsumptionPredictor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.lr_model = LinearRegression()
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
    def load_data(self, filepath):
        """Load consumption data from CSV/Excel"""
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        return df
    
    def preprocess_data(self, df):
        """Preprocess and engineer features"""
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract time-based features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['day_of_month'] = df['date'].dt.day
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Handle missing values
        df = df.fillna(df.mean(numeric_only=True))
        
        # Create lag features (previous day consumption)
        df = df.sort_values('date')
        df['prev_day_consumption'] = df['consumption'].shift(1)
        df['prev_week_consumption'] = df['consumption'].shift(7)
        
        # Drop rows with NaN from lag features
        df = df.dropna()
        
        return df
    
    def prepare_features(self, df):
        """Prepare feature matrix and target variable"""
        feature_columns = [
            'day_of_week', 'month', 'day_of_month', 'is_weekend',
            'prev_day_consumption', 'prev_week_consumption'
        ]
        
        X = df[feature_columns]
        y = df['consumption']
        
        return X, y
    
    def train_models(self, X_train, y_train):
        """Train both Linear Regression and Random Forest models"""
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train Linear Regression
        print("Training Linear Regression model...")
        self.lr_model.fit(X_train_scaled, y_train)
        
        # Train Random Forest
        print("Training Random Forest model...")
        self.rf_model.fit(X_train_scaled, y_train)
        
        print("✓ Models trained successfully!")
    
    def evaluate_models(self, X_test, y_test):
        """Evaluate model performance"""
        X_test_scaled = self.scaler.transform(X_test)
        
        # Linear Regression predictions
        lr_predictions = self.lr_model.predict(X_test_scaled)
        lr_mse = mean_squared_error(y_test, lr_predictions)
        lr_rmse = np.sqrt(lr_mse)
        lr_mae = mean_absolute_error(y_test, lr_predictions)
        lr_r2 = r2_score(y_test, lr_predictions)
        
        # Random Forest predictions
        rf_predictions = self.rf_model.predict(X_test_scaled)
        rf_mse = mean_squared_error(y_test, rf_predictions)
        rf_rmse = np.sqrt(rf_mse)
        rf_mae = mean_absolute_error(y_test, rf_predictions)
        rf_r2 = r2_score(y_test, rf_predictions)
        
        print("\n" + "="*60)
        print("MODEL EVALUATION RESULTS")
        print("="*60)
        
        print("\nLinear Regression:")
        print(f"  RMSE: {lr_rmse:.2f} kWh")
        print(f"  MAE:  {lr_mae:.2f} kWh")
        print(f"  R²:   {lr_r2:.4f}")
        
        print("\nRandom Forest:")
        print(f"  RMSE: {rf_rmse:.2f} kWh")
        print(f"  MAE:  {rf_mae:.2f} kWh")
        print(f"  R²:   {rf_r2:.4f}")
        
        print("\n" + "="*60)
        
        return {
            'lr': {'rmse': lr_rmse, 'mae': lr_mae, 'r2': lr_r2},
            'rf': {'rmse': rf_rmse, 'mae': rf_mae, 'r2': rf_r2}
        }
    
    def save_models(self, output_dir='ml_models'):
        """Save trained models and scaler"""
        os.makedirs(output_dir, exist_ok=True)
        
        joblib.dump(self.scaler, os.path.join(output_dir, 'scaler.pkl'))
        joblib.dump(self.lr_model, os.path.join(output_dir, 'linear_regression_model.pkl'))
        joblib.dump(self.rf_model, os.path.join(output_dir, 'random_forest_model.pkl'))
        
        print(f"\n✓ Models saved to {output_dir}/")
    
    def predict(self, features, model_type='rf'):
        """Make predictions using trained model"""
        features_scaled = self.scaler.transform(features)
        
        if model_type == 'lr':
            return self.lr_model.predict(features_scaled)
        else:
            return self.rf_model.predict(features_scaled)


def main():
    """Main training pipeline"""
    print("="*60)
    print("POWER CONSUMPTION PREDICTION - MODEL TRAINING")
    print("="*60)
    
    # Initialize predictor
    predictor = PowerConsumptionPredictor()
    
    # Load data (replace with actual data path)
    # For demo, create sample data
    print("\nGenerating sample training data...")
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    sample_data = pd.DataFrame({
        'date': dates,
        'consumption': np.random.normal(50, 15, len(dates)) + \
                      np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 10  # Seasonal pattern
    })
    
    # Preprocess data
    print("Preprocessing data...")
    df = predictor.preprocess_data(sample_data)
    
    # Prepare features
    X, y = predictor.prepare_features(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train models
    predictor.train_models(X_train, y_train)
    
    # Evaluate models
    metrics = predictor.evaluate_models(X_test, y_test)
    
    # Save models
    predictor.save_models()
    
    print("\n✓ Training pipeline completed successfully!")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    main()
