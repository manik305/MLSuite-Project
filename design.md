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
- **Reflective Backgrounds**: Use ultra-subtle radial gradients to simulate light reflecting off polished dark surfaces, enhancing the premium feel.
- **Chromatic Bloom**: Focused or active elements emit a soft, tinted glow to simulate light passing through glass.

## 5. Visual Design System: The Digital Nebula

### 5.1 Overview
The "Digital Nebula" aesthetic moves away from clinical ML interfaces toward a high-end, editorial experience. It emphasizes depth, mystery, and multi-dimensional intelligence. The UI is treated as a series of light-emitting surfaces suspended in a vast, dark void.

### 5.2 Key Design Principles
- **The "No-Line" Rule**: Avoid 1px solid borders. Use background tonal shifts (e.g., `surface` vs `surface_container_low`) to define boundaries.
- **Glassmorphism**: Floating panels use 60% opacity backgrounds with 20px backdrop-blur.
- **Reflective Backgrounds**: Incorporate ultra-subtle radial gradients (5% opacity) of primary (`#9cf0ff`) and secondary (`#e0e0ff`) colors positioned asymmetrically to simulate light reflecting off polished dark surfaces.
- **Chromatic Bloom**: Interactive elements emit a soft glow (`rgba(0, 218, 243, 0.15)`) when focused, creating the illusion of light passing through glass.
- **Intentional Asymmetry**: Balance heavy data tables with expansive negative space to create a curated, cinematic feel.

### 5.3 Color Palette (Nebula)
- **Base**: `#0b1323` (Deep Space Blue)
- **Primary**: `#c3f5ff` to `#00e5ff` (Electric Cyan Gradient)
- **Surface**: Tonal layering from `#060e1d` (Lowest) to `#2d3546` (Highest).
- **Reflective Tones**: `#9cf0ff` (Primary Fixed) and `#e0e0ff` (Secondary Fixed) at low opacity for background highlights.

### 5.4 Typography
- **Headlines**: Space Grotesk (Technical yet expressive). Tight letter-spacing (-0.04em) for display titles.
- **Body**: Inter (Neutral workhorse).
- **Data/Labels**: Manrope (High numeric legibility for metadata and scores).
