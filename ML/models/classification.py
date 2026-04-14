from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ClassificationModels:
    def __init__(self):
        self.models = {
            'Logistic Regression': LogisticRegression(max_iter=1000),
            'SVC': SVC(probability=True),
            'Decision Tree': DecisionTreeClassifier(),
            'Random Forest': RandomForestClassifier(n_estimators=100)
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
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            self.results[name] = {
                'Accuracy': accuracy,
                'F1 Score': f1
            }
        return self.results

    def get_best_model(self):
        # Best model based on highest Accuracy
        best_name = max(self.results, key=lambda x: self.results[x]['Accuracy'])
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

        # 1. Confusion Matrix
        plt.figure(figsize=(10, 8))
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='mako', cbar=True, 
                    annot_kws={"size": 12, "weight": "bold"})
        plt.title(f'Confusion Matrix: {model_name}', fontsize=16, weight='bold', color="#00e5ff", pad=20)
        plt.xlabel('Predicted Label', fontsize=12, labelpad=10)
        plt.ylabel('True Label', fontsize=12, labelpad=10)
        plt.tight_layout()
        plt.savefig(os.path.join(save_path, 'model_confusion_matrix.png'), dpi=200, facecolor='#050a14')
        plt.close()

        # 2. ROC Curve / Probabilities
        try:
            if hasattr(model, "predict_proba"):
                plt.figure(figsize=(10, 8))
                y_score = model.predict_proba(X_test)
                
                # Plot for the first class for simplicity, or macro-average logic
                if len(model.classes_) == 2:
                    fpr, tpr, _ = roc_curve(y_test, y_score[:, 1], pos_label=model.classes_[1])
                    roc_auc = auc(fpr, tpr)
                    plt.plot(fpr, tpr, color='#00e5ff', lw=3, label=f'ROC curve (Area = {roc_auc:0.2f})')
                else:
                    # Multi-class fallback
                    plt.text(0.5, 0.5, "Multi-class ROC coming soon", ha='center', va='center')
                
                plt.plot([0, 1], [0, 1], color='#1f2937', lw=2, linestyle='--')
                plt.xlim([0.0, 1.0])
                plt.ylim([0.0, 1.05])
                plt.xlabel('False Positive Rate', fontsize=12)
                plt.ylabel('True Positive Rate', fontsize=12)
                plt.title(f'Neural Performance (ROC): {model_name}', fontsize=16, weight='bold', color="#00e5ff", pad=20)
                plt.legend(loc="lower right", frameon=True, facecolor='#050a14', edgecolor='#00e5ff')
                plt.grid(alpha=0.1)
                plt.tight_layout()
                plt.savefig(os.path.join(save_path, 'model_roc_curve.png'), dpi=200, facecolor='#050a14')
            plt.close()
        except Exception:
            plt.close()
