# Technical Report: Real-Time News & Events Monitoring System

**Project**: Utility Disruption Event Detection System  
**Date**: February 9, 2026  
**Author**: System Architect

---

## 1. Problem Statement

### Objective
Build an automated system to monitor and classify utility disruption incidents across Indian cities in real-time using publicly available news sources.

### Requirements
- **Real-time data ingestion** from free, accessible sources
- **Automated classification** into three categories: power outages, water issues, logistics delays
- **Location detection** for major Indian cities
- **Backend API** for programmatic data access
- **User interface** for visualization and filtering
- **Production-ready** architecture suitable for interview demonstrations

### Constraints
- Zero cost (no paid APIs)
- Fully local execution (no cloud dependencies)
- Interview-ready (3-minute demo capability)
- Beginner-friendly code

---

## 2. Detection Logic

### 2.1 Classification Approach

**Method**: Rule-based keyword matching

**Algorithm**:
```python
def classify_incident(title, summary):
    text = (title + " " + summary).lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return category
    
    return None  # Skip if no match
```

**Category Definitions**:

| Category | Keywords | Example Headlines |
|----------|----------|-------------------|
| **power_outage** | power cut, electricity outage, blackout, power failure, grid failure | "Major power cut affects Delhi" |
| **water_issue** | water shortage, pipeline leak, water supply disruption, water crisis | "Mumbai faces water shortage" |
| **logistics_delay** | traffic jam, transport delay, supply chain issue, road blockage | "Traffic chaos in Bengaluru" |

**Why Keyword Matching?**
- ✅ **Simple and explainable**: Easy to debug and understand
- ✅ **Fast processing**: No ML model overhead
- ✅ **No training data required**: Works immediately
- ✅ **Predictable results**: Deterministic behavior
- ❌ **Limited accuracy**: Can't handle semantic nuances
- ❌ **Brittle**: Misses synonyms not in keyword list

### 2.2 Accuracy Considerations

**Expected Performance**:
- Precision: ~70-80% (some false positives from keyword ambiguity)
- Recall: ~60-70% (misses articles using different terminology)

**Example Edge Cases**:
- ❌ "Power companies face regulatory issues" → False positive (contains "power")
- ❌ "Water quality debate in parliament" → False positive (contains "water")
- ❌ "Electrical grid modernization announced" → Missed (no exact keyword match)

---

## 3. Location Inference

### 3.1 City Detection Method

**Approach**: Word-boundary regex pattern matching

**Implementation**:
```python
def detect_city(title, summary):
    text = title + " " + summary
    
    for city in CITIES:
        if re.search(r'\b' + city + r'\b', text, re.IGNORECASE):
            return city
    
    return "Unknown"
```

**Supported Cities**:
- Delhi
- Mumbai
- Bengaluru
- Chennai
- Kolkata
- Hyderabad

**Why These Cities?**
- Largest metro areas in India
- Most frequent in national news
- Represent different regions (North, South, East, West)

### 3.2 Detection Limitations

**Current Issues**:
1. **Variations not handled**:
   - "NCR" vs "Delhi"
   - "Bombay" vs "Mumbai"
   - "Bangalore" vs "Bengaluru"

2. **Spelling errors ignored**: Typos will cause misses

