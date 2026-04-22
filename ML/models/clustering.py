from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
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
            'Agglomerative': AgglomerativeClustering(n_clusters=3)
        }

    def get_model_list(self):
        return list(self.models.keys())

    def train_and_eval(self, X, selected_model='K-Means'):
        model = self.models.get(selected_model)
        if not model:
            raise ValueError(f"Model {selected_model} not found.")

        # Train
        st = time.time()
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
                from sklearn.decomposition import PCA
                pca = PCA(n_components=2)
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
