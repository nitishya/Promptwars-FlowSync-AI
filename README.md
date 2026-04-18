# 🏟️ FlowSync AI
**Live Venue Intelligence & Dynamic Crowd Management System**

FlowSync AI is an intelligent backend and dashboard designed to manage crowd density, predict congestion, and optimize routing in large sporting venues and stadiums.

---

## 🚀 Key Features You Built

1. **AI Congestion Prediction:**
   *   Implemented an algorithm that takes snapshots of historical crowd data and uses moving averages to predict what the crowd density will be 10 minutes in the future.
2. **Dynamic Pathfinding (Dijkstra's Algorithm):**
   *   Built a custom graph of the venue. The algorithm finds the shortest physical path between two zones, but dynamically adds "penalty weights" if a hallway is crowded. If a zone hits 5,000+ people, the system marks it as completely impassable.
3. **Queue Wait Time Estimations:**
   *   Implemented Little's Law to accurately estimate wait times at specific service zones (Food Court, Restrooms), capping out with a visual "(FULL CAPACITY)" warning if lines get dangerously long.
4. **Live Asynchronous Simulation:**
   *   Built a background Python worker (`asyncio.sleep`) that constantly simulates live crowd movement so the dashboard always feels alive and realistic.
5. **Resilient Frontend Architecture:**
   *   The UI auto-refreshes every 3 seconds, formats massive numbers dynamically (e.g., `100,000` to `100k`), and features offline detection that turns the screen red if the backend server crashes.

---

## 💻 Technologies & Languages Used

**Backend Core:**
*   **Python 3:** The primary programming language used for all logic, pathfinding, and AI models.
*   **FastAPI:** The high-performance web framework used to build our asynchronous REST API.
*   **Uvicorn:** The ASGI web server that runs the FastAPI application.
*   **Pydantic:** Used to enforce strict data validation and create schemas for API requests/responses.

**Frontend Dashboard:**
*   **HTML5:** Structured the entire dashboard layout.
*   **CSS3 (Vanilla):** We built a completely custom, premium "Glassmorphic" dark-mode theme without relying on heavy frameworks like Tailwind. We used modern CSS Grid and Flexbox for responsiveness.
*   **JavaScript (ES6+):** Wrote pure, vanilla JS to fetch live data from the backend, update the UI asynchronously, and handle edge cases like server disconnections.
*   **SVG Icons:** Used native scalable vector graphics for the footer icons (LinkedIn & GitHub).

**DevOps & Tools:**
*   **Docker:** Created a production-ready `Dockerfile` to containerize the entire application.
*   **Bash Scripting:** Wrote a custom `deploy.sh` script to automate deployment to Google Cloud Run.
*   **Git/GitHub:** Standard version control.

---

## 📂 Architecture & Directory Structure

```text
FlowSync-AI/
├── app/
│   ├── main.py              # Application entry point & startup lifespans
│   ├── api/endpoints.py     # FastAPI REST routers and rate-limiting
│   ├── core/
│   │   ├── ai_model.py      # Trend prediction & Little's Law queue math
│   │   ├── pathfinding.py   # Dijkstra's Algorithm with dynamic crowd weights
│   │   └── simulation.py    # Background asyncio crowd simulation worker
│   ├── db/store.py          # In-memory database and Venue Graph definition
│   ├── models/schemas.py    # Pydantic data schemas
│   └── static/              # Frontend UI assets
│       ├── index.html       # Glassmorphic Dashboard
│       └── restroom_bg.png  # Generated premium background imagery
├── Dockerfile               # Production-ready Docker configuration
├── deploy.sh                # Google Cloud deployment automation
└── requirements.txt         # Python dependencies
```

---

## 💻 Running Locally

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the Server:**
   ```bash
   uvicorn app.main:app --reload --port 8080
   ```
3. **View the Dashboard:**
   Open your browser and navigate to `http://127.0.0.1:8080`

## 🛡️ Edge Cases Handled

*   **API Rate Limiting:** Prevents malicious spamming of the ingest endpoint.
*   **Stale Data Protection:** Prediction models explicitly ignore historical data older than 15 minutes.
*   **Impassable Zones:** Pathfinding actively avoids routes through zones that exceed maximum safe capacity limits.
*   **Frontend Resiliency:** The UI actively detects backend failures, displays error states, and auto-heals when connection is restored.