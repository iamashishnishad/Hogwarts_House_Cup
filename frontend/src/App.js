import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [points, setPoints] = useState({
    Gryff: 0,
    Slyth: 0,
    Raven: 0,
    Huff: 0
  });
  const [timeWindow, setTimeWindow] = useState('all');
  const [liveUpdates, setLiveUpdates] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(new Date());

  const fetchPoints = async () => {
    try {
      const response = await fetch(`http://localhost:5001/api/points?window=${timeWindow}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setPoints(data);
      setLastUpdated(new Date());
    } catch (error) {
      console.error('Error fetching points:', error);
    }
  };

  useEffect(() => {
    fetchPoints();
    
    if (liveUpdates) {
      const interval = setInterval(fetchPoints, 2000);
      return () => clearInterval(interval);
    }
  }, [timeWindow, liveUpdates]);

  const houses = [
    { 
      name: 'Gryff', 
      fullName: 'Gryffindor',
      symbol: '🦁'
    },
    { 
      name: 'Slyth', 
      fullName: 'Slytherin',
      symbol: '🐍'
    },
    { 
      name: 'Raven', 
      fullName: 'Ravenclaw',
      symbol: '🦅'
    },
    { 
      name: 'Huff', 
      fullName: 'Hufflepuff',
      symbol: '🦡'
    }
  ];

  const sortedHouses = [...houses].sort((a, b) => points[b.name] - points[a.name]);
  const maxPoints = Math.max(...Object.values(points)) || 1;

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  return (
    <div className="App">
      <div className="header-container">
        <header className="App-header">
          <div className="title-container">
            <h1>Hogwarts House Cup</h1>
            <div className="subtitle">Leaderboard</div>
          </div>
          <div className="house-symbols">
            {houses.map(house => (
              <div key={house.name} className="symbol">
                {house.symbol}
              </div>
            ))}
          </div>
        </header>
      </div>
      
      <div className="controls-container">
        <div className="controls">
          <div className="time-windows">
            <h3>Time Period</h3>
            <div className="button-group">
              <button 
                className={timeWindow === '5min' ? 'active' : ''}
                onClick={() => setTimeWindow('5min')}
              >
                5 min
              </button>
              <button 
                className={timeWindow === '1hour' ? 'active' : ''}
                onClick={() => setTimeWindow('1hour')}
              >
                1 hour
              </button>
              <button 
                className={timeWindow === 'all' ? 'active' : ''}
                onClick={() => setTimeWindow('all')}
              >
                All Time
              </button>
            </div>
          </div>
          
          <div className="live-control">
            <h3>Live Updates</h3>
            <button 
              className={liveUpdates ? 'active' : ''}
              onClick={() => setLiveUpdates(!liveUpdates)}
            >
              <span className="status-indicator"></span>
              {liveUpdates ? 'Pause' : 'Resume'}
            </button>
            <div className="last-updated">
              Updated: {formatTime(lastUpdated)}
            </div>
          </div>
        </div>
      </div>
      
      <div className="leaderboard-container">
        <div className="leaderboard-header">
          <div className="header-position">Rank</div>
          <div className="header-house">House</div>
          <div className="header-points">Points</div>
          <div className="header-progress">Progress</div>
        </div>
        
        <div className="leaderboard">
          {sortedHouses.map((house, index) => (
            <div key={house.name} className="house-row">
              <div className="position">
                <div className="position-number">{index + 1}</div>
                {index === 0 && <div className="trophy">🏆</div>}
              </div>
              <div className="house-info">
                <div className="house-name">
                  {house.fullName}
                </div>
                <div className="house-symbol">
                  {house.symbol}
                </div>
              </div>
              <div className="house-points">
                {points[house.name].toLocaleString()}
              </div>
              <div className="house-bar">
                <div 
                  className="bar-fill"
                  style={{
                    width: `${(points[house.name] / maxPoints) * 90}%`
                  }}
                ></div>
                <div className="bar-background"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className="footer">
        <p>Hogwarts School of Witchcraft and Wizardry</p>
      </div>
    </div>
  );
}

export default App;