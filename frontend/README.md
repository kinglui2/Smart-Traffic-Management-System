# Smart Traffic Management System - Frontend

This is the frontend application for the Smart Traffic Management System. It's built with React and Material-UI, providing a modern and responsive interface for traffic monitoring and control.

## Features

- Real-time traffic monitoring
- Vehicle statistics and analytics
- Emergency vehicle controls
- Traffic signal management
- Dark/Light mode support
- Responsive design for all devices
- Interactive charts and visualizations

## Prerequisites

- Node.js 18 or higher
- npm or yarn
- Backend server running (see main project README)

## Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the root directory:
```env
REACT_APP_BACKEND_URL=http://localhost:5000
```

3. Start the development server:
```bash
npm start
```

## Building for Production

```bash
npm run build
```

## Deployment on Netlify

1. Fork or clone this repository

2. Connect your GitHub repository to Netlify:
   - Log in to Netlify
   - Click "New site from Git"
   - Choose your repository
   - Select the `frontend` directory as the base directory
   - Set the build command to `npm run build`
   - Set the publish directory to `build`

3. Configure environment variables in Netlify:
   - Go to Site settings > Build & deploy > Environment
   - Add the following variables:
     - `REACT_APP_BACKEND_URL`: Your backend server URL

4. Deploy:
   - Netlify will automatically build and deploy your site
   - Any push to the main branch will trigger a new deployment

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── TrafficCamera.js
│   │   ├── VehicleStats.js
│   │   ├── SignalControls.js
│   │   ├── EmergencyPanel.js
│   │   └── TrafficAnalytics.js
│   ├── App.js
│   └── index.js
├── public/
├── package.json
└── netlify.toml
```

## Environment Variables

- `REACT_APP_BACKEND_URL`: URL of the backend server
  - Development: http://localhost:5000
  - Production: Your deployed backend URL

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 