# System Design: MLSuite

## 1. High-Level Architecture
MLSuite follows a classic three-tier architecture:
- **Presentation Layer**: React + TypeScript frontend, styled with Tailwind CSS for a premium look.
- **Service Layer**: FastAPI backend providing RESTful endpoints for data handling and ML processing.
- **Persistence Layer**: NanoDB for user and project metadata, combined with the local filesystem for dataset storage.

## 2. Component Design

### 2.1 Frontend (Presentation)
- **Framework**: Vite + React + TypeScript.
- **Styling**: Tailwind CSS + Modern UI components (e.g., Shadcn/UI patterns).
- **State Management**: React Context or Zustand for user auth and dataset state.
- **Routing**: React Router for navigation between Home, Auth, and Dashboard.
- **Visualization**: Matplotlib (customized for high-quality screening in frontend).

### 2.2 Backend (FastAPI)
- **API Framework**: FastAPI with Pydantic for validation.
- **Auth**: JWT-based authentication for secure session management.
- **ML Engine**: A modular Python package (`ML/`) that handles:
    - Data cleaning/imputation.
    - Feature scaling (StandardScaler/MinMax).
    - EDA generation (using Seaborn/Matplotlib to export images/JSON).
    - GridSearch for hyperparameter tuning.

### 2.3 ML Folder Structure
All machine learning logic resides in the `ML/` directory:
- `ML/data_loader.py`: Handles SQL, MongoDB (NoSQL), Excel, and CSV ingestion.
- `ML/preprocessor.py`: Implements missing value detection and standardization.
- `ML/eda_engine.py`: Generates visual analysis graphs using Matplotlib.
- `ML/models/`:
    - `regression.py`: Linear Regression and Support Vector Regression implementations.
    - `classification.py`: Logistic Regression and Support Vector Classification implementations.
- `ML/tuner.py`: Automated hyperparameter tuning and model comparison.

### 2.4 Database Schema (NanoDB)
NanoDB stores project-level information. Key collections:
- `users`: `{id, email, password_hash}`.
- `datasets`: `{id, name, path, uploaded_at, type}`.
- `models`: `{id, dataset_id, type, parameters, accuracy, f1_score, r2_score}`.

## 3. Data Flow
1. **Authentication**: User logs in -> Receive JWT.
2. **Upload**: User uploads file (CSV/Excel) -> Backend stores it in `/uploads/` and logs entry in NanoDB.
3. **Preprocessing**: User triggers preprocessing -> Backend reads file, handles missing values, and standardizes data using `ML/preprocessor.py`.
4. **EDA**: Backend generates graphs using `ML/eda_engine.py` -> Sends URLs/data to Frontend.
5. **Training/Tuning**: User selects "Regression" or "Classification" -> Backend runs hyperparameter tuning across relevant models -> Best model is saved and results are returned.

## 4. Design Guidelines
- **Responsive Design**: Ensure dashboard works across various screen sizes.
- **Interactivity**: Graphs should allow zooming and data inspection.
- **User Feedback**: Loaders and progress bars for long-running preprocessing/tuning tasks.
- **Aesthetics**: Dark mode support, glassmorphism elements, and smooth transitions.
