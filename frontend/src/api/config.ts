/**
 * MLSuite API Configuration
 * Centralized logic for API base URL and common headers.
 */

const getApiBaseUrl = () => {
  // 1. Check if VITE_API_BASE_URL is set in environment (injected during build or deployment)
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }

  // 2. Fallback to current origin if in production (assuming same-host deployment)
  if (import.meta.env.PROD) {
    // If frontend is served from the same host or via proxy
    return window.location.origin;
  }

  // 3. Default for local development
  return 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();

export const getAuthHeaders = (token: string) => ({
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json',
});

export const getUploadHeaders = (token: string) => ({
  'Authorization': `Bearer ${token}`,
  // Content-Type is handled automatically by FormData
});
