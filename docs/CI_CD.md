# MLSuite CI/CD Strategy

This document outlines the GitHub Actions pipeline implemented for the MLSuite project, ensuring robust model performance and automated documentation synchronization.

## 1. Pipeline Overview: `ml-pipeline.yml`

The "Smart Pipeline" is designed to handle the multi-disciplinary nature of this project (ML + Web).

### Phase 1: Validation
- **Unit Tests**: Runs `pytest` on the backend and ML modules.
- **Frontend Build**: Validates that the TypeScript/Vite frontend compiles without errors.
- **ML Benchmark**: A standalone "GitHub Action Function" (`scripts/model_benchmark.py`) that trains a sample model and verifies the R2 Score meets a minimum threshold (0.8).

### Phase 2: Synchronization
- **Google Sheets Sync**: On push to `main`, the pipeline triggers `scripts/sync_to_sheets.py`.
- **Target**: Updates the [MLsuit Sprintplan](https://docs.google.com/spreadsheets/d/17735uZEs0gB7x8XN6Ycy_JCWhMN4DS3ez8xAkXzKSVo) with the latest build status and system health stats.

### Phase 3: Deployment (CD)
- **Cloud Run**: The `cd.yml` workflow is configured to deploy the containerized backend to Google Cloud Run upon successful validation.

## 2. GitHub Action Functions (`ML/pipeline_actions.py`)

We have introduced a pattern of "Pipeline Functions"—modular Python methods specifically for automation:
- `generate_system_health_report()`: Summarizes DB and log stats.
- `sync_to_cloud_storage()`: Handles artifact persistence.

## 3. Required Secrets

To fully enable this pipeline, the following GitHub Secrets must be configured:
- `GOOGLE_SHEET_ID`: `17735uZEs0gB7x8XN6Ycy_JCWhMN4DS3ez8xAkXzKSVo`
- `GOOGLE_SYNC_TOKEN`: Service account JSON or OAuth token for Sheets API.
- `SLACK_WEBHOOK`: (Optional) For deployment notifications.
