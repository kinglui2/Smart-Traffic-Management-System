import React from 'react';
import { Box, Typography, Grid, Button } from '@mui/material';

const SignalControls = ({ data }) => {
  const handleSignalChange = (intersection, color) => {
    // TODO: Implement signal change logic
    console.log(`Changing signal at ${intersection} to ${color}`);
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Traffic Signal Controls
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Typography variant="subtitle1" gutterBottom>
            Main Intersection
          </Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              variant="contained"
              color="success"
              onClick={() => handleSignalChange('main', 'green')}
            >
              Green
            </Button>
            <Button
              variant="contained"
              color="warning"
              onClick={() => handleSignalChange('main', 'yellow')}
            >
              Yellow
            </Button>
            <Button
              variant="contained"
              color="error"
              onClick={() => handleSignalChange('main', 'red')}
            >
              Red
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SignalControls; 