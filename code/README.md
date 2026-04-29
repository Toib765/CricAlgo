# CricAlgo

A comprehensive, full-stack Cricket Statistics Web Application powered by Flask. This project goes beyond basic CRUD operations by integrating advanced Data Structures and Algorithms (DAA) to provide deep analytics, fantasy team suggestions, and complex data visualizations.

## Features

- **Core Dashboard:** View current standings, tournament summaries, matches, top batters, top bowlers, toss impact, and ground statistics.
- **Player & Team Profiles:** Detailed statistics on players and teams, including recent form, moving averages, head-to-head records, and top partnerships.
- **Live Match Data:** Integrates with external APIs (CricketData.org, Cricbuzz, ESPNcricinfo via RapidAPI) to fetch live scores, recent match results, and ICC standings. Includes a local caching mechanism to minimize API calls.
- **Admin Panel:** Secure admin interface to manage and update matches, teams, and player statistics manually.

## Advanced Analytics (Custom Implementations)

This application implements several custom algorithms from scratch to power complex data analysis features without relying heavily on external libraries:

- **Fantasy Team Engine (0/1 Knapsack & DP):** Uses constrained Dynamic Programming to build the most mathematically valuable fantasy cricket team within a strict budget, adhering to real-world role requirements (batters, bowlers, all-rounders).
- **Peak Phase Analysis (Kadane's Algorithm):** Employs the Maximum Subarray algorithm across a player's historical match data to identify their most prolific run-scoring phase.
- **Lightning-Fast Autocomplete (Prefix Trie):** Uses a custom Trie data structure to provide instant, sub-millisecond autocomplete suggestions when searching for players, bypassing slow database `LIKE` queries.
- **Player Network (BFS Shortest Path):** Builds an adjacency list graph of batting partnerships and uses Breadth-First Search to find the "degrees of separation" between any two players.
- **Dynamic Impact Ranking (Merge Sort):** Calculates a complex "Impact Score" on the fly (weighing strike rates and bowling economies) and uses Merge Sort to rank players efficiently.
- **Deep Search (Rabin-Karp):** Implements Rabin-Karp string matching to perform efficient substring searches across thousands of player and team records simultaneously.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript (Vanilla JS, likely using templates)
- **External APIs:** RapidAPI (Cricbuzz, ESPNcricinfo), CricketData.org

## Setup & Installation

1. **Clone the repository.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Keys:**
   - Ensure your `config.py` contains the required `SECRET_KEY`, `ADMIN_USER`, `ADMIN_PASS`, `CRICDATA_KEY`, and `RAPIDAPI_KEY`.
4. **Initialize the Database:**
   If the database (`champions_trophy.db`) does not exist, run the initialization script:
   ```bash
   python init_db.py
   ```
   *Optionally, populate initial stats with `python populate_stats.py` if available.*
5. **Run the Application:**
   ```bash
   python app.py
   ```
   Alternatively, you can run the provided batch script on Windows:
   ```cmd
   run.bat
   ```
6. **Access the App:** Open your browser and navigate to `http://localhost:5000`.

## Project Structure

- `app.py`: Main Flask application, routing, and API endpoints.
- `api_fetcher.py`: Handles requests to external cricket APIs with built-in caching.
- `daa_algos.py`: Contains all the custom Data Structures and Algorithms implementations.
- `init_db.py`: Script to create the SQLite database schema.
- `db.py`: Database connection and query execution utilities.
- `templates/`: HTML templates for the frontend.
- `cache/`: Directory storing cached JSON responses from external APIs.

## License

This project is open-source and available for educational and personal use.
