import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

class Preprocessor:
    def __init__(self, df):
        self.df = df
        self.imputer_num = SimpleImputer(strategy='mean')
        self.imputer_cat = SimpleImputer(strategy='most_frequent')
        self.scaler = StandardScaler()
        self.label_encoders = {}

    def handle_missing_values(self):
        import numpy as np
        # Replace infinity with NaN
        self.df.replace([np.inf, -np.inf], np.nan, inplace=True)
        # Numeric missing values
        num_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        if not num_cols.empty:
            self.df[num_cols] = self.imputer_num.fit_transform(self.df[num_cols])

        # Categorical missing values
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns
        if not cat_cols.empty:
            self.df[cat_cols] = self.imputer_cat.fit_transform(self.df[cat_cols])

        return self.df

    def standardize(self, exclude_cols=None):
        # Numerical columns scale
        num_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        if exclude_cols:
            num_cols = [c for c in num_cols if c not in exclude_cols]
            
        if len(num_cols) > 0:
            self.df[num_cols] = self.scaler.fit_transform(self.df[num_cols])
        return self.df

    def encode_categorical(self):
        # Label encode categorical columns
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            le = LabelEncoder()
            self.df[col] = le.fit_transform(self.df[col].astype(str))
            self.label_encoders[col] = le
        return self.df

    def sanitize_column_names(self):
        import re
        # Comprehensive sanitization for LightGBM/XGBoost/JSON compatibility
        # Replace any character that is not alphanumeric or underscore with '_'
        self.df.columns = [re.sub(r'[^a-zA-Z0-9]', '_', str(col)) for col in self.df.columns]
        return self.df

    def process_all(self, target_col=None):
        import re
        if target_col:
            # Predict what the sanitized target column name will be
            new_target_col = re.sub(r'[^a-zA-Z0-9]', '_', str(target_col))
        else:
            new_target_col = None
            
        self.sanitize_column_names()
        self.handle_missing_values()
        self.encode_categorical()
        # Keep target column as is (discrete) for classification/regression targets
        self.standardize(exclude_cols=[new_target_col] if new_target_col else None)
        return self.df, new_target_col
