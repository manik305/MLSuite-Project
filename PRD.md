# Product Requirements Document (PRD): MLSuite

## 1. Project Overview
**MLSuite** is a comprehensive, automated Machine Learning pipeline platform designed to simplify the end-to-end ML process. It allows users to upload datasets from various sources, automatically preprocess data, perform Exploratory Data Analysis (EDA), and execute automated hyperparameter tuning for both regression and classification tasks.

## 2. Objectives
- Provide a user-friendly interface for non-experts to build ML models.
- Automate tedious data cleaning and preprocessing steps.
- Enable data exploration through automated visual analytics.
- Simplify model selection and optimization through automated hyperparameter tuning.
- Ensure secure access through email-based authentication.

## 3. Target Audience
- Data Scientists and Analysts looking for quick experimentation.
- Business users wanting to extract insights from their data without deep coding knowledge.
- Developers needing a rapid prototyping tool for ML models.

## 4. Functional Requirements

### 4.1 Authentication
- **User Registration/Login**: Secure login using Email ID and Password.
- **Session Management**: Persistent sessions for authenticated users.

### 4.2 Data Ingestion
- **Diverse Sources**: Support for uploading data from:
    - **SQL Databases** (via connection strings/files).
    - **NoSQL Databases**: MongoDB (support for connection strings and document uploads).
    - **Excel Files** (.xlsx, .xls).
    - **CSV Files** (.csv).
- **File Validation**: Ensure uploaded files are readable and within size limits.

### 4.3 Automated Preprocessing
- **Missing Value Handling**: Automatically identify and impute or remove missing values/items.
- **Standardization**: Feature scaling (e.g., StandardScaler, MinMax) to prepare data for modeling.
- **Categorical Encoding**: Auto-detection and encoding of non-numeric features.

### 4.4 Automated EDA (Exploratory Data Analysis)
- **Visual Analytics**: Generate a suite of graphs, including:
    - Distribution plots (histograms/densities).
    - Correlation heatmaps.
    - Scatter matrices.
    - Box plots for outlier detection.
- **Dashboard View**: A cohesive screening of all generated graphs.
- **Reporting Freshness Policy**: Automatically clears previous analysis artifacts at the start of each run to ensure report integrity and prevent stale data visualization.

### 4.5 Machine Learning Engine
- **Task Types**: Support for both Regression and Classification.
- **Algorithms**:
    - **Classification**: Logistic Regression, Support Vector Classification (SVC).
    - **Regression**: Linear Regression, Support Vector Regression (SVR).
- **Hyperparameter Tuning**: Automated search (e.g., GridSearch or RandomSearch) to find the optimal parameters for each model.
- **Best Model Selection**: Compare performance across supported algorithms and recommend the best-fit model for the specific dataset.

### 4.6 Reporting & Visualization
- **Model performance**: Reprint implementation results with clear metrics (Accuracy, F1, MSE, R2, etc.).
- **Screening**: High-quality visual representation of model performance:
    - **Classification**: Confusion Matrix and ROC Curves.
    - **Regression**: Actual vs. Predicted and Residual analysis plots.

## 5. Non-Functional Requirements
- **Performance**: Preprocessing and EDA should be responsive for reasonably sized datasets.
- **Security**: Database passwords and user credentials must be handled securely.
- **UX/UI**: **"Digital Nebula" (Ethereal Intelligence)**. A premium, high-end editorial aesthetic featuring:
    - **No-Line Rule**: Surfaces are separated by tonal background shifts (#060e1d to #0b1323) rather than 1px borders.
    - **Precision Glassware**: High-blur background-refractive panels for core UI elements.
    - **Ambient Nodes**: Soft primary-colored glows (#c3f5ff) that guide the eye toward active data.
    - **Editorial Typography**: Pairing *Space Grotesk* (Headings) with *Inter* (Body) and *Manrope* (Data/Monospace).
    - **Confidence Meters**: High-contrast, glowing progress visualizations for neural metrics.

## 6. Technical Stack
- **Frontend**: TypeScript, Tailwind CSS, React (Vite).
- **Backend**: Python, FastAPI.
- **Database**: NanoDB (internal storage); MongoDB (NoSQL upload source).
- **ML Libraries**: Scikit-Learn, Pandas, Matplotlib for all visualizations.

## 7. Project Structure (ML Folder)
All algorithms and pipeline logic will be organized within an `ML/` directory for modularity and scalability.
