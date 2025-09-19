import React from 'react'
import {
  Typography,
  Box,
} from '@mui/material'

const UploadPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Upload Files
      </Typography>
      <Typography>
        Drag and drop files here to upload them with environmental impact analysis.
      </Typography>
    </Box>
  )
}

export default UploadPage