import React from 'react'
import {
  Typography,
  Box,
} from '@mui/material'

const FilesPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        My Files
      </Typography>
      <Typography>
        View and manage your uploaded files, duplicates, and environmental impact metrics.
      </Typography>
    </Box>
  )
}

export default FilesPage