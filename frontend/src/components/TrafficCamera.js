import React from 'react';
import {
  Box,
  Typography,
  IconButton,
  Grid,
  Chip,
  useTheme,
} from '@mui/material';
import {
  Fullscreen,
  FullscreenExit,
  Camera,
  DirectionsCar,
} from '@mui/icons-material';

const TrafficCamera = ({ data }) => {
  const [isFullscreen, setIsFullscreen] = React.useState(false);
  const theme = useTheme();

  const handleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  return (
    <Box>
      <Grid container spacing={2} alignItems="center" sx={{ mb: 2 }}>
        <Grid item>
          <Camera color="primary" />
        </Grid>
        <Grid item xs>
          <Typography variant="h6">Live Traffic Feed</Typography>
        </Grid>
        <Grid item>
          <IconButton onClick={handleFullscreen}>
            {isFullscreen ? <FullscreenExit /> : <Fullscreen />}
          </IconButton>
        </Grid>
      </Grid>

      <Box
        sx={{
          position: 'relative',
          width: '100%',
          paddingTop: '56.25%', // 16:9 aspect ratio
          backgroundColor: theme.palette.background.default,
          borderRadius: 1,
          overflow: 'hidden',
        }}
      >
        <Box
          component="img"
          src={data.cameraFeed || '/placeholder-camera.jpg'}
          alt="Traffic Camera Feed"
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
        
        {/* Overlay with real-time stats */}
        <Box
          sx={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            p: 2,
            background: 'linear-gradient(transparent, rgba(0,0,0,0.7))',
            color: 'white',
          }}
        >
          <Grid container spacing={1}>
            <Grid item>
              <Chip
                icon={<DirectionsCar sx={{ color: 'white' }} />}
                label={`${data.vehicleCounts?.total || 0} Vehicles`}
                sx={{
                  backgroundColor: 'rgba(0,0,0,0.5)',
                  color: 'white',
                }}
              />
            </Grid>
            {data.signalStates && Object.entries(data.signalStates).map(([direction, state]) => (
              <Grid item key={direction}>
                <Chip
                  label={`${direction}: ${state}`}
                  sx={{
                    backgroundColor: (() => {
                      switch (state) {
                        case 'RED': return 'rgba(244,67,54,0.8)';
                        case 'GREEN': return 'rgba(76,175,80,0.8)';
                        case 'YELLOW': return 'rgba(255,193,7,0.8)';
                        default: return 'rgba(0,0,0,0.5)';
                      }
                    })(),
                    color: 'white',
                  }}
                />
              </Grid>
            ))}
          </Grid>
        </Box>
      </Box>
    </Box>
  );
};

export default TrafficCamera; 