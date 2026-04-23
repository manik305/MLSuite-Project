from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score, mean_absolute_error
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
            'SVR': {'C': [0.1, 1, 10], 'epsilon': [0.01, 0.1, 1]},
            'K-Means': {'n_clusters': [2, 3, 4, 5, 6]},
            'DBSCAN': {'eps': [0.3, 0.5, 0.7], 'min_samples': [3, 5, 10]},
            'Agglomerative': {'n_clusters': [2, 3, 4, 5, 6]},
            'PCA': {'n_components': [2, 3, 5]},
            'ARIMA': {'p': [1, 2], 'd': [1], 'q': [1]}
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
        from ML.models.clustering import ClusteringModels
        
        if task_type == 'classification':
            collector = ClassificationModels()
        elif task_type == 'regression':
            collector = RegressionModels()
        elif task_type == 'clustering':
            collector = ClusteringModels()
        elif task_type == 'time_series':
            from ML.models.time_series import TimeSeriesModels
            collector = TimeSeriesModels()
        else:
            raise ValueError("Unsupported task type")
            
        leaderboard = []
        best_overall_score = -float('inf')
        winner_name = None
        winner_model = None

        if task_type == 'clustering':
            # Combine X for clustering tuning
            X_all = pd.concat([X_train, X_test]) if X_test is not None and not X_test.empty else X_train
            from sklearn.metrics import silhouette_score
            from sklearn.model_selection import ParameterGrid
            
            for model_name, base_predictor in collector.models.items():
                param_grid = cls.get_param_grid(model_name)
                best_score = -1.0
                best_model = None
                
                best_params_val = None
                
                if not param_grid:
                    params_list = [{}]
                else:
                    params_list = list(ParameterGrid(param_grid))
                    
                for params in params_list:
                    model = clone(base_predictor)
                    model.set_params(**params)
                    
                    if model_name == 'PCA':
                        model.fit(X_all)
                        # For PCA, use Explained Variance as a surrogate score for comparison
                        score = np.sum(model.explained_variance_ratio_)
                        labels = None
                    elif model_name == 'DBSCAN':
                        labels = model.fit_predict(X_all)
                        unique_labels = np.unique(labels)
                        if len(unique_labels) > 1 and len(unique_labels) < len(X_all):
                            score = silhouette_score(X_all, labels)
                        else:
                            score = -1.0
                    else:
                        model.fit(X_all)
                        labels = model.labels_
                        unique_labels = np.unique(labels)
                        if len(unique_labels) > 1 and len(unique_labels) < len(X_all):
                            score = silhouette_score(X_all, labels)
                        else:
                            score = -1.0
                        
                    if score > best_score:
                        best_score = score
                        best_model = model
                        best_params_val = params
                
                 # Convert numpy types to native types for JSON serialization if necessary
                if best_params_val:
                    for k, v in best_params_val.items():
                        if hasattr(v, 'item'):
                            best_params_val[k] = v.item()

                model_entry = {
                    'model_name': model_name,
                    'score': round(best_score, 4),
                    'error_rate': 0.0,
                    'metric_name': 'Variance Explained' if model_name == 'PCA' else 'Silhouette Score',
                    'mae': None,
                    'rmse': None,
                    'best_params': best_params_val,
                    'is_winner': False
                }
                leaderboard.append(model_entry)
                
                if best_score > best_overall_score:
                    best_overall_score = best_score
                    winner_name = model_name
                    winner_model = best_model

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

        if task_type == 'time_series':
            # Simplified ARIMA comparison for now
            for model_name in collector.get_model_list():
                # For ARIMA we use AIC as the metric
                res = collector.train_and_eval(y_train, selected_model=model_name)
                metrics = res[model_name]
                
                leaderboard.append({
                    'model_name': model_name,
                    'score': metrics['AIC'], # Lower is better, but tuner expects higher is better?
                    'error_rate': metrics['BIC'],
                    'metric_name': 'AIC',
                    'mae': None,
                    'rmse': None,
                    'best_params': {'order': (1,1,1)},
                    'is_winner': True
                })
                winner_name = model_name
                winner_model = metrics['fitted_model']

            return {
                'leaderboard': leaderboard,
                'winner_name': winner_name,
                'best_model': winner_model,
                'task_type': task_type
            }

        # For Supervised tasks
        for model_name, base_predictor in collector.models.items():
            # 1. Base Evaluation
            base_model = clone(base_predictor)
            base_model.fit(X_train, y_train)
            base_preds = base_model.predict(X_test)
            
            # Initialize metrics
            tuned_mse = tuned_mae = tuned_rmse = None
            base_mse = base_mae = base_rmse = None
            
            if task_type == 'classification':
                base_score = accuracy_score(y_test, base_preds)
                base_error = 1.0 - base_score
                metric_name = 'Accuracy'
            else:
                base_score = r2_score(y_test, base_preds)
                # For regression, we now track a richer set of errors
                base_mse = mean_squared_error(y_test, base_preds)
                base_mae = mean_absolute_error(y_test, base_preds)
                base_rmse = np.sqrt(base_mse)
                base_error = base_rmse # Use RMSE as default error rate for leaderboard
                metric_name = 'R2 Score'

            # 2. Tuning Evaluation
            param_grid = cls.get_param_grid(model_name)
            if param_grid:
                # Optimized Grid Search with professional CV and error metrics
                from sklearn.model_selection import GridSearchCV
                grid_search = GridSearchCV(base_model, param_grid, cv=5, n_jobs=-1, scoring='accuracy' if task_type == 'classification' else 'r2')
                grid_search.fit(X_train, y_train)
                tuned_model = grid_search.best_estimator_
                tuned_preds = tuned_model.predict(X_test)
                
                if task_type == 'classification':
                    tuned_score = accuracy_score(y_test, tuned_preds)
                    tuned_error = 1.0 - tuned_score
                else:
                    tuned_score = r2_score(y_test, tuned_preds)
                    tuned_mse = mean_squared_error(y_test, tuned_preds)
                    tuned_mae = mean_absolute_error(y_test, tuned_preds)
                    tuned_rmse = np.sqrt(tuned_mse)
                    tuned_error = tuned_rmse
                
                best_params_val = grid_search.best_params_
                if best_params_val:
                    for k, v in best_params_val.items():
                        if hasattr(v, 'item'):
                            best_params_val[k] = v.item()

            else:
                tuned_model = base_model
                tuned_score = base_score
                tuned_error = base_error
                tuned_mse = base_mse if task_type == 'regression' else None
                tuned_mae = base_mae if task_type == 'regression' else None
                tuned_rmse = base_rmse if task_type == 'regression' else None
                best_params_val = None

            # Add to leaderboard
            model_entry = {
                'model_name': model_name,
                'score': round(tuned_score, 4),
                'error_rate': round(tuned_error, 4),
                'metric_name': metric_name,
                'mae': round(tuned_mae, 4) if task_type == 'regression' else None,
                'rmse': round(tuned_rmse, 4) if task_type == 'regression' else None,
                'best_params': best_params_val,
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
