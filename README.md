# 🏏 CricAlgo — ICC Champions Trophy 2025 DAA Dashboard

A full-stack cricket analytics web app for the **ICC Champions Trophy 2025**, built with **Flask**, **SQLite**, and **Chart.js** — demonstrating **6 DAA algorithms** on real tournament data.

## Project Members

1. [Toib Fayaz] — RA2411030030061
2. [Ujjawal Sharma] — RA2411030030054

## 📁 Project Documents

| Sr | Description | Link |
|----|-------------|------|
| 1 | Project Code | [View](https://github.com/Toib765/CricAlgo/tree/main/code) |
| 2 | Project Report (DAA) | [View](https://github.com/Toib765/CricAlgo/blob/main/CT25_DAA_Report.docx) |
| 3 | Final PPT | [View](https://github.com/Toib765/CricAlgo/blob/main/CricAlgo_DAA_Presentation.pdf) |

## 🧠 DAA Algorithms Implemented

| # | Algorithm | Unit | Complexity | Dashboard Feature |
|---|-----------|------|------------|-------------------|
| 1 | **Prefix Trie** | U1 — Algorithm Design | O(M) lookup | Global search autocomplete |
| 2 | **BFS on Graph** | U4 — Graph Algorithms | O(V + E) | Player network degrees of separation |
| 3 | **Merge Sort** | U2 — Divide & Conquer | O(N log N) | Sort-by-Impact leaderboard |
| 4 | **Kadane's Algorithm** | U2 — Dynamic Programming | O(N) | Peak form phase detection |
| 5 | **Rabin-Karp** | U5 — String Matching | O(N+M) avg | Deep substring player search |
| 6 | **0/1 Knapsack DP** | U3 — Dynamic Programming | O(N·W) | Fantasy squad auto-fill |

## Features

| Tab | Description |
|-----|-------------|
| 📊 **Overview** | Tournament summary — runs, wickets, sixes, champion, top scorer & bowler |
| 🏅 **Standings** | Group A & B tables with captain, coach, and wicket-keeper |
| 🏟️ **Matches** | All 15 matches; click any for innings breakdown, partnerships & performers |
| 👤 **Players** | Phase splits, wicket types, handedness, Kadane peak form window |
| 📈 **Analytics** | Toss impact, Convex Hull elite batters, Huffman coding, Floyd-Warshall matrix |
| ⚡ **Phase Analysis** | PP / middle / death overs batting & bowling leaderboards |
| 🌍 **Grounds** | Venue stats — avg score, bat/field win rates, pitch type |
| 🤝 **Partnerships** | Top 10 batting stands + BFS player network tool |
| 📡 **Live** | Real-time scores via Cricbuzz API (RapidAPI) with SQLite fallback |
| 🧩 **Fantasy Team** | DP Knapsack squad builder vs Greedy comparison |
| 🔐 **Admin Panel** | Login-protected panel to add/update matches, players, and stats |

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3 + Flask |
| **Database** | SQLite 3 |
| **Frontend** | HTML5 + Vanilla JavaScript |
| **Charts** | Chart.js |
| **External APIs** | CricketData.org · Cricbuzz (RapidAPI) |
| **PDF** | jsPDF (client-side) |

## Quick Setup

### 1. Prerequisites
- Python 3.8+
- pip

### 2. Clone the Repository
```bash
git clone https://github.com/Toib765/ICC-Champions-Trophy-2025.git
cd ICC-Champions-Trophy-2025/Project
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
```bash
cp config.example.py config.py
```

Edit `config.py` and fill in your keys:

| Key | Where to Get It |
|-----|-----------------|
| `CRICDATA_KEY` | [cricketdata.org/member.aspx](https://cricketdata.org/member.aspx) — free, 100 hits/day |
| `RAPIDAPI_KEY` | [rapidapi.com](https://rapidapi.com) — free account → API Key |

### 5. Initialize the Database
```bash
python init_db.py
```
Seeds 8 teams, ~30 players, 15 matches, 30 innings, partnerships, and all player stats.

### 6. Run the App
```bash
python app.py
```
Open **http://localhost:5000** in your browser.

> **Windows:** Double-click `run.bat` to auto-initialize and start the server.

## Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| **Admin** | `toib` | `toib123` |

> ⚠️ Change these in `config.py` before sharing or deploying.

## Project Structure

```
ct25-dashboard/
├── app.py              # Flask server — 30+ REST API routes
├── daa_algos.py        # All 6 DAA algorithm implementations
├── db.py               # SQLite helpers (query + execute)
├── api_fetcher.py      # External API calls + TTL cache
├── init_db.py          # DB schema and seed data (run once)
├── config.py           # API keys & admin password (DO NOT COMMIT)
├── config.example.py   # Template — copy to config.py
├── requirements.txt    # Python dependencies
├── run.bat             # Windows one-click launcher
└── templates/
    ├── index.html      # Main dashboard SPA (10 tabs)
    ├── admin.html      # Admin control panel
    └── login.html      # Admin login page
```

## Database Schema

**12 tables · 6 SQL views · 1 trigger · 1 window function view**

### Core Tables

| Table | Key Columns |
|-------|-------------|
| `STADIUM` | stadium_name PK, city, capacity, ends, pitch_type |
| `TEAM` | team_id PK, group_name, no_of_wins, no_of_loses |
| `PLAYER` | 35 columns — aggregates, phase splits, wicket breakdown, vs-handedness |
| `MATCHES` | match_id PK, toss_winner, winner, win_type, stadium_name FK |
| `INNINGS` | match_id FK, pp/mid/death runs & wickets per innings |
| `PLAYER_MATCH_STATS` | per-player per-match batting + bowling figures |
| `PARTNERSHIP` | player1_id FK, player2_id FK, runs, balls, wicket_no |
| `CAPTAIN` | team_id FK, captain_name |
| `COACH` | team_id FK, coach_name |
| `WICKET_KEEPER` | team_id FK, wk_name |
| `UMPIRE` | umpire_id PK, umpire_name, country |
| `api_cache` | cache_key PK, data JSON, fetched_at timestamp |

### SQL Views

| View | Purpose |
|------|---------|
| `vw_TopRunScorers` | Ranked batters by total runs |
| `vw_TopWicketTakers` | Ranked bowlers with economy and best figures |
| `vw_TossImpact` | Win rates by toss decision |
| `vw_GroundStats` | Per-venue averages and win rates |
| `vw_PhaseStats` | Per-player phase-wise strike rates |
| `vw_PlayerMatchForm` | Match-by-match form per player |
| `vw_MovingAverage` | 5-match rolling average (SQL window function) |

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/summary` | Tournament overview |
| GET | `/api/standings` | Group standings |
| GET | `/api/matches` | All 15 matches |
| GET | `/api/match/<id>` | Innings, partnerships & performers |
| GET | `/api/player/<id>` | Player profile + Kadane peak form |
| GET | `/api/top_batters` | Top 10 run scorers |
| GET | `/api/top_bowlers` | Top 10 wicket takers |
| GET | `/api/phase_stats` | Phase-wise leaderboard |
| GET | `/api/ground_stats` | Venue stats |
| GET | `/api/best_partnerships` | Top 10 batting stands |
| GET | `/api/head_to_head?t1=X&t2=Y` | Team vs. team history |
| GET | `/api/live` | Live scores (Cricbuzz → SQLite fallback) |
| GET | `/api/search_trie?q=` | Trie autocomplete — O(M) |
| GET | `/api/search_deep?q=` | Rabin-Karp deep search |
| GET | `/api/players/impact_sort` | Merge Sort by impact score |
| GET | `/api/player_network/path` | BFS shortest path |
| GET | `/api/fantasy/autofill` | 0/1 Knapsack optimal squad |
| POST | `/api/add_match` *(admin)* | Add or update a match |
| POST | `/api/update_player` *(admin)* | Overwrite all player stats |

## GitHub Safety

Ensure `.gitignore` contains:
```
champions_trophy.db
config.py
__pycache__/
*.pyc
```
> Never commit `config.py` — only `config.example.py`.

---

*Toib Fayaz · Ujjawal Sharma · SRM Institute of Science and Technology, Delhi NCR · 4th Semester DAA Project · 2025*
