import React, { useState, useEffect } from 'react';
import {
  CssBaseline,
  ThemeProvider,
  createTheme,
  Box,
  AppBar,
  Toolbar,
  Typography,
  Container,
  Grid,
  Paper,
  IconButton,
  useMediaQuery,
} from '@mui/material';
import {
  Brightness4,
  Brightness7,
  Traffic,
  Warning,
} from '@mui/icons-material';
import { io } from 'socket.io-client';

// Components
import TrafficCamera from './components/TrafficCamera';
import VehicleStats from './components/VehicleStats';
import SignalControls from './components/SignalControls';
import EmergencyPanel from './components/EmergencyPanel';
import TrafficAnalytics from './components/TrafficAnalytics';
import TrafficMap from './components/TrafficMap';

// Create theme
const getTheme = (mode) =>
  createTheme({
    palette: {
      mode,
      primary: {
        main: '#1976d2',
      },
      secondary: {
        main: '#dc004e',
      },
      background: {
        default: mode === 'dark' ? '#121212' : '#f5f5f5',
        paper: mode === 'dark' ? '#1e1e1e' : '#ffffff',
      },
    },
    components: {
      MuiPaper: {
        styleOverrides: {
          root: {
            borderRadius: 12,
            boxShadow: mode === 'dark' 
              ? '0 4px 6px rgba(0, 0, 0, 0.4)'
              : '0 4px 6px rgba(0, 0, 0, 0.1)',
          },
        },
      },
    },
  });

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [trafficData, setTrafficData] = useState({
    vehicleCounts: {},
    signalStates: {},
    emergencyMode: false,
  });
  
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const theme = React.useMemo(
    () => getTheme(darkMode ? 'dark' : 'light'),
    [darkMode]
  );

  useEffect(() => {
    setDarkMode(prefersDarkMode);
  }, [prefersDarkMode]);

  useEffect(() => {
    const socket = io(process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000');
    
    socket.on('system_update', (data) => {
      setTrafficData(data);
    });

    return () => socket.disconnect();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <AppBar position="sticky" elevation={0}>
          <Toolbar>
            <Traffic sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Smart Traffic Management
            </Typography>
            {trafficData.emergencyMode && (
              <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
                <Warning color="error" sx={{ mr: 1 }} />
                <Typography variant="body2" color="error">
                  Emergency Mode Active
                </Typography>
              </Box>
            )}
            <IconButton onClick={() => setDarkMode(!darkMode)} color="inherit">
              {darkMode ? <Brightness7 /> : <Brightness4 />}
            </IconButton>
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl" sx={{ mt: 4, mb: 4, flex: 1 }}>
          <Grid container spacing={3}>
            {/* Main content area */}
            <Grid item xs={12} lg={8}>
              <Paper sx={{ p: 2, mb: 3 }}>
                <TrafficCamera data={trafficData} />
              </Paper>
              <Paper sx={{ p: 2 }}>
                <TrafficAnalytics data={trafficData} />
              </Paper>
            </Grid>

            {/* Sidebar */}
            <Grid item xs={12} lg={4}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Paper sx={{ p: 2 }}>
                    <VehicleStats data={trafficData} />
                  </Paper>
                </Grid>
                <Grid item xs={12}>
                  <Paper sx={{ p: 2 }}>
                    <SignalControls data={trafficData} />
                  </Paper>
                </Grid>
                <Grid item xs={12}>
                  <Paper sx={{ p: 2 }}>
                    <EmergencyPanel />
                  </Paper>
                </Grid>
                <Grid item xs={12}>
                  <Paper sx={{ p: 2 }}>
                    <TrafficMap data={trafficData} />
                  </Paper>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Container>

        <Box
          component="footer"
          sx={{
            py: 3,
            px: 2,
            mt: 'auto',
            backgroundColor: theme.palette.background.paper,
          }}
        >
          <Container maxWidth="sm">
            <Typography variant="body2" color="text.secondary" align="center">
              © {new Date().getFullYear()} Smart Traffic Management System
            </Typography>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App; 