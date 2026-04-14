import pandas as pd
import sqlite3
from pymongo import MongoClient
import os

class DataLoader:
    @staticmethod
    def load_csv(file_path):
        try:
            return pd.read_csv(file_path)
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding='latin1')

    @staticmethod
    def load_excel(file_path):
        return pd.read_excel(file_path)

    @staticmethod
    def load_sql(connection_string, table_name):
        try:
            # Basic sqlite3 connection for now, can be extended to sqlalchemy
            conn = sqlite3.connect(connection_string)
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            raise ValueError(f"SQL Load Error (Table: {table_name}): {str(e)}")

    @staticmethod
    def load_mongodb(connection_uri, db_name, collection_name):
        try:
            client = MongoClient(connection_uri)
            db = client[db_name]
            collection = db[collection_name]
            data = list(collection.find())
            if not data:
                return pd.DataFrame()
            df = pd.DataFrame(data)
            if '_id' in df.columns:
                df = df.drop(columns=['_id'])
            return df
        except Exception as e:
            raise ValueError(f"MongoDB Load Error (Collection: {collection_name}): {str(e)}")

    @classmethod
    def load_data(cls, source_type, **kwargs):
        if source_type == 'file' or source_type == 'csv' or source_type == 'excel':
            file_path = kwargs.get('file_path')
            if not file_path:
                raise ValueError("file_path is required for file source")
            if file_path.endswith(('.xlsx', '.xls')):
                return cls.load_excel(file_path)
            else:
                return cls.load_csv(file_path)
        elif source_type == 'sql':
            return cls.load_sql(kwargs.get('connection_string'), kwargs.get('table_name'))
        elif source_type == 'mongodb':
            return cls.load_mongodb(kwargs.get('connection_uri'), kwargs.get('db_name'), kwargs.get('collection_name'))
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
