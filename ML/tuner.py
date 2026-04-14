from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.base import clone
import pandas as pd
import numpy as np

class MLTuner:
    @staticmethod
    def get_param_grid(model_name):
        grids = {
            'Logistic Regression': {'C': [0.1, 1, 10]},
            'Random Forest': {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20]},
            'Gradient Boosting': {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1]},
            'Decision Tree': {'max_depth': [None, 5, 10, 20], 'min_samples_split': [2, 5, 10]},
            'SVC': {'C': [0.1, 1, 10], 'gamma': ['scale', 'auto']},
            'Linear Regression': {},
            'Ridge Regression': {'alpha': [0.1, 1.0, 10.0]},
            'Lasso Regression': {'alpha': [0.1, 1.0, 10.0]},
            'SVR': {'C': [0.1, 1, 10], 'epsilon': [0.01, 0.1, 1]}
        }
        return grids.get(model_name, {})

    @classmethod
    def run_automated_comparison(cls, X_train, y_train, X_test, y_test, task_type):
        """
        Automated Model Comparison (Auto-Selection).
        Evaluates all available models for the given task type, performs tuning on each,
        and returns a leaderboard with prediction scores and error rates.
        """
        from ML.models.classification import ClassificationModels
        from ML.models.regression import RegressionModels
        
        collector = ClassificationModels() if task_type == 'classification' else RegressionModels()
        leaderboard = []
        best_overall_score = -float('inf')
        winner_name = None
        winner_model = None

        for model_name, base_predictor in collector.models.items():
            # 1. Base Evaluation
            base_model = clone(base_predictor)
            base_model.fit(X_train, y_train)
            base_preds = base_model.predict(X_test)
            
            if task_type == 'classification':
                base_score = accuracy_score(y_test, base_preds)
                base_error = 1.0 - base_score
                metric_name = 'Accuracy'
            else:
                base_score = r2_score(y_test, base_preds)
                base_error = mean_squared_error(y_test, base_preds)
                metric_name = 'R2 Score'

            # 2. Tuning Evaluation
            param_grid = cls.get_param_grid(model_name)
            if param_grid:
                grid_search = GridSearchCV(base_model, param_grid, cv=3, n_jobs=1)
                grid_search.fit(X_train, y_train)
                tuned_model = grid_search.best_estimator_
                tuned_preds = tuned_model.predict(X_test)
                
                if task_type == 'classification':
                    tuned_score = accuracy_score(y_test, tuned_preds)
                    tuned_error = 1.0 - tuned_score
                else:
                    tuned_score = r2_score(y_test, tuned_preds)
                    tuned_error = mean_squared_error(y_test, tuned_preds)
            else:
                tuned_model = base_model
                tuned_score = base_score
                tuned_error = base_error

            # Add to leaderboard
            model_entry = {
                'model_name': model_name,
                'score': round(tuned_score, 4),
                'error_rate': round(tuned_error, 4),
                'metric_name': metric_name,
                'is_winner': False
            }
            leaderboard.append(model_entry)

            if tuned_score > best_overall_score:
                best_overall_score = tuned_score
                winner_name = model_name
                winner_model = tuned_model

        # Sort leaderboard and mark winner
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        for entry in leaderboard:
            if entry['model_name'] == winner_name:
                entry['is_winner'] = True
                break

        return {
            'leaderboard': leaderboard,
            'winner_name': winner_name,
            'best_model': winner_model,
            'task_type': task_type
        }
