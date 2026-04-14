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
        # Numeric missing values
        num_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        if not num_cols.empty:
            self.df[num_cols] = self.imputer_num.fit_transform(self.df[num_cols])

        # Categorical missing values
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns
        if not cat_cols.empty:
            self.df[cat_cols] = self.imputer_cat.fit_transform(self.df[cat_cols])

        return self.df

    def standardize(self):
        # Numerical columns scale
        num_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        if not num_cols.empty:
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

    def process_all(self):
        self.handle_missing_values()
        self.encode_categorical()
        self.standardize()
        return self.df
