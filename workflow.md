# MLSuite Workflow Implementation Protocol

This document outlines the iterative development procedure followed to build the MLSuite platform's machine learning and hyperparameter tuning features. By documenting each phase, we can evaluate architectural choices, feature additions, and pipeline improvements.

## First Iteration: Foundation & Supervised Learning Pipeline
**Focus:** Establishing the core backend processes, automated supervised learning, and initial frontend integration.

- **Data Loading & Preprocessing:** Implemented the `DataLoader` and `Preprocessor` classes to accept CSV data, handle missing values, map targets, and perform basic feature scaling.
- **Model Orchestration (Supervised):** Built `ClassificationModels` and `RegressionModels` components. These components iterate over popular scikit-learn models (e.g., Logistic Regression, Random Forest, SVC). 
- **Automated Hyperparameter Tuning:** Implemented `MLTuner.run_automated_comparison`, allowing the backend to scan multiple model geometries via `GridSearchCV`.
- **Leaderboard UX:** Exposed `/train` endpoint returning ranked model statistics. Integrated this to the frontend Dashboard's "Leaderboard" to rank models automatically by $R^2$ or Accuracy score.

## Second Iteration: Unsupervised Integration (Clustering)
**Focus:** Introducing unsupervised capability and fixing endpoint authentication blockers.

- **Clustering Module Addition:** Created `ClusteringModels` with integrations for K-Means, DBSCAN, and Agglomerative clustering.
- **Metrics Shift:** Adjusted the metric logic to evaluate Silhouette, Davies-Bouldin, and Calinski-Harabasz scores instead of supervised metrics for label-less modeling.
- **UI Task Switcher:** Enhanced the Frontend `Dashboard` configuration step to hide target-variable selection when "Clustering" is enabled.
- **Environment Maintenance:** Handled system-wide 403 Forbidden errors when fetching admin statistics due to rigid JWT token configurations, modifying `main.py` admin dependencies to allow proper visibility for debugging.

## Third Iteration: Hybrid Manual Override & State Persistance 
**Focus:** Putting deep control back in the user's hands through manual configuration overlays.

- **Best-Params Extraction:** Upgraded `MLTuner` and local trainer configurations to accurately capture `.best_params_` parameters extracted during GridSearch runs for both supervised and clustering algorithms.
- **Frontend Override Mechanism:** Displayed an "Override Parameters" button directly inside the Winner Leaderboard card. Once clicked, this populates a JSON-editor text-area filled with the optimal hyperparameters discovered.
- **Conditional Retraining Loop:** Created conditional rules in `/train`. If the frontend triggers `isManualTuning`, `tune=False` is passed alongside `manual_params`. The backend `train_single_model` logic evaluates this json mapping and uses `.set_params()` on the Scikit-learn artifact before a forced refit.
- **Dominant Neural Kernel State:** Ensuring that custom, manual model fitting automatically forwards to the performance and visualization plots ("Dominant Neural Kernel" screen) skipping the automatic leaderboard hierarchy to give a true representation of user modifications.

## Fourth Iteration: Legacy API Compatibility & Refinement
**Focus:** Ensuring legacy endpoints dynamically synchronize with our new training architectures across all models.

- **`/process` Route Update:** Truncated the legacy `/process` route mapping error in `backend/main.py`. The legacy route was passing unmapped, flat arguments `(filename, config.task_type, config.target_column...)` into the newly parameterized `train_model()` function, causing silent crashes. 
- **Legacy Fallbacks:** Implemented keyword-argument (Kwargs) mapping passing explicit configurations (`model_name=model_name`, `task_type=config.task_type`) and establishing "K-Means" as the immediate fallback algorithm if the system encounters a legacy clustering request without a selected model.
- **Service Recovery:** Auto-started the Uvicorn application to re-initialize internal workers efficiently with zero exit-code errors.
