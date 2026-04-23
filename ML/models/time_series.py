from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time

class TimeSeriesModels:
    def __init__(self):
        # Default order (1,1,1) for ARIMA
        self.models = {
            'ARIMA': None  # Will be initialized during training
        }

    def get_model_list(self):
        return list(self.models.keys())

    def train_and_eval(self, y, selected_model='ARIMA', order=(1,1,1)):
        # For ARIMA, we need a univariate series
        st = time.time()
        try:
            model = ARIMA(y, order=order)
            model_fit = model.fit()
        except Exception as e:
            # Fallback or error
            return {selected_model: {"error": str(e)}}

        train_time = round(time.time() - st, 4)
        
        # Simple evaluation: AIC, BIC
        aic = model_fit.aic
        bic = model_fit.bic
        
        return {
            selected_model: {
                'AIC': round(float(aic), 4),
                'BIC': round(float(bic), 4),
                'Training Time (s)': train_time,
                'fitted_model': model_fit
            }
        }

    def generate_visualizations(self, model_fit, series, static_dir):
        plt.figure(figsize=(10, 6))
        plt.plot(series, label='Observed')
        plt.plot(model_fit.fittedvalues, color='red', label='Fitted')
        plt.title('ARIMA Model Fit')
        plt.legend()
        
        filepath = os.path.join(static_dir, "time_series_fit.png")
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()
        
        # Also forecast
        plt.figure(figsize=(10, 6))
        forecast = model_fit.forecast(steps=10)
        plt.plot(series, label='Observed')
        plt.plot(np.arange(len(series), len(series) + 10), forecast, color='green', label='Forecast')
        plt.title('ARIMA Forecast (Next 10 Steps)')
        plt.legend()
        
        filepath = os.path.join(static_dir, "time_series_forecast.png")
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()
