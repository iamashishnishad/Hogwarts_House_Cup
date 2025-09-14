# Hogwarts House Cup Leaderboard

A real-time leaderboard system for tracking house points at Hogwarts School of Witchcraft and Wizardry.

## 🚀 Quick Start (Docker - Recommended)

### Prerequisites
- Docker Desktop installed on your system

### Installation & Running
1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd hogwarts-leaderboard
   ```

2. **Start the application with Docker**
   ```bash
   docker-compose up
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5001

## 🖥️ Manual Installation (Without Docker)

### Backend Setup
1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install flask flask-cors
   ```

3. **Run the backend server**
   ```bash
   python app.py
   ```
   The backend will run on http://localhost:5001

### Frontend Setup
1. **Open a new terminal and navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the frontend development server**
   ```bash
   npm start
   ```
   The frontend will run on http://localhost:3000

## 📁 Project Structure
```
hogwarts-leaderboard/
├── backend/           # Python Flask API
│   ├── app.py        # Main application
│   ├── data_gen.py   # Data generator
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/          # React application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml # Docker configuration
```

## 🛠️ Built With
- **Backend**: Python, Flask, SQLite
- **Frontend**: React.js
- **Containerization**: Docker, Docker Compose

## 📋 Features
- Real-time point updates
- Time-based filtering (5min, 1hr, All-time)
- Live updates toggle
- Responsive design
- House ranking with progress bars

## 🐳 Docker Commands
```bash
# Start application
docker-compose up

# Start in background
docker-compose up -d

# Stop application
docker-compose down

# View logs
docker-compose logs

# Rebuild images
docker-compose up --build
```

## 🌐 API Endpoints
- `GET /api/points?window=all` - Get points by time window
- `GET /api/debug/db` - Database status endpoint

## 📊 Time Windows
- `5min` - Points from last 5 minutes
- `1hour` - Points from last hour  
- `all` - All points (default)

## 🐛 Troubleshooting
- Ensure ports 3000 and 5001 are available
- Verify Docker Desktop is running
- Check `docker-compose logs` for errors


---

