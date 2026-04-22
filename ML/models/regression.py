from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class RegressionModels:
    def __init__(self):
        self.models = {
            'Linear Regression': LinearRegression(),
            'SVR': SVR(),
            'Decision Tree': DecisionTreeRegressor(),
            'Random Forest': RandomForestRegressor(n_estimators=100),
            'Gradient Boosting': GradientBoostingRegressor(),
            'AdaBoost': AdaBoostRegressor(),
            'K-Nearest Neighbors': KNeighborsRegressor(),
            'XGBoost': XGBRegressor(),
            'LightGBM': LGBMRegressor(),
            'CatBoost': CatBoostRegressor(verbose=0)
        }
        self.results = {}

    def get_model_list(self):
        return list(self.models.keys())

    def train_and_eval(self, X_train, X_test, y_train, y_test, selected_model=None):
        if selected_model == 'auto':
            selected_model = None
            
        target_models = {selected_model: self.models[selected_model]} if selected_model else self.models
        
        for name, model in target_models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            
            self.results[name] = {
                'MSE': mse,
                'MAE': mae,
                'RMSE': rmse,
                'R2 Score': r2
            }
        return self.results

    def get_best_model(self):
        # Best model based on highest R2 Score
        best_name = max(self.results, key=lambda x: self.results[x]['R2 Score'])
        return best_name, self.results[best_name]

    def generate_visualizations(self, model_name, X_test, y_test, save_path, trained_model=None):
        """Generates performance plots for the chosen model with Digital Nebula theme."""
        model = trained_model if trained_model else self.models[model_name]
        y_pred = model.predict(X_test)
        
        # Consistent Styling
        plt.style.use('dark_background')
        plt.rcParams['figure.facecolor'] = '#050a14'
        plt.rcParams['axes.facecolor'] = '#050a14'
        plt.rcParams['text.color'] = '#c3f5ff'
        plt.rcParams['axes.labelcolor'] = '#c3f5ff'
        plt.rcParams['xtick.color'] = '#c3f5ff'
        plt.rcParams['ytick.color'] = '#c3f5ff'

        # 1. Prediction vs Actual Plot
        plt.figure(figsize=(10, 8))
        plt.scatter(y_test, y_pred, color='#00e5ff', alpha=0.6, edgecolors='none', s=50)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='#ff00cc', lw=2, linestyle='--')
        plt.xlabel('Actual Values', fontsize=12)
        plt.ylabel('Predicted Values', fontsize=12)
        plt.title(f'Regression Analysis: {model_name}', fontsize=16, weight='bold', color="#00e5ff", pad=20)
        plt.grid(alpha=0.1)
        plt.tight_layout()
        plt.savefig(os.path.join(save_path, 'model_actual_vs_predicted.png'), dpi=200, facecolor='#050a14')
        plt.close()

        # 2. Residuals Plot
        plt.figure(figsize=(10, 8))
        residuals = y_test - y_pred
        plt.scatter(y_pred, residuals, color='#ff00cc', alpha=0.6, edgecolors='none', s=50)
        plt.axhline(y=0, color='#00e5ff', lw=2, linestyle='--')
        plt.xlabel('Predicted Values', fontsize=12)
        plt.ylabel('Residuals', fontsize=12)
        plt.title(f'Residual Analysis: {model_name}', fontsize=16, weight='bold', color="#00e5ff", pad=20)
        plt.grid(alpha=0.1)
        plt.tight_layout()
        plt.savefig(os.path.join(save_path, 'model_residuals_plot.png'), dpi=200, facecolor='#050a14')
        plt.close()
