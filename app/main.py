"""
FastAPI Backend - Real-Time News & Events Monitoring System
============================================================

Purpose:
    REST API backend that serves event data from SQLite database.
    Provides endpoints for querying events, statistics, and city information.

Endpoints:
    GET /                 - Frontend dashboard (HTML)
    GET /events          - Get all events with optional filters
    GET /stats           - Get event count statistics by category
    GET /cities          - Get cities with event counts
    GET /docs            - Swagger API documentation

Usage:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import Optional, List, Dict
import os
from pathlib import Path

# ============================================================================
# APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Real-Time News & Events Monitoring API",
    description="Monitor utility disruption events across Indian cities",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_PATH = BASE_DIR / "app" / "templates" / "index.html"
DATABASE_PATH = BASE_DIR / "db" / "events.db"

# Mount static files directory for CSS
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

def get_db_connection():
    """
    Create and return a SQLite database connection.
    
    Returns:
        sqlite3.Connection: Database connection object
        
    Note:
        Using Row factory allows accessing columns by name (dict-like)
    """
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve the frontend dashboard HTML page.
    
    Returns:
        HTML content of the dashboard
    """
    try:
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Dashboard not found</h1>",
            status_code=404
        )


@app.get("/events")
async def get_events(
    city: Optional[str] = Query(None, description="Filter by city name"),
    category: Optional[str] = Query(None, description="Filter by category")
) -> List[Dict]:
    """
    Get all events with optional filtering by city and/or category.
    
    Args:
        city: Optional city filter (e.g., "Delhi", "Mumbai")
        category: Optional category filter (e.g., "power_outage", "water_issue")
        
    Returns:
        List of event dictionaries with fields:
            - id: Event ID
            - title: News article title
            - city: Detected city
            - date: Publication date
            - category: Event category
            - source: Source URL
            
    Examples:
        GET /events
        GET /events?city=Delhi
        GET /events?category=power_outage
        GET /events?city=Mumbai&category=water_issue
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build dynamic SQL query based on filters
    query = "SELECT id, title, city, date, category, source FROM events"
    params = []
    conditions = []
    
    if city:
        conditions.append("city = ?")
        params.append(city)
    
    if category:
        conditions.append("category = ?")
        params.append(category)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    # Order by date (most recent first)
    query += " ORDER BY date DESC"
    
    # Execute query
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    # Convert to list of dictionaries
    events = [
        {
            "id": row["id"],
            "title": row["title"],
            "city": row["city"],
            "date": row["date"],
            "category": row["category"],
            "source": row["source"]
        }
        for row in rows
    ]
    
    conn.close()
    return events


@app.get("/stats")
async def get_stats() -> Dict[str, int]:
    """
    Get event count statistics grouped by category.
    
    Returns:
        Dictionary with category names as keys and counts as values
        
    Example response:
        {
            "power_outage": 15,
            "water_issue": 8,
            "logistics_delay": 12
        }
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to count events by category
    cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM events
        GROUP BY category
    """)
    
    rows = cursor.fetchall()
    
    # Convert to dictionary
    stats = {row["category"]: row["count"] for row in rows}
    
    conn.close()
    return stats


@app.get("/cities")
async def get_cities() -> List[Dict]:
    """
    Get list of cities with their event counts.
    
    Returns:
        List of dictionaries with city and count
        Sorted by count (descending)
        
    Example response:
        [
            {"city": "Delhi", "count": 10},
            {"city": "Mumbai", "count": 8},
            {"city": "Bengaluru", "count": 5}
        ]
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to count events by city
    cursor.execute("""
        SELECT city, COUNT(*) as count
        FROM events
        GROUP BY city
        ORDER BY count DESC
    """)
    
    rows = cursor.fetchall()
    
    # Convert to list of dictionaries
    cities = [
        {"city": row["city"], "count": row["count"]}
        for row in rows
    ]
    
    conn.close()
    return cities


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Simple health check endpoint.
    
    Returns:
        Status message
    """
    # Check if database exists
    db_exists = DATABASE_PATH.exists()
    
    return {
        "status": "healthy" if db_exists else "database_not_found",
        "database": str(DATABASE_PATH),
        "database_exists": db_exists
    }


# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts.
    Prints helpful information for developers.
    """
    print("\n" + "="*70)
    print("🚀 Real-Time News & Events Monitoring API")
    print("="*70)
    print(f"Dashboard:       http://localhost:8000")
    print(f"API Docs:        http://localhost:8000/docs")
    print(f"Events Endpoint: http://localhost:8000/events")
    print(f"Stats Endpoint:  http://localhost:8000/stats")
    print(f"Cities Endpoint: http://localhost:8000/cities")
    print("="*70 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
