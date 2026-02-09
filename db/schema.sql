-- Real-Time News & Events Monitoring System
-- SQLite Database Schema
-- Purpose: Store classified news events with location and category information

-- Drop table if exists (for clean re-initialization)
DROP TABLE IF EXISTS events;

-- Create events table
-- This table stores all detected utility disruption events
CREATE TABLE events (
    -- Primary key: Auto-incrementing unique identifier
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Event title from news article
    -- UNIQUE constraint prevents duplicate articles when ingestion runs multiple times
    title TEXT NOT NULL UNIQUE,
    
    -- Detected city from predefined list
    -- Values: Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Unknown
    city TEXT NOT NULL,
    
    -- Publication date of the article (ISO 8601 format: YYYY-MM-DD HH:MM:SS)
    date TEXT NOT NULL,
    
    -- Event category based on keyword classification
    -- Values: power_outage, water_issue, logistics_delay
    category TEXT NOT NULL,
    
    -- Source URL of the news article (for reference)
    source TEXT NOT NULL
);

-- Create indexes for efficient filtering
-- These indexes speed up API queries with WHERE clauses on city and category
CREATE INDEX idx_city ON events(city);
CREATE INDEX idx_category ON events(category);
CREATE INDEX idx_date ON events(date);

-- Sample query to verify schema
-- SELECT * FROM events WHERE city = 'Delhi' AND category = 'power_outage';