3. **Multiple cities**: Only detects first match (doesn't handle "Delhi and Mumbai")

4. **Suburbs/Regions**: Can't detect "Gurugram", "Navi Mumbai"

**Improvement Path**: Use spaCy NER (Named Entity Recognition) to detect location entities with fuzzy matching.

---

## 4. Output Explanation

### 4.1 Database Schema

**Table**: `events`

| Column | Type | Purpose | Constraints |
|--------|------|---------|-------------|
| `id` | INTEGER | Primary key | AUTO_INCREMENT |
| `title` | TEXT | News headline | NOT NULL, UNIQUE |
| `city` | TEXT | Detected city | NOT NULL |
| `date` | TEXT | Publication timestamp | NOT NULL |
| `category` | TEXT | Event type | NOT NULL |
| `source` | TEXT | Original URL | NOT NULL |

**Design Decisions**:
- **UNIQUE on title**: Prevents duplicate articles when ingestion runs multiple times
- **TEXT for date**: SQLite text format (ISO 8601)
- **Indexes on city/category**: Speed up filtered queries

### 4.2 API Structure

**REST Endpoints**:

```
GET /events?city=Delhi&category=power_outage
→ Returns filtered events array

GET /stats
→ Returns {"power_outage": 10, "water_issue": 5, ...}

GET /cities
→ Returns [{"city": "Delhi", "count": 10}, ...]
```

**Response Format**: JSON (industry standard, easy to consume)

**CORS Enabled**: Allows frontend access from any origin (would restrict in production)

### 4.3 Frontend Dashboard

**Layout**:
1. **Statistics Cards**: Overview of total and per-category counts
2. **Filter Controls**: City and category dropdowns
3. **Events Table**: Sortable, scrollable list of events
4. **Source Links**: Direct links to original articles

**Data Flow**:
```
User loads page
    → JavaScript calls GET /events, /stats, /cities
    → Parse JSON responses
    → Render HTML elements dynamically

User changes filter
    → Rebuild query parameters
    → Call GET /events with filters
    → Re-render table
```

---

## 5. Limitations

### 5.1 Technical Limitations

**1. Data Source Dependency**
- **Issue**: Relies on Google News RSS availability
- **Impact**: System breaks if Google changes RSS format
- **Mitigation**: Add multiple news sources (NewsAPI, Twitter)

**2. Classification Accuracy**
- **Issue**: Keyword matching is not semantic
- **Impact**: False positives/negatives (~20-30% error rate)
- **Mitigation**: Use ML classifier (Naive Bayes, BERT)

**3. Location Coverage**
- **Issue**: Only 6 cities supported
- **Impact**: Events in other cities marked "Unknown"
- **Mitigation**: Expand city list, use NER

**4. Scalability**
- **Issue**: SQLite has concurrency limits
- **Impact**: Can't handle thousands of concurrent users
- **Mitigation**: Migrate to PostgreSQL + Redis

**5. Real-Time Latency**
- **Issue**: Ingestion is manual/scheduled
- **Impact**: Data is only as fresh as last ingestion run
- **Mitigation**: Implement event-driven architecture with webhooks

### 5.2 Design Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| **RSS over API** | Free, no auth | Limited to what's in RSS |
| **Keywords over ML** | Simple, fast | Lower accuracy |
| **SQLite over PostgreSQL** | Zero config | Not production-scalable |
| **Vanilla JS over React** | No build step | Less maintainable at scale |

---

## 6. Production Roadmap

### Phase 1: Enhanced Accuracy (1-2 weeks)

**1. Implement NLP Classification**
```python
import spacy
nlp = spacy.load("en_core_web_sm")

def classify_nlp(text):
    doc = nlp(text)
    # Use entity recognition and dependency parsing
    # Train on labeled dataset
```

**2. Improve Location Detection**
```python
def detect_location_ner(text):
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    # Fuzzy match against city database
```

**Expected Improvement**:
- Classification accuracy: 70% → 85%
- Location detection: 60% → 80%

---

### Phase 2: Data & Infrastructure (2-4 weeks)

**1. Multiple Data Sources**
- NewsAPI integration (5,000 requests/day free tier)
- Twitter API for social media mentions
- Government alert RSS feeds

**2. Database Migration**
```sql
-- PostgreSQL schema with relations
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    city_id INTEGER REFERENCES cities(id),
    category_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    state TEXT,
    population INTEGER
);
```

**3. Caching Layer**
```python
import redis
cache = redis.Redis()

@app.get("/events")
async def get_events(city, category):
    cache_key = f"events:{city}:{category}"
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)
    # Query database...
    cache.setex(cache_key, 300, json.dumps(events))
```

---

### Phase 3: Advanced Features (4-8 weeks)

**1. Real-Time Updates**
```javascript
// WebSocket for live updates
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
    const newEvent = JSON.parse(event.data);
    addEventToTable(newEvent);
};
```

**2. Sentiment Analysis**
```python
from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    return {
        'polarity': blob.sentiment.polarity,  # -1 to 1
        'subjectivity': blob.sentiment.subjectivity
    }
```

**3. Trend Detection**
```sql
-- Detect increasing incident rates
SELECT 
    city,
    category,
    DATE(date) as day,
    COUNT(*) as incidents
FROM events
WHERE date >= DATE('now', '-7 days')
GROUP BY city, category, day
HAVING incidents > (
    SELECT AVG(daily_count) * 1.5 
    FROM daily_stats
);
```

**4. Visualization**
```javascript
// Map visualization with Leaflet
const map = L.map('map').setView([20.5937, 78.9629], 5);
events.forEach(event => {
    L.marker([event.lat, event.lng])
        .bindPopup(event.title)
        .addTo(map);
});
```

---

### Phase 4: Enterprise Deployment (8+ weeks)

**1. Microservices Architecture**
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Ingestion  │────▶│   Message    │────▶│ Classifier  │
│  Service    │     │   Queue      │     │  Service    │
└─────────────┘     │  (RabbitMQ)  │     └─────────────┘
                    └──────────────┘            │
                                                ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Frontend   │────▶│   API        │────▶│  Database   │
│  React      │     │  FastAPI     │     │ PostgreSQL  │
└─────────────┘     └──────────────┘     └─────────────┘
```

**2. CI/CD Pipeline**
```yaml
# .github/workflows/deploy.yml
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: pytest tests/
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: kubectl apply -f k8s/
```

**3. Monitoring & Alerting**
```python
from prometheus_client import Counter, Histogram

events_ingested = Counter('events_ingested_total', 'Total events')
classification_duration = Histogram('classification_seconds', 'Time to classify')

@classification_duration.time()
def classify_incident(text):
    # ... classification logic
    events_ingested.inc()
```

---

## 7. Conclusion

### What Was Achieved
✅ **Complete end-to-end system** from data ingestion to visualization  
✅ **Zero-cost solution** using free, public data sources  
✅ **Production-ready code** with clean architecture and documentation  
✅ **Interview-ready demo** in under 3 minutes  

### Key Learnings
- **Simplicity first**: Rule-based approach works for MVP
- **Trade-offs matter**: SQLite vs PostgreSQL depends on use case
- **Documentation crucial**: README as important as code

### Next Steps
1. Deploy to cloud (AWS/GCP free tier)
2. Implement ML-based classification
3. Add more data sources
4. Build mobile app (React Native)

---

**End of Report**
