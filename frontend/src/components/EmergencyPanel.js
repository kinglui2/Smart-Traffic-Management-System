import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  Grid,
  Fade,
  useTheme,
} from '@mui/material';
import {
  LocalHospital,
  LocalFireDepartment,
  LocalPolice,
  Warning,
} from '@mui/icons-material';

const EmergencyButton = ({ icon: Icon, label, color, onClick }) => {
  const theme = useTheme();
  
  return (
    <Button
      variant="contained"
      color={color}
      startIcon={<Icon />}
      onClick={onClick}
      fullWidth
      sx={{
        py: 2,
        borderRadius: 2,
        backgroundColor: theme.palette.mode === 'dark' 
          ? `${color}.dark`
          : `${color}.main`,
        '&:hover': {
          backgroundColor: theme.palette.mode === 'dark'
            ? `${color}.main`
            : `${color}.dark`,
        },
      }}
    >
      {label}
    </Button>
  );
};

const EmergencyPanel = () => {
  const [open, setOpen] = useState(false);
  const [selectedEmergency, setSelectedEmergency] = useState(null);
  const [emergencyActive, setEmergencyActive] = useState(false);

  const handleEmergencyClick = (type) => {
    setSelectedEmergency(type);
    setOpen(true);
  };

  const handleConfirm = () => {
    setEmergencyActive(true);
    setOpen(false);
    // Here you would also emit the emergency event to the backend
  };

  const handleCancel = () => {
    setSelectedEmergency(null);
    setOpen(false);
  };

  const handleEmergencyToggle = () => {
    // TODO: Implement emergency mode toggle logic
    setEmergencyActive(!emergencyActive);
  };

  const emergencyTypes = [
    {
      icon: LocalHospital,
      label: 'Ambulance',
      color: 'error',
      description: 'Priority route for medical emergency',
    },
    {
      icon: LocalFireDepartment,
      label: 'Fire Truck',
      color: 'warning',
      description: 'Clear path for fire emergency',
    },
    {
      icon: LocalPolice,
      label: 'Police',
      color: 'info',
      description: 'Emergency police response',
    },
  ];

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Emergency Controls
      </Typography>

      {emergencyActive && (
        <Fade in>
          <Alert
            severity="error"
            icon={<Warning />}
            sx={{ mb: 2 }}
            onClose={() => setEmergencyActive(false)}
          >
            Emergency mode is active - All signals will be optimized for emergency vehicle passage
          </Alert>
        </Fade>
      )}

      <Grid container spacing={2}>
        {emergencyTypes.map((type) => (
          <Grid item xs={12} key={type.label}>
            <EmergencyButton
              icon={type.icon}
              label={type.label}
              color={type.color}
              onClick={() => handleEmergencyClick(type)}
            />
          </Grid>
        ))}
      </Grid>

      <Dialog
        open={open}
        onClose={handleCancel}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {selectedEmergency?.label} Emergency Mode
        </DialogTitle>
        <DialogContent>
          <Typography>
            Activating emergency mode will:
          </Typography>
          <Box component="ul" sx={{ mt: 1 }}>
            <li>Override normal traffic signal patterns</li>
            <li>Optimize route for emergency vehicle</li>
            <li>Alert nearby vehicles through the system</li>
          </Box>
          <Typography color="error" sx={{ mt: 2 }}>
            Please confirm to activate emergency mode
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCancel}>
            Cancel
          </Button>
          <Button
            variant="contained"
            color="error"
            onClick={handleConfirm}
            startIcon={<Warning />}
          >
            Activate Emergency Mode
          </Button>
        </DialogActions>
      </Dialog>

      <Button
        variant="contained"
        color={emergencyActive ? "error" : "primary"}
        fullWidth
        onClick={handleEmergencyToggle}
      >
        {emergencyActive ? "Deactivate Emergency Mode" : "Activate Emergency Mode"}
      </Button>
    </Box>
  );
};

export default EmergencyPanel; 