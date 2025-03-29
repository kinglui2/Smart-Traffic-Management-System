// Connect to WebSocket server
const socket = io();

// Update traffic light display
function updateTrafficLight(laneId, state) {
    const container = document.getElementById(`${laneId.toLowerCase()}-signal`);
    const lights = container.querySelectorAll('.light');
    
    // Reset all lights
    lights.forEach(light => light.classList.remove('active'));
    
    // Activate the correct light
    switch (state) {
        case 'RED':
            lights[0].classList.add('active');
            break;
        case 'YELLOW':
            lights[1].classList.add('active');
            break;
        case 'GREEN':
            lights[2].classList.add('active');
            break;
    }
}

// Update statistics display
function updateStats(laneId, data) {
    const container = document.getElementById(`${laneId.toLowerCase()}-signal`);
    
    // Update car count
    container.querySelector('.car-count').textContent = data.car_count;
    
    // Update congestion level with color coding
    const congestionPercent = Math.round(data.congestion_level * 100);
    const congestionSpan = container.querySelector('.congestion');
    congestionSpan.textContent = `${congestionPercent}%`;
    
    // Apply color classes based on congestion level
    congestionSpan.classList.remove('congestion-low', 'congestion-medium', 'congestion-high');
    if (data.congestion_level < 0.3) {
        congestionSpan.classList.add('congestion-low');
    } else if (data.congestion_level < 0.7) {
        congestionSpan.classList.add('congestion-medium');
    } else {
        congestionSpan.classList.add('congestion-high');
    }
    
    // Update wait time
    container.querySelector('.wait-time').textContent = 
        `${Math.round(data.wait_time)}s`;
}

// Update recommendations
function updateRecommendations(recommendations) {
    const list = document.getElementById('recommendations-list');
    list.innerHTML = '';
    
    if (recommendations.length === 0) {
        const emptyItem = document.createElement('li');
        emptyItem.className = 'list-group-item text-muted';
        emptyItem.textContent = 'No current recommendations';
        list.appendChild(emptyItem);
        return;
    }
    
    recommendations.forEach(rec => {
        const item = document.createElement('li');
        item.className = 'list-group-item recommendation-item';
        item.textContent = rec;
        list.appendChild(item);
    });
}

// Handle incoming traffic updates
socket.on('traffic_update', function(data) {
    // Update each lane's display
    for (const [lane, state] of Object.entries(data.states)) {
        updateTrafficLight(lane, state.state);
        updateStats(lane, state);
    }
    
    // Update recommendations
    updateRecommendations(data.recommendations);
});

// Handle connection status
socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('disconnect', function() {
    console.log('Disconnected from server');
}); 