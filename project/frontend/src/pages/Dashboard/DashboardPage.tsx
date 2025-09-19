import React from 'react'
import {
  Typography,
  Box,
} from '@mui/material'

const DashboardPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Typography>
        Welcome to EcoLink! Your environmental impact dashboard will be displayed here.
      </Typography>
    </Box>
  )
}

export default DashboardPage