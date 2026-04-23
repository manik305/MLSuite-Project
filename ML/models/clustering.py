from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import time

class ClusteringModels:
    def __init__(self):
        self.models = {
            'K-Means': KMeans(n_clusters=3, random_state=42),
            'DBSCAN': DBSCAN(eps=0.5, min_samples=5),
            'Agglomerative': AgglomerativeClustering(n_clusters=3),
            'PCA': PCA(n_components=2) # Added PCA as requested
        }

    def get_model_list(self):
        return list(self.models.keys())

    def train_and_eval(self, X, selected_model='K-Means'):
        model = self.models.get(selected_model)
        if not model:
            raise ValueError(f"Model {selected_model} not found.")

        # Train
        st = time.time()
        if selected_model == 'PCA':
            model.fit(X)
            # PCA doesn't have labels, but we can compute explained variance
            exp_var = np.sum(model.explained_variance_ratio_)
            train_time = round(time.time() - st, 4)
            return {
                selected_model: {
                    'Explained Variance Ratio': round(float(exp_var), 4),
                    'n_components': model.n_components,
                    'Training Time (s)': train_time
                }
            }
        
        # DBSCAN doesn't have predict, it has fit_predict. All can just use fit_predict.
        if selected_model == 'DBSCAN':
            labels = model.fit_predict(X)
        else:
            model.fit(X)
            labels = model.labels_
        
        train_time = round(time.time() - st, 4)

        # Eval
        unique_labels = np.unique(labels)
        if len(unique_labels) > 1 and len(unique_labels) < len(X):
            sil_score = silhouette_score(X, labels)
        else:
            sil_score = -1.0 # Invalid for silhouette

        return {
            selected_model: {
                'Silhouette Score': round(sil_score, 4),
                'Estimated Clusters': int(len([l for l in unique_labels if l != -1])),
                'Training Time (s)': train_time
            }
        }

    def generate_visualizations(self, model_name, X, static_dir, trained_model=None):
        model = trained_model if trained_model else self.models[model_name]
        
        if model_name == 'PCA':
            X_pca = model.transform(X)
            plt.figure(figsize=(8, 6))
            plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.7)
            plt.title("PCA Dimensionality Reduction")
            plt.xlabel("Component 1")
            plt.ylabel("Component 2")
            filepath = os.path.join(static_dir, "model_cluster_scatter.png")
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()
            return

        if hasattr(model, 'labels_'):
            labels = model.labels_
        else:
            # Re-predict just for plot if we must
            labels = model.fit_predict(X)

        num_features = X.shape[1]
        
        if num_features >= 2:
            plt.figure(figsize=(8, 6))
            # Just scatter the first two principal components or columns as visualization
            if num_features > 2:
                from sklearn.decomposition import PCA as VizPCA
                pca = VizPCA(n_components=2)
                X_plot = pca.fit_transform(X)
                plt.scatter(X_plot[:, 0], X_plot[:, 1], c=labels, cmap='viridis', s=50, alpha=0.7)
                plt.title(f"{model_name} Clusters (PCA reduced)")
                plt.xlabel("PCA 1")
                plt.ylabel("PCA 2")
            else:
                X_plot = X.values if hasattr(X, 'values') else X
                plt.scatter(X_plot[:, 0], X_plot[:, 1], c=labels, cmap='viridis', s=50, alpha=0.7)
                plt.title(f"{model_name} Clusters")
                plt.xlabel("Feature 1")
                plt.ylabel("Feature 2")

            filepath = os.path.join(static_dir, f"model_cluster_scatter.png")
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()
