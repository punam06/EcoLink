import React, { createContext, useContext, useState, useEffect } from 'react'
import type { ReactNode } from 'react'
import { authAPI } from '../api/client'
import type { LoginRequest, LoginResponse } from '../types/api'

interface RegisterRequest {
  username: string
  email: string
  firstName: string
  lastName: string
  password: string
}

interface AuthContextType {
  isAuthenticated: boolean
  user: { username: string } | null
  login: (credentials: LoginRequest) => Promise<void>
  register: (data: RegisterRequest) => Promise<void>
  logout: () => void
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false)
  const [user, setUser] = useState<{ username: string } | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(true)

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('access_token')
    const username = localStorage.getItem('username')
    
    if (token && username) {
      setIsAuthenticated(true)
      setUser({ username })
    }
    
    setIsLoading(false)
  }, [])

  const login = async (credentials: LoginRequest): Promise<void> => {
    try {
      const response: LoginResponse = await authAPI.login(credentials.username, credentials.password)
      
      localStorage.setItem('access_token', response.access)
      localStorage.setItem('refresh_token', response.refresh)
      localStorage.setItem('username', credentials.username)
      
      setIsAuthenticated(true)
      setUser({ username: credentials.username })
    } catch (error) {
      throw error
    }
  }

  const register = async (data: RegisterRequest): Promise<void> => {
    try {
      // For demo purposes, simulate a successful registration
      // In real implementation, this would make an API call
      await new Promise((resolve) => setTimeout(resolve, 1000))
      
      // Simulate successful registration response
      console.log('Registration successful for:', data.username)
    } catch (error) {
      throw error
    }
  }

  const logout = (): void => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('username')
    
    setIsAuthenticated(false)
    setUser(null)
  }

  const value: AuthContextType = {
    isAuthenticated,
    user,
    login,
    register,
    logout,
    isLoading,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}