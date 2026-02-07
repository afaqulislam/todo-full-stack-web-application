// API Configuration with validation
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

if (!API_BASE_URL) {
  console.warn('NEXT_PUBLIC_API_BASE_URL is not defined. Using default value.');
}

const BASE_URL = API_BASE_URL || 'http://localhost:8000';

// Ensure URL has proper format
const normalizeUrl = (url: string): string => {
  // Remove trailing slashes
  let normalized = url.endsWith('/') ? url.slice(0, -1) : url;
  // Ensure it starts with http:// or https://
  if (!normalized.startsWith('http://') && !normalized.startsWith('https://')) {
    normalized = 'http://' + normalized;
  }
  return normalized;
};

const normalizedBaseUrl = normalizeUrl(BASE_URL);

export const apiConfig = {
  baseUrl: normalizedBaseUrl,
  endpoints: {
    auth: {
      login: `${normalizedBaseUrl}/api/v1/auth/login`,
      register: `${normalizedBaseUrl}/api/v1/auth/register`,
      me: `${normalizedBaseUrl}/api/v1/auth/me`,
      logout: `${normalizedBaseUrl}/api/v1/auth/logout`,
    },
    todos: {
      base: `${normalizedBaseUrl}/api/v1/todos/`,
      getById: (id: string) => `${normalizedBaseUrl}/api/v1/todos/${id}`,
      toggle: (id: string) => `${normalizedBaseUrl}/api/v1/todos/${id}/toggle`,
    },
  },
};