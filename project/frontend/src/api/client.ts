import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
            refresh: refreshToken,
          })
          
          const { access, refresh } = response.data
          localStorage.setItem('access_token', access)
          if (refresh) {
            localStorage.setItem('refresh_token', refresh)
          }
          
          originalRequest.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
        } catch (refreshError) {
          // Refresh failed, redirect to login
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
          return Promise.reject(refreshError)
        }
      }
    }
    
    return Promise.reject(error)
  }
)

export default api

// Auth API functions
export const authAPI = {
  login: async (username: string, password: string) => {
    const response = await api.post('/auth/login/', { username, password })
    return response.data
  },
  
  refresh: async (refreshToken: string) => {
    const response = await api.post('/auth/refresh/', { refresh: refreshToken })
    return response.data
  },
}

// Files API functions
export const filesAPI = {
  getFiles: async (page?: number) => {
    const response = await api.get(`/v1/files/`, { params: { page } })
    return response.data
  },
  
  getFile: async (id: number) => {
    const response = await api.get(`/v1/files/${id}/`)
    return response.data
  },
  
  requestUploadUrl: async (filename: string, contentType?: string) => {
    const response = await api.post('/v1/files/request-upload-url/', {
      filename,
      content_type: contentType,
    })
    return response.data
  },
  
  commitUpload: async (data: {
    bucket: string
    key: string
    filename: string
    size_bytes: number
  }) => {
    const response = await api.post('/v1/files/commit/', data)
    return response.data
  },
  
  getDownloadUrl: async (id: number) => {
    const response = await api.get(`/v1/files/${id}/download-url/`)
    return response.data
  },
}

// Analytics API functions
export const analyticsAPI = {
  getSummary: async () => {
    const response = await api.get('/v1/analytics/summary/')
    return response.data
  },
  
  getFileTypes: async () => {
    const response = await api.get('/v1/analytics/file-types/')
    return response.data
  },
  
  getImpactTrend: async (days?: number) => {
    const response = await api.get('/v1/analytics/impact-trend/', {
      params: { days }
    })
    return response.data
  },
}

// Recommendations API functions
export const recommendationsAPI = {
  getRecommendations: async (page?: number) => {
    const response = await api.get('/v1/recommendations/', { params: { page } })
    return response.data
  },
}