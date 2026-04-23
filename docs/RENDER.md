# Render.com Deployment Guide

This document provides instructions for deploying **MLSuite** to [Render.com](https://render.com/) using the provided `render.yaml` Blueprint.

## Architecture Overview
- **Backend**: Containerized FastAPI service running on a **Starter** plan (to support persistent disks).
- **Frontend**: High-performance static site hosted on Render's CDN.
- **Persistence**: A 1GB persistent disk mounted to the backend to store `nanodb.json` and user uploads.

## Prerequisites
1. A [Render](https://dashboard.render.com/) account.
2. A GitHub repository containing the project code.

## Deployment Steps

### 1. Connect Repository
1. Log in to the Render Dashboard.
2. Click **New +** and select **Blueprint**.
3. Connect your GitHub repository.
4. Render will automatically detect the `render.yaml` file.

### 2. Configuration
- Render will prompt you for any missing environment variables (though most are automated in the blueprint).
- The `SECRET_KEY` will be automatically generated.
- The `VITE_API_BASE_URL` will be automatically linked from the backend service.

### 3. Monitoring
- Once deployed, you can monitor the logs for both services in the Render dashboard.
- The backend health check is configured at `/health`.

## Post-Deployment Tasks

### 1. Security (CORS)
By default, `CORS_ORIGINS` is set to `*`. For production, it is recommended to update this in the Render Dashboard for the backend service:
- Go to **Backend Service** -> **Environment**.
- Update `CORS_ORIGINS` to your frontend URL (e.g., `https://mlsuite-frontend.onrender.com`).

### 2. Scaling
If you need more storage, you can increase the disk size in the **Disks** section of the backend service.

## Troubleshooting
- **Disk Permissions**: If the backend fails to write to `/app/data`, ensure the directory exists and is writable by the user defined in the `Dockerfile`. The current blueprint mounts it at `/app/data`, and the app handles directory creation.
- **Vite Build**: If the frontend fails to connect to the backend, verify that `VITE_API_BASE_URL` is correctly set in the environment variables of the Static Site.
