"""
Demo Data Insertion Script
===========================

Purpose:
    Insert 100+ realistic demo news items into the events database
    for testing and demonstration purposes.

Usage:
    python db/insert_demo_data.py
"""

import sqlite3
from datetime import datetime, timedelta
import random

# Database path
DATABASE_PATH = "db/events.db"

# Indian cities
CITIES = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata", "Hyderabad"]

# Categories
CATEGORIES = ["power_outage", "water_issue", "logistics_delay"]

# Demo news templates
DEMO_NEWS = {
    "power_outage": [
        "{city}: Major power outage affects {area} locality - {duration} hours without electricity",
        "{city}: Transformer failure causes blackout in {area} area",
        "{city}: Scheduled power maintenance in {area} disrupts supply",
        "{city}: Power grid failure leaves {area} in darkness",
        "{city}: Electricity supply interrupted in {area} due to technical fault",
        "{city}: Mass power cut in {area} - residents face hardship",
        "{city}: {area} experiences prolonged power outage",
        "{city}: Emergency repairs cause power disruption in {area}",
        "{city}: Substation breakdown affects {area} residents",
        "{city}: {area} witnesses unexpected power failure",
        "{city}: Heavy rains cause power outage in {area}",
        "{city}: Cable damage leads to blackout in {area}",
        "{city}: Load shedding implemented in {area} locality",
        "{city}: Circuit breaker malfunction disrupts power in {area}",
        "{city}: {area} area faces electricity crisis",
        "{city}: Power supply restoration delayed in {area}",
        "{city}: {area} residents protest against frequent outages",
        "{city}: Maintenance work causes power cut in {area}",
        "{city}: Electrical fire disrupts supply in {area}",
        "{city}: {area} industrial zone experiences power failure",
    ],
    "water_issue": [
        "{city}: Water shortage hits {area} - residents queue for tankers",
        "{city}: Pipeline burst in {area} disrupts water supply",
        "{city}: {area} to face water cut for {duration} hours",
        "{city}: Contaminated water supply reported in {area}",
        "{city}: {area} residents complain of low water pressure",
        "{city}: Major water crisis in {area} locality",
        "{city}: Pipeline maintenance affects {area} water supply",
        "{city}: {area} area faces acute water shortage",
        "{city}: Pump failure causes water disruption in {area}",
        "{city}: {area} residents struggle with irregular water supply",
        "{city}: Water tanker services increased in {area}",
        "{city}: {area} experiences complete water outage",
        "{city}: Main pipeline repair work affects {area}",
        "{city}: {area} faces drinking water scarcity",
        "{city}: Water treatment plant issue impacts {area}",
        "{city}: {area} locality protests water shortage",
        "{city}: Emergency water rationing in {area}",
        "{city}: {area} area gets contaminated tap water",
        "{city}: Valve breakdown disrupts {area} water supply",
        "{city}: {area} residents demand better water infrastructure",
    ],
    "logistics_delay": [
        "{city}: Traffic jam on {area} route causes major delays",
        "{city}: Road construction in {area} disrupts logistics",
        "{city}: {area} experiences severe transport delays",
        "{city}: Accident on {area} highway blocks goods movement",
        "{city}: Strike action causes logistics disruption in {area}",
        "{city}: Heavy rains delay deliveries in {area}",
        "{city}: {area} road blockage affects supply chain",
        "{city}: Port operations delayed at {area}",
        "{city}: {area} warehouse faces inventory delays",
        "{city}: Transport workers protest in {area}",
        "{city}: {area} experiences fuel shortage affecting logistics",
        "{city}: Bridge under repair delays {area} deliveries",
        "{city}: {area} area faces courier service disruption",
        "{city}: Freight movement slow at {area} junction",
        "{city}: {area} distribution center reports delays",
        "{city}: Vehicle breakdown causes {area} logistics issues",
        "{city}: {area} customs clearance delays shipments",
        "{city}: Bad weather disrupts {area} transport services",
        "{city}: {area} road maintenance causes delivery delays",
        "{city}: Supply chain bottleneck reported in {area}",
    ]
}

# Area/locality names for templates
AREAS = [
    "Connaught Place", "Andheri", "Koramangala", "T Nagar", "Salt Lake",
    "Banjara Hills", "Karol Bagh", "Powai", "Whitefield", "Adyar",
    "Park Street", "Jubilee Hills", "Malviya Nagar", "Goregaon", "HSR Layout",
    "Mylapore", "New Town", "Madhapur", "Vasant Kunj", "Borivali",
    "Indiranagar", "Vadapalani", "Rajarhat", "Gachibowli", "Dwarka",
    "Thane", "Electronic City", "Anna Nagar", "Dum Dum", "Hitech City",
    "Rohini", "Bandra", "JP Nagar", "Nungambakkam", "Howrah",
    "Secunderabad", "Saket", "Churchgate", "Jayanagar", "Porur",
    "Sealdah", "Ameerpet", "Greater Kailash", "Dadar", "BTM Layout"
]

def generate_demo_news(num_items=120):
    """Generate demo news items"""
    news_items = []
    base_date = datetime.now()
    
    # Generate news from the past 30 days
    for i in range(num_items):
        category = random.choice(CATEGORIES)
        city = random.choice(CITIES)
        area = random.choice(AREAS)
        duration = random.choice([2, 3, 4, 6, 8, 12, 24])
        
        # Pick a template and format it
        template = random.choice(DEMO_NEWS[category])
        title = template.format(city=city, area=area, duration=duration)
        
        # Random date within past 30 days
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        event_date = base_date - timedelta(days=days_ago, hours=hours_ago)
        date_str = event_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate a dummy source URL
        source = f"https://news.google.com/articles/{random.randint(100000, 999999)}"
        
        news_items.append({
            "title": title,
            "city": city,
            "date": date_str,
            "category": category,
            "source": source
        })
    
    return news_items

def insert_demo_data():
    """Insert demo data into database"""
    print("Generating demo news items...")
    news_items = generate_demo_news(120)
    
    print(f"Connecting to database: {DATABASE_PATH}")
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("Clearing existing data...")
    cursor.execute("DELETE FROM events")
    
    print(f"Inserting {len(news_items)} demo news items...")
    inserted_count = 0
    skipped_count = 0
    
    for item in news_items:
        try:
            cursor.execute("""
                INSERT INTO events (title, city, date, category, source)
                VALUES (?, ?, ?, ?, ?)
            """, (item["title"], item["city"], item["date"], item["category"], item["source"]))
            inserted_count += 1
        except sqlite3.IntegrityError:
            # Skip duplicates (in case title already exists)
            skipped_count += 1
            continue
    
    conn.commit()
    
    # Verify insertion
    cursor.execute("SELECT COUNT(*) FROM events")
    total_count = cursor.fetchone()[0]
    
    print("\n" + "="*70)
    print("✅ Demo Data Insertion Complete!")
    print("="*70)
    print(f"Inserted: {inserted_count} news items")
    print(f"Skipped:  {skipped_count} duplicates")
    print(f"Total:    {total_count} events in database")
    print("="*70)
    
    # Show sample data by category
    print("\nSample data by category:")
    cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM events
        GROUP BY category
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} events")
    
    print("\nSample data by city:")
    cursor.execute("""
        SELECT city, COUNT(*) as count
        FROM events
        GROUP BY city
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} events")
    
    conn.close()
    print("\n🎉 Done! You can now view the data at http://localhost:8000")

if __name__ == "__main__":
    insert_demo_data()
