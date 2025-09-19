// API Types
export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
}

export interface FileAsset {
  id: number
  user: User
  filename: string
  size_bytes: number
  size_mb: number
  size_gb: number
  mime_type: string | null
  sha256: string
  storage_url: string | null
  duplicate_of: {
    id: number
    filename: string
    user: string
    created_at: string
  } | null
  is_duplicate: boolean
  kwh_estimate: number
  co2_g_estimate: number
  impact_score: number
  recommendations: Recommendation[]
  created_at: string
  updated_at: string
}

export interface FileAssetList {
  id: number
  user: string
  filename: string
  size_bytes: number
  size_mb: number
  mime_type: string | null
  is_duplicate: boolean
  impact_score: number
  recommendations_count: number
  created_at: string
}

export interface Recommendation {
  id: number
  kind: string
  kind_display: string
  message: string
  created_at: string
}

export interface AnalyticsSummary {
  total_files: number
  total_size_bytes: number
  total_size_gb: number
  total_co2_saved_g: number
  total_kwh_saved: number
  duplicates_count: number
  duplicates_percentage: number
  average_impact_score: number
  files_this_month: number
  co2_saved_this_month: number
}

export interface FileTypeAnalytics {
  mime_type: string
  count: number
  total_size_bytes: number
  average_impact_score: number
}

export interface ImpactTrend {
  date: string
  files_count: number
  total_co2_g: number
  total_kwh: number
  duplicates_count: number
}

export interface UploadUrlResponse {
  upload_url: string
  bucket: string
  key: string
  expires_in: number
}

export interface DownloadUrlResponse {
  download_url: string
  expires_in: number
  filename: string
}

export interface CommitUploadResponse {
  message: string
  task_id: string
  filename: string
  size_bytes: number
}

// Auth Types
export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access: string
  refresh: string
}

export interface RefreshResponse {
  access: string
  refresh?: string
}

// Pagination Types
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// Upload Types
export interface FileUploadData {
  file: File
  filename: string
  contentType: string
}

export interface UploadProgress {
  filename: string
  progress: number
  status: 'uploading' | 'processing' | 'complete' | 'error'
  error?: string
}