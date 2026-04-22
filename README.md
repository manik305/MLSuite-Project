# MLSuite: Automated Machine Learning Pipeline

MLSuite is an end-to-end platform for automated data preprocessing, Exploratory Data Analysis (EDA), and machine learning model optimization. 

## Features
- **Aesthetic**: **Digital Nebula (Ethereal Intelligence)**. A high-end editorial dark theme featuring:
    - **No-Line Rule**: Visual hierarchy defined by surface tonal shifts (#060e1d, #0b1323, #18202f).
    - **Glassmorphism**: 20px blur panels using the "Precision Glassware" specification.
    - **Typography**: Space Grotesk (Display) and Inter (Body) for an authoritative, premium feel.
    - **Interactive Data**: Confidence meters and glowing primary-colored nodes.
- **Authentication**: Secure login and session management.
- **Data Upload**: Support for SQL, MongoDB (NoSQL), Excel, and CSV files.
- **Auto-Preprocessing**: Automated handling of missing values and feature standardization.
- **Intelligent EDA**: Dynamic visualization of data distributions, correlations, and outlier analysis.
- **Reporting Freshness Policy**: Automatic clearing of previous run artifacts to ensure data integrity.
- **Model Optimization**: Advanced hyperparameter tuning and best-model selection using `GridSearchCV`:
    - **Classification**: Logistic Regression, SVC, Random Forest, XGBoost, and more.
    - **Regression**: Linear Regression, SVR, Decision Trees, AdaBoost, GBM, XGBoost, LightGBM, and CatBoost.
- **Expert-Grade Evaluation**: Standardized performance reporting using core industry metrics:
    - **Regression**: Optimized for **Mean Absolute Error (MAE)**, **Mean Squared Error (MSE)**, and **Root Mean Squared Error (RMSE)** for maximum precision.
    - **Classification**: Precision, Recall, F1-Score, and AUC-ROC analysis.

## Tech Stack
- **Frontend**: TypeScript, React, Vite, Tailwind CSS (Featuring the "Digital Nebula" Base Design Aesthetic).
- **Backend**: Python, FastAPI.
- **Database**: NanoDB & MongoDB.
- **ML Libraries**: Scikit-Learn, Pandas, Matplotlib.

## Getting Started (Coming Soon)
For more details on the system architecture and requirements, see:
- [PRD.md](./PRD.md)
- [design.md](./design.md)

## Folder Structure
```text
MLSuite/
├── ML/ (Automated ML Logic)
│   ├── data_loader.py (SQL/MongoDB)
│   ├── preprocessor.py
│   ├── eda_engine.py (Matplotlib)
│   ├── tuner.py
│   └── models/ (Regression & Classification)
├── backend/ (FastAPI)
├── frontend/ (TypeScript + Tailwind)
├── database/ (NanoDB)
└── README.md
```

## License
MIT License.
