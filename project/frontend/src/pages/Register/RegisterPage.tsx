import React from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import {
  Container,
  Paper,
  Box,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Divider,
} from '@mui/material'
import { useAuth } from '../../contexts/AuthContext'

const registerSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Please enter a valid email address'),
  firstName: z.string().min(1, 'First name is required'),
  lastName: z.string().min(1, 'Last name is required'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
  confirmPassword: z.string().min(6, 'Please confirm your password'),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

type RegisterFormData = z.infer<typeof registerSchema>

const RegisterPage: React.FC = () => {
  const navigate = useNavigate()
  const { register: registerUser } = useAuth()
  const [error, setError] = React.useState<string | null>(null)
  const [isLoading, setIsLoading] = React.useState(false)
  const [success, setSuccess] = React.useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  })

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true)
    setError(null)

    try {
      // Remove confirmPassword before sending to API
      const { confirmPassword, ...registerData } = data
      await registerUser(registerData)
      setSuccess(true)
      setTimeout(() => {
        navigate('/login')
      }, 2000)
    } catch (err: any) {
      if (err.response?.status === 400) {
        setError('Username or email already exists')
      } else {
        setError('An error occurred during registration. Please try again.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  if (success) {
    return (
      <Container component="main" maxWidth="md">
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Paper elevation={3} sx={{ padding: 6, width: '100%', textAlign: 'center' }}>
            <Typography
              component="h1"
              variant="h4"
              sx={{ mb: 2, color: 'green', fontWeight: 'bold' }}
            >
              🌱 Registration Successful!
            </Typography>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Welcome to EcoLink!
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Your account has been created successfully. Redirecting to login page...
            </Typography>
          </Paper>
        </Box>
      </Container>
    )
  }

  return (
    <Container component="main" maxWidth="md">
      <Box
        sx={{
          marginTop: 6,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper elevation={3} sx={{ padding: 6, width: '100%' }}>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography
              component="h1"
              variant="h4"
              sx={{ mb: 2, color: 'green', fontWeight: 'bold' }}
            >
              🌱 EcoLink
            </Typography>
            <Typography component="h2" variant="h5" sx={{ mb: 4 }}>
              Create Your Account
            </Typography>
            
            {error && (
              <Alert severity="error" sx={{ width: '100%', mb: 3 }}>
                {error}
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ width: '100%' }}>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                <Box sx={{ flex: '1 1 calc(50% - 8px)', minWidth: '250px' }}>
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="firstName"
                    label="First Name"
                    autoComplete="given-name"
                    autoFocus
                    error={!!errors.firstName}
                    helperText={errors.firstName?.message}
                    {...register('firstName')}
                  />
                </Box>
                <Box sx={{ flex: '1 1 calc(50% - 8px)', minWidth: '250px' }}>
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="lastName"
                    label="Last Name"
                    autoComplete="family-name"
                    error={!!errors.lastName}
                    helperText={errors.lastName?.message}
                    {...register('lastName')}
                  />
                </Box>
                <Box sx={{ flex: '1 1 calc(50% - 8px)', minWidth: '250px' }}>
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="username"
                    label="Username"
                    autoComplete="username"
                    error={!!errors.username}
                    helperText={errors.username?.message}
                    {...register('username')}
                  />
                </Box>
                <Box sx={{ flex: '1 1 calc(50% - 8px)', minWidth: '250px' }}>
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="email"
                    label="Email Address"
                    type="email"
                    autoComplete="email"
                    error={!!errors.email}
                    helperText={errors.email?.message}
                    {...register('email')}
                  />
                </Box>
                <Box sx={{ flex: '1 1 calc(50% - 8px)', minWidth: '250px' }}>
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="new-password"
                    error={!!errors.password}
                    helperText={errors.password?.message}
                    {...register('password')}
                  />
                </Box>
                <Box sx={{ flex: '1 1 calc(50% - 8px)', minWidth: '250px' }}>
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    label="Confirm Password"
                    type="password"
                    id="confirmPassword"
                    autoComplete="new-password"
                    error={!!errors.confirmPassword}
                    helperText={errors.confirmPassword?.message}
                    {...register('confirmPassword')}
                  />
                </Box>
              </Box>
              
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 4, mb: 2, py: 1.5 }}
                disabled={isLoading}
                startIcon={isLoading ? <CircularProgress size={20} /> : null}
              >
                {isLoading ? 'Creating Account...' : 'Create Account'}
              </Button>
              
              <Divider sx={{ my: 3 }} />
              
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="body2">
                  Already have an account?{' '}
                  <Link 
                    to="/login" 
                    style={{ 
                      color: '#2e7d32', 
                      textDecoration: 'none',
                      fontWeight: 'bold'
                    }}
                  >
                    Sign in here
                  </Link>
                </Typography>
              </Box>
            </Box>
          </Box>
        </Paper>

        <Box sx={{ mt: 4, textAlign: 'center', maxWidth: 600 }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            🌍 Join EcoLink and start managing your files sustainably
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Detect duplicates • Measure environmental impact • Reduce your digital carbon footprint
          </Typography>
        </Box>
      </Box>
    </Container>
  )
}

export default RegisterPage