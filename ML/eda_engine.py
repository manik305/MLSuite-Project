import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import shutil

class EDAEngine:
    def __init__(self, df, save_path):
        self.df = df
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        # Configure Seaborn for "Digital Nebula" dark theme
        sns.set_theme(style="darkgrid", rc={
            "axes.facecolor": "#0b1323",
            "figure.facecolor": "#0b1323",
            "text.color": "#c3f5ff",
            "axes.labelcolor": "#c3f5ff",
            "xtick.color": "#c3f5ff",
            "ytick.color": "#c3f5ff",
            "grid.color": "#1f2937",
            "axes.edgecolor": "#1f2937"
        })

    def clear_plots(self):
        """Removes all files in the plots directory to ensure fresh reports."""
        if os.path.exists(self.save_path):
            shutil.rmtree(self.save_path)
        os.makedirs(self.save_path)

    def _sanitize_filename(self, filename):
        """Replaces characters that are illegal in Windows filenames."""
        illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in illegal_chars:
            filename = filename.replace(char, '_')
        return filename

    def generate_histograms(self):
        num_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        for col in num_cols:
            try:
                plt.figure(figsize=(8, 6))
                sns.histplot(self.df[col], kde=True, color="#00e5ff", edgecolor="#0b1323")
                plt.title(f'Distribution of {col}', fontsize=14, weight='bold')
                plt.tight_layout()
                safe_col = self._sanitize_filename(col)
                plt.savefig(os.path.join(self.save_path, f'hist_{safe_col}.png'), dpi=150)
                plt.close()
            except Exception as e:
                print(f"Error generating histogram for {col}: {e}")
                plt.close()

    def generate_correlation_heatmap(self):
        # Numerical columns only
        num_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        if len(num_cols) < 2:
            return
        corr = self.df[num_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="mako", fmt=".2f", linewidths=.5, cbar_kws={"shrink": .8})
        plt.title('Feature Correlation Heatmap', fontsize=16, weight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(os.path.join(self.save_path, 'correlation_heatmap.png'), dpi=150)
        plt.close()

    def generate_boxplots(self):
        num_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        for col in num_cols:
            try:
                plt.figure(figsize=(8, 6))
                sns.boxplot(y=self.df[col], color="#00e5ff", fliersize=5, linewidth=1.5)
                plt.title(f'Outlier Analysis: {col}', fontsize=14, weight='bold')
                plt.tight_layout()
                safe_col = self._sanitize_filename(col)
                plt.savefig(os.path.join(self.save_path, f'box_{safe_col}.png'), dpi=150)
                plt.close()
            except Exception as e:
                print(f"Error generating boxplot for {col}: {e}")
                plt.close()

    def generate_data_composition_plot(self):
        """Generates a pie chart showing numerical vs categorical feature distribution."""
        num_count = self.df.select_dtypes(include=['number']).shape[1]
        cat_count = self.df.select_dtypes(include=['object', 'category']).shape[1]
        
        plt.figure(figsize=(8, 8))
        colors = ['#00e5ff', '#1f2937'] # Primary vs Surface Container
        plt.pie([num_count, cat_count], labels=['Numerical Features', 'Categorical Features'], 
                autopct='%1.1f%%', colors=colors, startangle=140, 
                textprops={'color': "#c3f5ff", 'weight': 'bold'})
        plt.title('Data Feature Composition', fontsize=16, weight='bold', color="#c3f5ff", pad=20)
        plt.tight_layout()
        plt.savefig(os.path.join(self.save_path, 'data_composition_pie.png'), dpi=150)
        plt.close()

    def get_data_stats(self):
        """Returns numerical and character counts from the dataframe."""
        num_df = self.df.select_dtypes(include=['number'])
        cat_df = self.df.select_dtypes(include=['object', 'category'])
        
        numerical_entries_count = num_df.count().sum()
        # Sum of lengths of all strings in categorical columns
        character_count = cat_df.astype(str).map(len).sum().sum()
        
        return {
            "numerical_entries": int(numerical_entries_count),
            "character_count": int(character_count),
            "num_features": int(num_df.shape[1]),
            "cat_features": int(cat_df.shape[1])
        }

    def generate_all(self):
        self.generate_data_composition_plot()
        self.generate_histograms()
        self.generate_correlation_heatmap()
        self.generate_boxplots()
        # Return sorted list of PNG files in the current save_path
        return sorted([f for f in os.listdir(self.save_path) if f.endswith('.png')])
