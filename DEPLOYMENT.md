# MLSuite Deployment Guide

This document outlines the procedure for deploying **MLSuite** to both Google Cloud Platform (GCP) and Amazon Web Services (AWS) using automated CI/CD pipelines via GitHub Actions.

---

## 1. Cloud Architecture Overview

The system is designed to be cloud-agnostic, using containerized services:
- **Backend**: FastAPI app (Python)
- **Frontend**: React app (Vite/TS)
- **Database**: Local JSON (NanoDB) for demo, or external MongoDB/SQL.
- **CI/CD**: GitHub Actions for automated build and deployment.

---

## 2. AWS Deployment (Recommended)

### 2.1 Infrastructure Setup
- **AWS App Runner**: Recommended for hosting both backend and frontend as it handles scaling, SSL, and load balancing automatically.
- **Amazon ECR**: For storing Docker images.
- **AWS Secrets Manager**: For sensitive environment variables.

### 2.2 Manual Preparation
1. Create two ECR repositories: `mlsuite-backend` and `mlsuite-frontend`.
2. Create two App Runner services using the images from ECR.
3. Obtain the **Service ARNs** for both.

### 2.3 GitHub Secrets
Add the following to your GitHub repository secrets:
- `AWS_ACCESS_KEY_ID`: Your AWS Access Key.
- `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Key.
- `AWS_BACKEND_SERVICE_ARN`: ARN of the Backend App Runner service.
- `AWS_FRONTEND_SERVICE_ARN`: ARN of the Frontend App Runner service.

### 2.4 Persistence (Important for AWS)
Since **AWS App Runner** is stateless, any data in `uploads/`, `static/plots/`, or `nanodb.json` will be lost when the container restarts. To persist this data:
1.  **Amazon EFS**: Create an EFS file system.
2.  **App Runner EFS Mount**: Mount the EFS volume to `/app/persistent_data`.
3.  **Environment Variables**: Set the following in App Runner:
    - `NANODB_PATH=/app/persistent_data/nanodb.json`
    - `UPLOAD_DIR=/app/persistent_data/uploads`
    - `STATIC_DIR=/app/persistent_data/plots`
    - `MODELS_DIR=/app/persistent_data/models`

### 2.5 Security & Secrets Manager
Instead of hardcoding sensitive keys in `.env`, use **AWS Secrets Manager**:
- Store `SECRET_KEY` and `DATABASE_URL` as secrets.
- Reference these secrets in the App Runner service configuration.

### 2.6 Workflow Logic
The project uses two primary pipelines:
1.  **CI Pipeline (CL)**: Located in `.github/workflows/ci.yml`. It runs linting, testing, and build checks on every push and pull request.
2.  **CD Pipeline (CD)**: Located in `.github/workflows/cd.yml`. It handles the automated build and deployment to AWS (App Runner) upon successful pushes to `main`.

#### 2.6.1 CD Pipeline Steps:
1. Builds Docker images for both services.
2. Injects `VITE_API_BASE_URL` into the frontend build via a GitHub Secret.
3. Pushes them to Amazon ECR.
4. Triggers an update to the App Runner services with the new image tags.

### 2.7 Centralized Configuration
The frontend uses `frontend/src/api/config.ts` to manage the API base URL. In production, it defaults to `window.location.origin` but can be overridden by setting the `VITE_API_BASE_URL` build-arg in the Docker build or by defining it in the CI/CD pipeline secrets.

---

## 3. Render.com Deployment (Simplest)

For a quick and easy deployment with persistent storage:
1. Use the `render.yaml` blueprint provided in the root.
2. Follow the detailed instructions in [docs/RENDER.md](docs/RENDER.md).

### 3.1 Blueprint Features
- **Auto-linking**: Automatically connects the frontend to the backend URL.
- **Persistence**: Mounts a disk for `nanodb.json` and uploads.
- **Zero-Config Secrets**: Generates JWT secrets automatically.

---

## 4. GCP Deployment
... [rest of GCP section] ...

---

## 4. Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port for the service. | `8000` |
| `NANODB_PATH` | Path to the metadata JSON file. | `nanodb.json` |
| `UPLOAD_DIR` | Directory for uploaded files. | `uploads` |
| `VITE_API_BASE_URL` | Public URL of the Backend. | `window.location.origin` |
| `SECRET_KEY` | JWT signing key. | `super-secret-key` |

---

## 5. Security Note

**CRITICAL**: Ensure that `nanodb.json`, `.env`, and any `.pkl` files are NEVER committed to the repository. The `.gitignore` and `.dockerignore` files have been configured to exclude these. In production, always use managed services (RDS, S3) or persistent volumes (EFS) for storage.

---

## 6. Manual Deployment (Docker)

```bash
# Backend
docker build -t mlsuite-backend ./backend
docker run -p 8000:8000 mlsuite-backend

# Frontend
docker build -t mlsuite-frontend ./frontend
docker run -p 80:80 mlsuite-frontend
```
