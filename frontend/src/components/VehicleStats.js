import React from 'react';
import { Box, Typography, Grid } from '@mui/material';

const VehicleStats = ({ data }) => {
  const stats = data?.vehicleCounts || {
    cars: 0,
    trucks: 0,
    motorcycles: 0,
    buses: 0,
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Vehicle Statistics
      </Typography>
      <Grid container spacing={2}>
        {Object.entries(stats).map(([vehicle, count]) => (
          <Grid item xs={6} key={vehicle}>
            <Typography variant="subtitle1" sx={{ textTransform: 'capitalize' }}>
              {vehicle}
            </Typography>
            <Typography variant="h4">{count}</Typography>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default VehicleStats; 