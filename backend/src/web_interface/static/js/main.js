// Global variables
let socket = null;
let cameraFeed = null;
let trafficChart = null;
let signalChart = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Socket.IO connection
    socket = io();
    
    // Get DOM elements
    cameraFeed = document.getElementById('cameraFeed');
    
    // Initialize charts
    initializeCharts();
    
    // Set up event listeners
    setupEventListeners();
    
    // Set up Socket.IO event handlers
    setupSocketHandlers();
});

// Initialize charts
function initializeCharts() {
    // Traffic chart
    const trafficCtx = document.getElementById('trafficChart').getContext('2d');
    trafficChart = new Chart(trafficCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Total Vehicles',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    // Signal chart
    const signalCtx = document.getElementById('signalChart').getContext('2d');
    signalChart = new Chart(signalCtx, {
        type: 'bar',
        data: {
            labels: ['North-South', 'East-West'],
            datasets: [{
                label: 'Green Time (seconds)',
                data: [0, 0],
                backgroundColor: 'rgba(40, 167, 69, 0.5)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Set up event listeners
function setupEventListeners() {
    // Emergency vehicle buttons
    document.getElementById('ambulanceBtn').addEventListener('click', function() {
        socket.emit('emergency_vehicle', { type: 'ambulance' });
        showAlert('Emergency mode activated for ambulance', 'success');
    });
    
    document.getElementById('fireTruckBtn').addEventListener('click', function() {
        socket.emit('emergency_vehicle', { type: 'fire_truck' });
        showAlert('Emergency mode activated for fire truck', 'success');
    });
    
    document.getElementById('policeBtn').addEventListener('click', function() {
        socket.emit('emergency_vehicle', { type: 'police' });
        showAlert('Emergency mode activated for police vehicle', 'success');
    });
    
    // Emergency mode button
    document.getElementById('emergencyBtn').addEventListener('click', function(e) {
        e.preventDefault();
        showEmergencyModal();
    });
}

// Set up Socket.IO event handlers
function setupSocketHandlers() {
    socket.on('connect', function() {
        console.log('Connected to server');
        showAlert('Connected to traffic management system', 'success');
    });
    
    socket.on('disconnect', function() {
        console.log('Disconnected from server');
        showAlert('Disconnected from traffic management system', 'danger');
    });
    
    socket.on('system_update', function(data) {
        updateDashboard(data);
    });
    
    socket.on('error', function(error) {
        console.error('Socket error:', error);
        showAlert('Error: ' + error.message, 'danger');
    });
}

// Update dashboard with new data
function updateDashboard(data) {
    // Update camera feed
    if (data.traffic.frame) {
        cameraFeed.src = 'data:image/jpeg;base64,' + data.traffic.frame;
    }
    
    // Update vehicle counts
    updateVehicleCounts(data.traffic.vehicle_counts);
    
    // Update signal states
    updateSignalStates(data.signals.states);
    
    // Update charts
    updateCharts(data);
}

// Update vehicle counts display
function updateVehicleCounts(counts) {
    const container = document.getElementById('vehicleCounts');
    container.innerHTML = '';
    
    Object.entries(counts).forEach(([lane, count]) => {
        const div = document.createElement('div');
        div.className = 'vehicle-count';
        div.textContent = `${lane}: ${count} vehicles`;
        container.appendChild(div);
    });
}

// Update signal states display
function updateSignalStates(states) {
    const container = document.getElementById('signalStates');
    container.innerHTML = '';
    
    Object.entries(states).forEach(([signal, state]) => {
        const div = document.createElement('div');
        div.className = 'mb-2';
        
        const indicator = document.createElement('span');
        indicator.className = `signal-state ${state}`;
        
        const label = document.createElement('span');
        label.textContent = `${signal}: ${state}`;
        
        div.appendChild(indicator);
        div.appendChild(label);
        container.appendChild(div);
    });
}

// Update charts with new data
function updateCharts(data) {
    // Update traffic chart
    const timestamp = new Date(data.timestamp).toLocaleTimeString();
    const totalVehicles = Object.values(data.traffic.vehicle_counts).reduce((a, b) => a + b, 0);
    
    trafficChart.data.labels.push(timestamp);
    trafficChart.data.datasets[0].data.push(totalVehicles);
    
    // Keep only last 10 data points
    if (trafficChart.data.labels.length > 10) {
        trafficChart.data.labels.shift();
        trafficChart.data.datasets[0].data.shift();
    }
    
    trafficChart.update();
    
    // Update signal chart
    Object.entries(data.signals.timing).forEach(([signal, timing], index) => {
        signalChart.data.datasets[0].data[index] = timing.duration;
    });
    
    signalChart.update();
}

// Show alert message
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.row'));
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Show emergency mode modal
function showEmergencyModal() {
    const modal = new bootstrap.Modal(document.getElementById('emergencyModal'));
    modal.show();
}

// Handle emergency mode confirmation
function confirmEmergencyMode(type) {
    socket.emit('emergency_vehicle', { type: type });
    showAlert(`Emergency mode activated for ${type}`, 'success');
    bootstrap.Modal.getInstance(document.getElementById('emergencyModal')).hide();
} 