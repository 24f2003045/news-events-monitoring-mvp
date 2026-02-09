"""
Real-Time News Ingestion Pipeline
===================================

Purpose:
    Fetches real-time news from Google News RSS feeds, classifies incidents
    using keyword matching, detects cities, and stores in SQLite database.

Features:
    - Fetches RSS feeds for utility disruptions in India
    - Rule-based keyword classification (power_outage, water_issue, logistics_delay)
    - Simple city detection using string matching
    - Duplicate prevention using SQLite UNIQUE constraint
    - Safe to run multiple times

Usage:
    python ingestion/ingest_news.py
"""

import sqlite3
import feedparser
from datetime import datetime
from typing import List, Dict, Optional
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

# SQLite database path
DATABASE_PATH = "db/events.db"

# Cities to detect in news articles (predefined list)
CITIES = [
    'Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 
    'Kolkata', 'Hyderabad'
]

# Category keywords for classification
CATEGORY_KEYWORDS = {
    'power_outage': [
        'power cut', 'electricity outage', 'blackout',
        'power failure', 'grid failure', 'power supply disruption'
    ],
    'water_issue': [
        'water shortage', 'pipeline leak', 'water supply disruption',
        'water crisis', 'water cut', 'water contamination'
    ],
    'logistics_delay': [
        'traffic jam', 'transport delay', 'supply chain issue',
        'road blockage', 'traffic congestion', 'delivery delay'
    ]
}

# RSS feed URLs (Google News search queries)
RSS_FEEDS = [
    "https://news.google.com/rss/search?q=power+outage+India&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=water+shortage+India&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=traffic+jam+India&hl=en-IN&gl=IN&ceid=IN:en",
]

# ============================================================================
# CLASSIFICATION LOGIC
# ============================================================================

def classify_incident(title: str, summary: str) -> Optional[str]:
    """
    Classify incident using keyword matching (rule-based approach).
    
    Args:
        title: News article title
        summary: News article summary/description
        
    Returns:
        Category string (power_outage, water_issue, logistics_delay) or None
        
    Algorithm:
        1. Combine title and summary into single text
        2. Convert to lowercase for case-insensitive matching
        3. Check if any keyword from each category appears
        4. Return first matching category
        5. Return None if no match (article will be skipped)
    """
    # Combine title and summary for matching
    text = (title + " " + summary).lower()
    
    # Check each category's keywords
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return category
    
    # No match found
    return None


def detect_city(title: str, summary: str) -> str:
    """
    Detect city using simple string matching.
    
    Args:
        title: News article title
        summary: News article summary/description
        
    Returns:
        City name from CITIES list or "Unknown"
        
    Algorithm:
        1. Combine title and summary
        2. Check if any city name appears (case-insensitive)
        3. Return first match
        4. Default to "Unknown" if no city detected
    """
    # Combine title and summary
    text = (title + " " + summary)
    
    # Check each city
    for city in CITIES:
        # Case-insensitive substring search
        if re.search(r'\b' + city + r'\b', text, re.IGNORECASE):
            return city
    
    # No city detected
    return "Unknown"


# ============================================================================
# RSS FEED FETCHING
# ============================================================================

def fetch_rss_articles() -> List[Dict]:
    """
    Fetch articles from all configured RSS feeds.
    
    Returns:
        List of article dictionaries with keys: title, summary, link, published
        
    Note:
        Uses feedparser library which handles all RSS parsing complexities
    """
    all_articles = []
    
    print("🔍 Fetching RSS feeds...")
    
    for feed_url in RSS_FEEDS:
        try:
            # Parse RSS feed
            feed = feedparser.parse(feed_url)
            
            # Extract entries
            for entry in feed.entries:
                article = {
                    'title': entry.get('title', ''),
                    'summary': entry.get('summary', entry.get('description', '')),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', datetime.now().isoformat())
                }
                all_articles.append(article)
            
            print(f"  ✓ Fetched {len(feed.entries)} articles from feed")
        
        except Exception as e:
            print(f"  ✗ Error fetching feed {feed_url}: {e}")
            continue
    
    print(f"📰 Total articles fetched: {len(all_articles)}\n")
    return all_articles


# ============================================================================
# DATA PROCESSING PIPELINE
# ============================================================================

def process_and_store_articles(articles: List[Dict]) -> Dict[str, int]:
    """
    Process articles: classify, detect city, and store in database.
    
    Args:
        articles: List of article dictionaries from RSS feeds
        
    Returns:
        Statistics dictionary with counts: processed, inserted, duplicates, skipped
    """
    stats = {
        'processed': 0,
        'inserted': 0,
        'duplicates': 0,
        'skipped': 0
    }
    
    # Connect to database
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        print("✓ Connected to database\n")
    except sqlite3.Error as e:
        print(f"✗ Database connection error: {e}")
        return stats
    
    print("🔄 Processing articles...")
    
    for article in articles:
        stats['processed'] += 1
        
        title = article['title']
        summary = article['summary']
        link = article['link']
        published = article['published']
        
        # Step 1: Classify incident
        category = classify_incident(title, summary)
        
        if category is None:
            # No matching category - skip this article
            stats['skipped'] += 1
            continue
        
        # Step 2: Detect city
        city = detect_city(title, summary)
        
        # Step 3: Parse date (handle various formats)
        try:
            date = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %Z")
            date_str = date.strftime("%Y-%m-%d %H:%M:%S")
        except:
            # Fallback to current timestamp
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Step 4: Insert into database (with duplicate handling)
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO events (title, city, date, category, source)
                VALUES (?, ?, ?, ?, ?)
            """, (title, city, date_str, category, link))
            
            if cursor.rowcount > 0:
                stats['inserted'] += 1
                print(f"  ✓ [{category}] {city}: {title[:60]}...")
            else:
                stats['duplicates'] += 1
        
        except sqlite3.Error as e:
            print(f"  ✗ Database error: {e}")
            continue
    
    # Commit and close connection
    conn.commit()
    conn.close()
    
    return stats


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function: orchestrates the entire ingestion pipeline.
    
    Pipeline steps:
        1. Fetch RSS articles from Google News
        2. Classify each article by category
        3. Detect city from article text
        4. Store in SQLite database (skip duplicates)
        5. Print statistics
    """
    print("\n" + "="*70)
    print("REAL-TIME NEWS INGESTION PIPELINE")
    print("="*70 + "\n")
    
    # Step 1: Fetch articles
    articles = fetch_rss_articles()
    
    if not articles:
        print("⚠️  No articles fetched. Check your internet connection.")
        return
    
    # Step 2: Process and store
    stats = process_and_store_articles(articles)
    
    # Step 3: Print summary
    print("\n" + "="*70)
    print("INGESTION SUMMARY")
    print("="*70)
    print(f"  Articles processed: {stats['processed']}")
    print(f"  New events inserted: {stats['inserted']}")
    print(f"  Duplicates skipped: {stats['duplicates']}")
    print(f"  Irrelevant skipped: {stats['skipped']}")
    print("="*70 + "\n")
    
    print("✅ Ingestion complete!\n")


if __name__ == "__main__":
    main()
