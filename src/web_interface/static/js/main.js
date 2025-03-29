// Connect to WebSocket server
const socket = io();

// Track connection state
let isConnected = false;

// Update loading state
function setLoading(loading) {
    document.querySelectorAll('.signal-box').forEach(box => {
        box.classList.toggle('loading', loading);
    });
    document.getElementById('recommendations-list').classList.toggle('loading', loading);
}

// Update traffic signal state
function updateSignalState(state, elapsed, total) {
    const signalElement = document.getElementById('signal-state');
    signalElement.className = 'signal-state ' + state;
    
    // Update timing info
    document.getElementById('signal-elapsed').textContent = Math.round(elapsed);
    document.getElementById('signal-total').textContent = Math.round(total);
    
    // Update progress bar
    const progress = (elapsed / total) * 100;
    document.getElementById('signal-progress').style.width = `${progress}%`;
}

// Update lane information
function updateLaneInfo(laneId, data) {
    const laneElement = document.getElementById(`lane-${laneId}`);
    if (!laneElement) return;
    
    // Update car count
    const carsElement = laneElement.querySelector('.cars-count');
    carsElement.textContent = data.cars;
    
    // Update wait time
    const waitElement = laneElement.querySelector('.wait-time');
    waitElement.textContent = Math.round(data.wait_time);
    
    // Update congestion level
    const congestionLevel = data.cars < 5 ? 'low' : data.cars < 10 ? 'medium' : 'high';
    laneElement.className = `lane-box ${congestionLevel}`;
}

// Update recommendations
function updateRecommendations(recommendations) {
    const recommendationsList = document.getElementById('recommendations-list');
    recommendationsList.innerHTML = '';
    
    recommendations.forEach(rec => {
        const div = document.createElement('div');
        div.className = `recommendation-item ${rec.severity}`;
        div.innerHTML = `<p>${rec.message}</p>`;
        recommendationsList.appendChild(div);
    });
}

// Update timestamp
function updateTimestamp(timestamp) {
    const date = new Date(timestamp);
    document.getElementById('last-update').textContent = 
        date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

// Handle incoming traffic updates
socket.on('traffic_update', (data) => {
    if (!isConnected) {
        isConnected = true;
        setLoading(false);
    }
    
    // Update signal state
    updateSignalState(
        data.signal_state.state,
        data.signal_state.elapsed_time,
        data.signal_state.total_duration
    );
    
    // Update all lane information
    Object.entries(data.lanes).forEach(([laneId, laneData]) => {
        updateLaneInfo(laneId, laneData);
    });
    
    // Update recommendations
    updateRecommendations(data.recommendations);
    
    // Update timestamp
    if (data.timestamp) {
        updateTimestamp(data.timestamp);
    }
});

// Handle connection status
socket.on('connect', () => {
    console.log('Connected to server');
    isConnected = true;
    setLoading(false);
    document.getElementById('connection-status').textContent = 'Connected';
    document.getElementById('connection-status').className = 'connected';
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    isConnected = false;
    setLoading(true);
    document.getElementById('connection-status').textContent = 'Disconnected';
    document.getElementById('connection-status').className = 'disconnected';
});

socket.on('error', (error) => {
    console.error('Socket error:', error);
    document.getElementById('error-message').textContent = error.message;
    document.getElementById('error-message').style.display = 'block';
    setTimeout(() => {
        document.getElementById('error-message').style.display = 'none';
    }, 5000);
});

// Initialize loading state
setLoading(true);

// Add smooth scrolling for recommendations
document.getElementById('recommendations-list').addEventListener('scroll', (e) => {
    e.target.style.scrollBehavior = 'smooth';
}); 