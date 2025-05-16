import React from 'react';
import { Box, Typography } from '@mui/material';

const TrafficMap = ({ data }) => {
  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Traffic Map
      </Typography>
      <Box
        sx={{
          width: '100%',
          height: 300,
          backgroundColor: 'grey.100',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Typography variant="body1" color="text.secondary">
          Map View Placeholder
        </Typography>
      </Box>
    </Box>
  );
};

export default TrafficMap; 