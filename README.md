# 🔔 Real-Time News & Events Monitoring System

**A complete end-to-end system for monitoring and classifying utility disruption news in India.**

Fetches real-time news from Google RSS feeds, automatically classifies incidents by type, detects affected cities using pattern matching, stores data in a SQLite database, and presents all information through an interactive, modern web dashboard with powerful filtering and analytics capabilities.

![System Status](https://img.shields.io/badge/status-production--ready-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688)
![Database](https://img.shields.io/badge/database-SQLite-blue)
![Frontend](https://img.shields.io/badge/frontend-Vanilla%20JS-yellow)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Real-Time Ingestion](#real-time-ingestion)
- [Demo Instructions](#demo-instructions)
- [Project Structure](#project-structure)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)

---

## 🎯 What Is This Project?

### The Problem It Solves

Infrastructure disruptions (power outages, water shortages, traffic jams) happen constantly across Indian cities, but there's no centralized way to track and monitor them. News is scattered across multiple sources, and manually collecting this information is time-consuming and inefficient.

### The Solution

This **Real-Time News & Events Monitoring System** automatically:
- **Monitors** multiple news sources 24/7 for utility disruption incidents
- **Classifies** articles into categories (power outages, water issues, traffic delays)
- **Detects** which cities are affected using intelligent pattern matching
- **Stores** all information in a searchable database
- **Presents** beautiful dashboards and APIs for easy access

### Target Users

- **Government Agencies**: Track infrastructure incidents for emergency response
- **Utility Companies**: Monitor incidents affecting their services
- **News Aggregators**: Create intelligence dashboards from disruption news
- **Citizens**: Stay informed about disruptions in their cities
- **Researchers**: Analyze infrastructure resilience and incident patterns

---

## 🎯 How It Works: Step-by-Step Process

### The Data Flow

```
1. FETCH PHASE (Real-time)
   └─ Pulls latest news from Google News RSS feeds (3 feeds, ~100 articles each)

2. PROCESS PHASE (Automated)
   ├─ Parse articles and extract metadata (title, date, link, content)
   ├─ Classify each article (Power Outage? Water Issue? Traffic Jam?)
   └─ Detect city mentioned (Delhi? Mumbai? Bengaluru? Or Unknown?)

3. STORE PHASE (Intelligent)
   └─ Save to SQLite database with automatic duplicate detection

4. EXPOSE PHASE (REST APIs)
   ├─ /events       → Query all incidents with filters
   ├─ /stats        → Get statistics by category
   ├─ /cities       → See which cities are affected
   └─ /docs         → Interactive API documentation

5. DISPLAY PHASE (Beautiful UI)
   └─ Web dashboard showing live events, filters, and statistics
```

### Key Capabilities

| Capability | Description |
|-----------|-------------|
| **Real-Time Monitoring** | Checks Google News feeds continuously for new incidents |
| **Automatic Classification** | Categorizes articles: Power Outage, Water Issue, Logistics Delay |
| **City Detection** | Identifies affected cities: Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad |
| **Duplicate Prevention** | Never shows the same news twice (uses title as unique key) |
| **Powerful Search** | Filter by city, category, or both simultaneously |
| **Statistics Dashboard** | See event counts by type and location |
| **Source Links** | Click through to original news articles |
| **REST API** | Programmatic access to all data in JSON format |
| **Zero Configuration** | No API keys, databases, or external services needed |

---

## ✨ Features

### ✅ Real-Time Data Ingestion
- Fetches live news from Google News RSS (no API key required)
- Processes articles every time ingestion runs
- Safe to run multiple times (duplicate prevention)

### ✅ Automated Classification
- **Power Outages**: Detects power cuts, blackouts, electricity failures
- **Water Issues**: Identifies water shortages, pipeline leaks, supply disruptions
- **Logistics Delays**: Catches traffic jams, transport delays, supply chain issues

### ✅ Location Detection
- Automatically detects cities: Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad
- Marks as "Unknown" if no city detected

### ✅ REST API Backend
- Filter events by city and/or category
- Get statistics (event counts by category)
- Get cities with event counts
- Auto-generated Swagger documentation

### ✅ Interactive Dashboard
- Clean, modern UI with responsive design
- Real-time filtering by city and category
- Statistics cards showing event counts
- Source links to original news articles

---

## 🏗️ Complete System Architecture

### Visual Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          USER'S BROWSER (CLIENT SIDE)                        │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │              INTERACTIVE WEB DASHBOARD (Frontend)                     │  │
│  │                   HTML + CSS + Vanilla JavaScript                     │  │
│  │                                                                       │  │
│  │  ┌─────────────────────────────────────────────────────────────┐    │  │
│  │  │  Header: Real-Time News & Events Monitoring System          │    │  │
│  │  └─────────────────────────────────────────────────────────────┘    │  │
│  │                                                                       │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │  │
│  │  │  Stats Cards     │  │  City Filter     │  │  Category Filter │   │  │
│  │  │                  │  │                  │  │                  │   │  │
│  │  │  📊 Total: 164   │  │  📍 Dropdown ▼   │  │  📌 Dropdown ▼   │   │  │
│  │  │  Power: 92       │  │  Delhi, Mumbai,  │  │  Power Outage    │   │  │
│  │  │  Water: 54       │  │  Bengaluru...    │  │  Water Issue     │   │  │
│  │  │  Logistics: 18   │  │                  │  │  Logistics Delay │   │  │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │  │
│  │                                                                       │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │  Events Table (Dynamically Filtered)                         │   │  │
│  │  ├───────────────────────────────────────────────────────────────┤  │  │
│  │  │ Title | City | Date | Category | Source Link | View →        │   │  │
│  │  ├───────────────────────────────────────────────────────────────┤  │  │
│  │  │ Delhi Power Cut on Feb 9 | Delhi | Feb 9 2026 | power...     │   │  │
│  │  │ Water Crisis in Mumbai   | Mumbai| Feb 9 2026 | water...     │   │  │
│  │  │ Traffic Jam on NH-19     | Delhi | Feb 9 2026 | logistics... │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │                                                                       │  │
│  │  [Refresh Data Button] [Export CSV]                                  │  │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│                    ↕️  HTTP/REST Requests & Responses                       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                      ↕️
                          (Port 8000 on localhost)
                                      ↕️
┌──────────────────────────────────────────────────────────────────────────────┐
│                         SERVER SIDE (BACKEND)                                │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                   FastAPI Web Framework                              │  │
│  │         (Modern Python web framework with auto-generated docs)       │  │
│  │                                                                      │  │
│  │  REST API Endpoints:                                               │  │
│  │  ├─ GET  /              → Serve HTML dashboard                     │  │
│  │  ├─ GET  /events        → Get filtered events (JSON)               │  │
│  │  ├─ GET  /stats         → Get statistics by category               │  │
│  │  ├─ GET  /cities        → Get cities with event counts             │  │
│  │  ├─ GET  /docs          → Interactive Swagger UI                   │  │
│  │  └─ POST /refresh       → Trigger ingestion manually (optional)     │  │
│  │                                                                      │  │
│  │  Supported Query Parameters:                                        │  │
│  │  ├─ ?city=Delhi          → Filter by city name                     │  │
│  │  ├─ ?category=power_outage → Filter by incident type              │  │
│  │  └─ ?city=Delhi&category=power_outage → Combined filters          │  │
│  │                                                                      │  │
│  │  Response Format: JSON with pagination and metadata                │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                      ↕️                                       │
│                         (SQL Queries & Results)                              │
│                                      ↕️                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    SQLite Database Engine                            │  │
│  │              (Lightweight, file-based database)                      │  │
│  │                                                                      │  │
│  │  Database File: db/events.db                                        │  │
│  │                                                                      │  │
│  │  Table: events                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │ Column       │ Type     │ Properties                           │  │  │
│  │  ├──────────────┼──────────┼──────────────────────────────────────┤  │  │
│  │  │ id           │ INTEGER  │ Primary Key, Auto-increment          │  │  │
│  │  │ title        │ TEXT     │ UNIQUE (prevents duplicates)         │  │  │
│  │  │ city         │ TEXT     │ Indexed for fast filtering           │  │  │
│  │  │ date         │ DATETIME │ Indexed for sorting                  │  │  │
│  │  │ category     │ TEXT     │ Indexed for filtering                │  │  │
│  │  │ source       │ TEXT     │ Link to original news article        │  │  │
│  │  │ created_at   │ DATETIME │ Auto-populated insertion time        │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  │  Indexes:                                                           │  │
│  │  ├─ idx_city (fast city filtering)                                 │  │
│  │  ├─ idx_category (fast category filtering)                         │  │
│  │  └─ idx_date (chronological sorting)                               │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                      ↑                                       │
│                              (INSERT OR IGNORE)                              │
│                                      ↑                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                 Data Ingestion Pipeline                              │  │
│  │           (Python script: ingestion/ingest_news.py)                 │  │
│  │                                                                      │  │
│  │  Step 1: FETCH RSS FEEDS                                           │  │
│  │  ├─ Feed 1: Google News - "power outage India"                     │  │
│  │  ├─ Feed 2: Google News - "water shortage India"                   │  │
│  │  └─ Feed 3: Google News - "traffic jam India"                      │  │
│  │    └─ Downloads ~100 articles per feed                             │  │
│  │                                                                      │  │
│  │  Step 2: PARSE ARTICLES                                            │  │
│  │  ├─ Extract title (article headline)                               │  │
│  │  ├─ Extract summary (article snippet)                              │  │
│  │  ├─ Extract link (source URL)                                      │  │
│  │  └─ Extract date (publication date)                                │  │
│  │                                                                      │  │
│  │  Step 3: CLASSIFY INCIDENTS (Keyword Matching)                    │  │
│  │  ├─ POWER_OUTAGE keywords: "power cut", "blackout", "outage"      │  │
│  │  ├─ WATER_ISSUE keywords: "water shortage", "supply disrupted"    │  │
│  │  └─ LOGISTICS_DELAY keywords: "traffic jam", "delay", "stranded"  │  │
│  │                                                                      │  │
│  │  Step 4: DETECT CITIES (Regex Pattern Matching)                   │  │
│  │  ├─ Cities: Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad │  │
│  │  └─ Fallback: "Unknown" if no city matched                         │  │
│  │                                                                      │  │
│  │  Step 5: INSERT INTO DATABASE                                      │  │
│  │  ├─ Uses INSERT OR IGNORE (skips duplicate titles)                 │  │
│  │  ├─ Logs success/skip status                                       │  │
│  │  └─ Prints summary statistics                                      │  │
│  │                                                                      │  │
│  │  Execution:                                                         │  │
│  │  ├─ Manual: python ingestion/ingest_news.py                        │  │
│  │  ├─ Scheduled: cron job (Linux) or Task Scheduler (Windows)        │  │
│  │  └─ Triggered: API endpoint or CI/CD pipeline                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                      ↑                                       │
│                             (RSS/XML Feed)                                   │
│                                      ↑                                       │
└──────────────────────────────────────────────────────────────────────────────┘
                                      ↑
                          (Public Internet)
                                      ↑
┌──────────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL DATA SOURCE                                   │
│                                                                              │
│  Google News RSS Feeds (No API Key Required!)                               │
│  ├─ https://news.google.com/rss/search?q=power+outage+India               │
│  ├─ https://news.google.com/rss/search?q=water+shortage+India             │
│  └─ https://news.google.com/rss/search?q=traffic+jam+India                │
│                                                                              │
│  Data Source: Automatically updates with latest news every few hours        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### How Data Flows Through The System

1. **Ingestion (Pull-based)**
   - Scripts/scheduled jobs pull news from Google News RSS feeds
   - Articles are fetched, parsed, and classified
   - New events are inserted into SQLite database
   - Duplicates are automatically skipped

2. **Storage (Persistence)**
   - Events are stored in SQLite with full-text searchability
   - Database uses indexes for fast filtering
   - Unique title constraint prevents duplicate storage

3. **Query (Read)**
   - FastAPI backend queries the database based on filter parameters
   - Results are formatted as JSON
   - CORS headers enable cross-origin requests from any frontend

4. **Display (Visualization)**
   - HTML dashboard makes HTTP requests to the backend
   - JavaScript dynamically updates UI based on filters
   - Real-time interaction with dropdown filters

### Technology Stack at Each Layer

| Layer | Technology | What It Does |
|-------|-----------|-------------|
| **Presentation** | HTML5 + CSS3 | Renders the dashboard UI |
| **Interaction** | Vanilla JavaScript | Handles filters, clicks, API calls |
| **Network** | HTTP/REST | Communicates between frontend and backend |
| **Backend** | FastAPI | Handles requests, queries database, returns JSON |
| **Server** | Uvicorn ASGI | Runs FastAPI application |
| **Database** | SQLite | Stores events with indexing |
| **Ingestion** | Python + feedparser | Fetches and processes RSS feeds |

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | Modern, fast web framework with auto docs |
| **Server** | Uvicorn | ASGI server for FastAPI |
| **Database** | SQLite | Lightweight, file-based database |
| **RSS Parser** | feedparser | Parse Google News RSS feeds |
| **Frontend** | HTML/CSS/JS | Vanilla (no build step required) |
| **Deployment** | Docker (optional) | Containerization |

**Why These Choices?**
- **FastAPI**: Automatic API documentation, type validation, fast performance
- **SQLite**: Zero configuration, perfect for MVP/demo
- **Vanilla JS**: No build tools needed, runs directly in browser
- **RSS**: Free data source, no API key required

---

## 🚀 Running on Local System - Complete Guide

### System Requirements

**Minimum Requirements:**
- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.10 or higher
- **Disk Space**: ~100 MB (including dependencies and database)
- **RAM**: 512 MB minimum, 1GB recommended
- **Internet**: Required for fetching news feeds
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)

**Check Your Python Version:**
```bash
python --version
# Expected: Python 3.10.x or higher
```

### Step-by-Step Installation & Setup

#### Step 1: Navigate to Project Directory

**Windows (PowerShell/Command Prompt):**
```powershell
cd a:\hyd_proj\news-events-monitoring-mvp
```

**Mac/Linux:**
```bash
cd /path/to/news-events-monitoring-mvp
```

#### Step 2: Install Python Dependencies

This installs FastAPI, Uvicorn, and feedparser - everything the project needs.

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `fastapi==0.109.0` - Web framework
- `uvicorn[standard]==0.27.0` - Web server
- `feedparser==6.0.10` - RSS parsing library

**Verification:**
```bash
pip list | grep -E "fastapi|uvicorn|feedparser"
```

#### Step 3: Initialize the Database

Creates the SQLite database file and sets up the schema (tables, indexes).

**Windows PowerShell:**
```powershell
python -c "import sqlite3; conn = sqlite3.connect('db/events.db'); conn.executescript(open('db/schema.sql').read()); conn.close(); print('✅ Database initialized successfully')"
```

**Mac/Linux/Git Bash:**
```bash
mkdir -p db
sqlite3 db/events.db < db/schema.sql
echo "✅ Database initialized successfully"
```

**What happens:**
- Creates `db/events.db` (SQLite database file)
- Creates `events` table with columns: id, title, city, date, category, source
- Creates indexes on city, category, and date for fast filtering
- Sets up UNIQUE constraint on title to prevent duplicates

**Verification:**
```bash
# Check if database file exists
ls -la db/events.db  # Mac/Linux
dir db\events.db     # Windows
```

#### Step 4: Fetch Real-Time News Data (Ingestion)

Downloads the latest news from Google News RSS feeds and populates the database.

```bash
python ingestion/ingest_news.py
```

**Expected Output:**
```
======================================================================
REAL-TIME NEWS INGESTION PIPELINE
======================================================================

🔍 Fetching RSS feeds...
  ✓ Fetched 100 articles from feed
  ✓ Fetched 100 articles from feed
  ✓ Fetched 100 articles from feed
📰 Total articles fetched: 300

✓ Connected to database

🔄 Processing articles...
  ✓ [power_outage] Bengaluru: Bengaluru power cut: Bescom announces outage for five days
  ✓ [water_issue] Delhi: Water Crisis in Delhi? Despite plans to revive lakes...
  ✓ [logistics_delay] Mumbai: Stuck For 8 Hours, Industrialist Takes Helicopter...
  ... (more articles)

======================================================================
INGESTION SUMMARY
======================================================================
  Articles processed: 300
  New events inserted: 164
  Duplicates skipped: 0
  Irrelevant skipped: 136
======================================================================

✅ Ingestion complete!
```

**What happens:**
- Fetches ~300 articles from 3 Google News RSS feeds
- Classifies each article into one of 3 categories
- Detects city mentioned in each article
- Inserts new events into the database
- Skips articles that don't match any category
- Prevents duplicates using title uniqueness

#### Step 5: Start the Web Server (Backend)

Starts the FastAPI application on `http://localhost:8000`

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Or using Python module syntax:**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['A:\\hyd_proj\\news-events-monitoring-mvp']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [21388] using WatchFiles
INFO:     Started server process [15504]
INFO:     Waiting for application startup.

======================================================================
🚀 Real-Time News & Events Monitoring API
======================================================================
Dashboard:       http://localhost:8000
API Docs:        http://localhost:8000/docs
Events Endpoint: http://localhost:8000/events
Stats Endpoint:  http://localhost:8000/stats
Cities Endpoint: http://localhost:8000/cities
======================================================================

INFO:     Application startup complete.
```

**Parameters:**
- `app.main:app` - Loads the FastAPI application from app/main.py
- `--reload` - Auto-restarts server when code changes (development mode)
- `--host 0.0.0.0` - Listens on all network interfaces
- `--port 8000` - Uses port 8000

**Keep this terminal open!** The server runs here continuously.

#### Step 6: Access the Application

Open your web browser and navigate to:

**Dashboard (Main Website):**
```
http://localhost:8000
```

You should see a beautiful dashboard with:
- Statistics cards showing event counts
- City filter dropdown
- Category filter dropdown
- Table of events with details
- Links to original news sources

**Interactive API Documentation:**
```
http://localhost:8000/docs
```

Shows all available endpoints with ability to test them directly in the browser.

**Direct API Access:**
```
http://localhost:8000/events
http://localhost:8000/events?city=Delhi
http://localhost:8000/events?category=power_outage
http://localhost:8000/stats
http://localhost:8000/cities
```

### Running All Steps at Once (Quick Start Script)

Create a file named `setup_and_run.bat` (Windows) or `setup_and_run.sh` (Mac/Linux):

**Windows (setup_and_run.bat):**
```batch
@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Initializing database...
python -c "import sqlite3; conn = sqlite3.connect('db/events.db'); conn.executescript(open('db/schema.sql').read()); conn.close(); print('✅ Database ready')"

echo Fetching news data...
python ingestion/ingest_news.py

echo Starting server...
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
```

Run it:
```batch
setup_and_run.bat
```

**Mac/Linux (setup_and_run.sh):**
```bash
#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
mkdir -p db
sqlite3 db/events.db < db/schema.sql

echo "Fetching news data..."
python ingestion/ingest_news.py

echo "Starting server..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run it:
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### Using Docker (Optional - For Advanced Users)

Alternatively, run the entire application in a Docker container:

```bash
docker-compose up -d
```

Access at `http://localhost:8000`

Stop with:
```bash
docker-compose down
```

### Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| **"Port 8000 already in use"** | Change port: `uvicorn app.main:app --port 8001` |
| **"Module not found: fastapi"** | Run: `pip install -r requirements.txt` |
| **Database locked error** | Close any other terminal running the app, then restart |
| **"No events showing"** | Run ingestion again: `python ingestion/ingest_news.py` |
| **Dashboard not loading** | Check if server is running and port is correct |
| **API returns empty results** | Make sure ingestion pipeline completed successfully |

---

## 🌐 Website User Guide - How to Use the Dashboard

Once the server is running and you navigate to `http://localhost:8000`, you'll see an interactive dashboard. Here's how to use it:

### Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│         🔔 Real-Time News & Events Monitoring System                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  📊 STATISTICS SECTION                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │   TOTAL      │  │ POWER OUTAGE │  │ WATER ISSUE  │                 │
│  │    164       │  │      92      │  │      54      │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                         │
│  🔍 FILTER SECTION                                                     │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ City Filter: [All Cities ▼]    Category Filter: [All Categories ▼]│
│  │                                                                  │ │
│  │ [Refresh Data Button]  [Clear All Filters Button]              │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  📋 EVENTS TABLE (Filtered Results)                                   │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Title | City | Date | Category | Source | Action               │ │
│  ├──────────────────────────────────────────────────────────────────┤ │
│  │ Bengaluru power cut | Bengaluru | Feb 11, 2026 | power_outage   │ │
│  │ [View News Article →]                                            │ │
│  ├──────────────────────────────────────────────────────────────────┤ │
│  │ Water Crisis in Delhi | Delhi | Feb 9, 2026 | water_issue       │ │
│  │ [View News Article →]                                            │ │
│  ├──────────────────────────────────────────────────────────────────┤ │
│  │ Traffic Jam on Mumbai-Pune Expressway | Mumbai | ... | logistics │ │
│  │ [View News Article →]                                            │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  Showing 1-10 of 164 results                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Features & How to Use Them

#### 1. **Statistics Cards** (Top Section)
Shows quick overview of all events:
- **TOTAL**: Total number of events in the database
- **POWER OUTAGE**: Events classified as power-related incidents
- **WATER ISSUE**: Events classified as water-related problems
- **LOGISTICS DELAY**: Events related to traffic jams or transportation delays

**Use Case**: Quick health check - see how many of each type of incident is happening

#### 2. **City Filter Dropdown**
```
Click the dropdown that says "All Cities ▼"
Options appear:
  ☐ Delhi
  ☐ Mumbai
  ☐ Bengaluru
  ☐ Chennai
  ☐ Kolkata
  ☐ Hyderabad
  ☐ Unknown (when city couldn't be detected)
```

**How it works:**
- Select a city to see only events from that city
- The table updates instantly
- Statistics cards also update to show only that city's data
- Combine with Category filter for more specific results

**Example**: 
- Click "Delhi" to see only Delhi events
- Result: Shows 24 Delhi events with breakdown by type

#### 3. **Category Filter Dropdown**
```
Click the dropdown that says "All Categories ▼"
Options appear:
  ☐ power_outage (Power cuts, blackouts)
  ☐ water_issue (Water shortages, supply problems)
  ☐ logistics_delay (Traffic jams, transportation delays)
```

**How it works:**
- Select a category to see only events of that type
- Combine with City filter for specific queries
- Statistics cards show only matching events

**Example**: 
- Click "power_outage" to see only power-related incidents
- Result: Shows 92 power events sorted by date

#### 4. **Combined Filtering**
For maximum control, use both filters together:

**Example Scenarios:**
- "Show power outages in Delhi"
  - City Filter: Delhi
  - Category Filter: power_outage
  - Result: 12 events showing Delhi power incidents

- "Show all water issues"
  - City Filter: All Cities
  - Category Filter: water_issue
  - Result: 54 events showing water problems everywhere

- "Show everything in Mumbai"
  - City Filter: Mumbai
  - Category Filter: All Categories
  - Result: 18 events of all types in Mumbai

#### 5. **Refresh Data Button**
```
Click [Refresh Data] button
```

**What happens:**
- Re-fetches news from Google News RSS feeds
- Classifies and processes new articles
- Updates the database with new events
- Takes 10-30 seconds depending on internet speed
- Dashboard auto-updates with new data

**When to use:**
- When you want the absolute latest news
- Before an important decision
- After a major event happens

#### 6. **Events Table**
Displays all matching events with columns:

| Column | What It Shows | Example |
|--------|---|---|
| **Title** | Headline of the news article | "Delhi Faces Massive Power Outage" |
| **City** | Which city is affected | "Delhi" or "Unknown" |
| **Date** | When the incident occurred | "Feb 9, 2026 14:30" |
| **Category** | Type of incident | "power_outage", "water_issue", "logistics_delay" |
| **Source** | Link to original news | Click "View News Article →" |

**Sorting:**
- Most recent events appear first
- Newest incidents at the top

#### 7. **View News Article Links**
Each event has a "View News Article →" button

**What happens when you click:**
- Opens the original news article in a new browser tab
- Takes you directly to the source (Google News)
- Verify the incident with full article details

### Common Use Cases

**Scenario 1: I'm a Citizen in Delhi**
```
1. Click City Filter → Select "Delhi"
2. See all 24 incidents in Delhi
3. Check dates to see what's happening right now
4. Click on incidents to read full articles
```

**Scenario 2: I Work for the Power Company**
```
1. Click Category Filter → Select "power_outage"
2. See all 92 power-related incidents
3. Filter by city to focus on your service area
4. Use data for emergency response planning
```

**Scenario 3: I'm a News Researcher**
```
1. Click [Refresh Data] to get latest incidents
2. Filter by category to analyze trends
3. Click on articles to verify information
4. Use statistics cards for reporting
```

**Scenario 4: I Want to Monitor Everything**
```
1. Leave all filters as "All Cities" and "All Categories"
2. See complete dashboard: 164 total events
3. Statistics show breakdown by type
4. Periodically click [Refresh Data] for updates
```

### Tips & Tricks

- **Fastest Way to See Delhi News**: City→Delhi, leave Category as "All"
- **Find Traffic Issues**: Category→logistics_delay, City→your city
- **Get Statistics**: Just look at the cards at top (no scrolling needed)
- **Verify an Incident**: Click "View News Article" to read full story
- **Multiple Filters**: Using both City and Category gives most precise results
- **Real-Time Updates**: Click Refresh to get latest news
- **Unknown Cities**: If a city wasn't detected, it shows as "Unknown"

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### System Status & Monitoring

**Check if system is running:**
```bash
# Open in any browser or use curl
curl http://localhost:8000/

# Should return the dashboard HTML
# Status Code: 200 OK
```

**View API Documentation:**
```
http://localhost:8000/docs
```

Shows interactive Swagger UI with all endpoints and test capabilities.

### Endpoints

#### 1. GET /events
Get all events with optional filtering.

**Query Parameters**:
- `city` (optional): Filter by city name (e.g., "Delhi", "Mumbai")
- `category` (optional): Filter by category ("power_outage", "water_issue", "logistics_delay")

**Examples**:
```bash
# Get all events
curl http://localhost:8000/events

# Get events in Delhi
curl http://localhost:8000/events?city=Delhi

# Get power outage events
curl http://localhost:8000/events?category=power_outage

# Get water issues in Mumbai
curl http://localhost:8000/events?city=Mumbai&category=water_issue
```

**Response**:
```json
[
  {
    "id": 1,
    "title": "Major power outage affects 50,000 homes in Delhi",
    "city": "Delhi",
    "date": "2026-02-09 14:30:00",
    "category": "power_outage",
    "source": "https://news.google.com/..."
  }
]
```

---

#### 2. GET /stats
Get event count statistics grouped by category.

**Example**:
```bash
curl http://localhost:8000/stats
```

**Response**:
```json
{
  "power_outage": 15,
  "water_issue": 8,
  "logistics_delay": 12
}
```

---

#### 3. GET /cities
Get list of cities with event counts.

**Example**:
```bash
curl http://localhost:8000/cities
```

**Response**:
```json
[
  {"city": "Delhi", "count": 10},
  {"city": "Mumbai", "count": 8},
  {"city": "Bengaluru", "count": 5}
]
```

---

#### 4. GET /docs
Interactive Swagger UI for API testing.

**URL**: `http://localhost:8000/docs`

---

## 🔄 Real-Time Ingestion

### How It Works

The ingestion pipeline (`ingestion/ingest_news.py`) fetches real-time news from Google News RSS feeds:

**RSS Feed URLs**:
1. `https://news.google.com/rss/search?q=power+outage+India`
2. `https://news.google.com/rss/search?q=water+shortage+India`
3. `https://news.google.com/rss/search?q=traffic+jam+India`

**Processing Steps**:

1. **Fetch RSS Feeds**:
   - Uses `feedparser` library to parse XML
   - Extracts: title, summary, link, published date

2. **Classify Incidents**:
   - Keyword-based matching (case-insensitive)
   - Checks title and summary for category keywords
   - Skips articles with no matching category

3. **Detect City**:
   - Word boundary regex matching
   - Checks for: Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad
   - Defaults to "Unknown" if no match

4. **Store in Database**:
   - Uses `INSERT OR IGNORE` for duplicate prevention
   - Title is unique key (prevents same article being added twice)

**Running Ingestion**:
```bash
# Run once
python ingestion/ingest_news.py

# Run periodically with cron (Linux/Mac)
*/15 * * * * cd /path/to/project && python ingestion/ingest_news.py

# Run periodically with Task Scheduler (Windows)
# Create a task that runs: python C:\path\to\project\ingestion\ingest_news.py
```

---

## 🎬 Demo Instructions

### 3-Minute Demo Flow

Perfect for demonstrating the system in an interview or presentation:

**1. Initialize Database** (5 seconds)
```bash
python -c "import sqlite3; conn = sqlite3.connect('db/events.db'); conn.executescript(open('db/schema.sql').read()); conn.close()"
```

**2. Run Ingestion** (30 seconds)
```bash
python ingestion/ingest_news.py
```
Show the output: articles being fetched and classified.

**3. Start Backend** (5 seconds - in new terminal)
```bash
uvicorn app.main:app --reload
```

**4. Open Dashboard** (5 seconds)
Navigate to `http://localhost:8000` in browser.

**5. Demonstrate Features** (90 seconds)
- Show statistics cards (total events, breakdown by category)
- Filter by city (e.g., select "Delhi")
- Filter by category (e.g., "Power Outage")
- Click "View" link to show original news source
- Click "Refresh Data" button

**6. Show API** (30 seconds)
- Navigate to `http://localhost:8000/docs`
- Try `/events` endpoint with filters
- Show `/stats` endpoint

**7. Demonstrate Duplicate Prevention** (15 seconds)
```bash
python ingestion/ingest_news.py
```
Show that duplicate count increases but no new events added.

---

## 📁 Project Structure

```
news-events-monitoring-mvp/
│
├── ingestion/
│   └── ingest_news.py          # RSS fetching and classification script
│
├── app/
│   ├── main.py                 # FastAPI backend application
│   └── templates/
│       └── index.html          # Frontend dashboard
│
├── static/
│   └── styles.css              # Dashboard styling
│
├── db/
│   ├── schema.sql              # Database schema
│   └── events.db               # SQLite database (created at runtime)
│
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker deployment config
├── README.md                   # This file
└── report.md                   # Technical report
```

---

## ⚠️ Limitations

### Current Implementation

1. **Classification Accuracy**:
   - Uses simple keyword matching (not ML)
   - May misclassify articles with ambiguous language
   - Can't handle complex semantic understanding

2. **Location Detection**:
   - Only detects 6 predefined cities
   - Uses basic string matching (not NLP/NER)
   - Can't handle variations (e.g., "NCR" vs "Delhi")

3. **Data Source**:
   - Depends on Google News RSS availability
   - Limited to articles indexed by Google
   - No historical data (only recent news)

4. **Scalability**:
   - SQLite not suitable for high concurrency
   - No distributed architecture
   - Frontend makes direct API calls (no caching)

5. **Real-Time Processing**:
   - Ingestion is manual/scripted (not event-driven)
   - No webhooks or push notifications
   - Requires periodic cron jobs

---

## 🚀 Future Improvements

### Short-Term (MVP+)

1. **Better Classification**:
   - Use spaCy or NLTK for NLP-based classification
   - Train a simple ML model (Naive Bayes, Logistic Regression)
   - Add confidence scores

2. **Enhanced Location Detection**:
   - Integrate NER (Named Entity Recognition)
   - Support state-level detection
   - Handle spelling variations

3. **More Data Sources**:
   - NewsAPI integration
   - Twitter/X API for social media monitoring
   - Government alert feeds

4. **Frontend Enhancements**:
   - Charts/graphs (Chart.js or D3.js)
   - Map visualization (Google Maps API)
   - Export data to CSV/JSON

### Long-Term (Production)

1. **Scalability**:
   - Migrate to PostgreSQL or MongoDB
   - Add Redis caching layer
   - Implement message queue (RabbitMQ, Kafka)

2. **Real-Time Processing**:
   - WebSocket for live updates
   - Event-driven architecture
   - Push notifications

3. **Advanced Features**:
   - Sentiment analysis
   - Trend detection
   - Predictive alerts

4. **DevOps**:
   - CI/CD pipeline (GitHub Actions)
   - Kubernetes deployment
   - Monitoring (Prometheus, Grafana)

---

## 🤝 Contributing

This is an interview/demo project. Feel free to fork and extend!

---

## 📄 License

MIT License - feel free to use for educational/commercial purposes.

---

## 📞 Contact

For questions or feedback, reach out to the project maintainer.

---

**Built with ❤️ using FastAPI, SQLite, and Vanilla JavaScript**

---

## Deploy on Vercel

This repository is configured for Vercel serverless deployment using FastAPI.

### Included deployment files

- `vercel.json` routes all requests to the FastAPI app.
- `api/index.py` is the Vercel Python entrypoint.
- Frontend API calls use relative URLs, so they work on your Vercel domain.

### Steps

1. Push this project to GitHub.
2. In Vercel, click **Add New Project** and import the repository.
3. Keep default settings. Vercel will detect `vercel.json`.
4. Deploy.

After deploy, your app will be available at:

- `/` dashboard
- `/events` API
- `/stats` API
- `/cities` API
- `/docs` FastAPI docs

### Important note about SQLite on Vercel

Vercel serverless filesystem is read-only at runtime and ephemeral between deployments.
This app can **read** the bundled `db/events.db` file, but runtime writes/persistent updates are not reliable on Vercel.
If you need live ingestion in production, move to a managed database (for example: Neon/Postgres, Supabase, or PlanetScale/MySQL).
