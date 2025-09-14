
# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime, timedelta, timezone
import threading
from data_gen import record_stream
import os

app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize database
def init_db():
    # Get the absolute path to the database file
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hogwarts.db')
    print(f"Database path: {db_path}")
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS house_points (
            id TEXT PRIMARY KEY,
            category TEXT,
            points INTEGER,
            timestamp DATETIME
        )
    ''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_category ON house_points (category)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON house_points (timestamp)')
    conn.commit()
    conn.close()
    print("Database initialized successfully")

# Modified ingest_event function with better error handling
def ingest_event(event):
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hogwarts.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO house_points (id, category, points, timestamp) VALUES (?, ?, ?, ?)",
            (event['id'], event['category'], event['points'], event['timestamp'])
        )
        conn.commit()
        conn.close()
        print(f"Ingested event: {event['category']} - {event['points']} points")
    except Exception as e:
        print(f"Error ingesting event: {e}")

@app.route('/api/points', methods=['GET'])
def get_points():
    try:
        time_window = request.args.get('window', 'all')
        
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hogwarts.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        if time_window == 'all':
            c.execute("SELECT category, SUM(points) FROM house_points GROUP BY category")
        else:
            now = datetime.now(timezone.utc)
            if time_window == '5min':
                start_time = now - timedelta(minutes=5)
            else:  # 1hour
                start_time = now - timedelta(hours=1)
            
            start_time_str = start_time.isoformat()
            c.execute(
                "SELECT category, SUM(points) FROM house_points WHERE timestamp >= ? GROUP BY category",
                (start_time_str,)
            )
        
        results = c.fetchall()
        conn.close()
        
        points = {category: 0 for category in ["Gryff", "Slyth", "Raven", "Huff"]}
        for category, total in results:
            if category in points and total is not None:
                points[category] = total
        
        return jsonify(points)
    except Exception as e:
        print(f"Error in get_points: {e}")
        return jsonify({"error": str(e)}), 500

# Background thread to ingest events from the generator
def ingest_events():
    print("Starting event ingestion thread...")
    event_count = 0
    for event in record_stream():
        ingest_event(event)
        event_count += 1
        if event_count % 10 == 0:
            print(f"Ingested {event_count} events so far...")

# Initialize database when the app starts
init_db()

# Start the ingestion thread
ingestion_thread = threading.Thread(target=ingest_events, daemon=True)
ingestion_thread.start()

@app.route('/api/debug/db', methods=['GET'])
def debug_db():
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hogwarts.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Check if table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='house_points'")
        table_exists = c.fetchone() is not None
        
        if not table_exists:
            conn.close()
            return jsonify({"error": "house_points table does not exist"})
        
        # Get database info
        c.execute("SELECT COUNT(*) FROM house_points")
        total_count = c.fetchone()[0]
        
        c.execute("SELECT category, COUNT(*), SUM(points) FROM house_points GROUP BY category")
        by_category = []
        for category, count, points in c.fetchall():
            by_category.append({
                'category': category,
                'count': count,
                'points': points or 0
            })
        
        conn.close()
        
        return jsonify({
            'table_exists': table_exists,
            'total_records': total_count,
            'by_category': by_category,
            'database_file': db_path
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, port=5001, host='0.0.0.0')