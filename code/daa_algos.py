def knapsack_fantasy(players, max_budget):
    """
    0/1 Knapsack using Dynamic Programming.
    players: list of dicts [{'id': 'P1', 'name': 'Player 1', 'cost': 8.5, 'value': 120}, ...]
    max_budget: float (e.g. 100.0)
    Returns the maximum value and the list of selected players.
    Note: To use standard DP, we should scale costs to integers.
    """
    # Scale costs by 10 to make them integers (e.g., 8.5 -> 85)
    budget = int(max_budget * 10)
    n = len(players)
    
    # DP table: dp[i][w] represents max value with first i items and weight limit w
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        item_cost = int(players[i-1].get('cost', 0) * 10)
        item_val = players[i-1].get('value', 0)
        
        for w in range(1, budget + 1):
            if item_cost <= w:
                dp[i][w] = max(item_val + dp[i-1][w - item_cost], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
                
    # Backtrack to find selected players
    selected = []
    w = budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(players[i-1])
            w -= int(players[i-1].get('cost', 0) * 10)
            
    return {"max_value": dp[n][budget], "team": selected}

def constrained_knapsack_fantasy(batters, bowlers, wkar, req_bat, req_bowl, req_wkar, max_budget):
    """
    Multi-stage Dynamic Programming for Constrained 0/1 Knapsack.
    Finds exactly req_bat batters, req_bowl bowlers, and req_wkar WKs within max_budget.
    """
    budget = int(max_budget * 10)
    
    def solve_role(players, req_count):
        n = len(players)
        dp = [[[-1] * (budget + 1) for _ in range(req_count + 1)] for __ in range(n + 1)]
        for i in range(n + 1):
            for w in range(budget + 1):
                dp[i][0][w] = 0
                
        for i in range(1, n + 1):
            cost = int(players[i-1].get('cost', 0) * 10)
            val = players[i-1].get('value', 0)
            
            for k in range(1, req_count + 1):
                for w in range(budget + 1):
                    best = dp[i-1][k][w]
                    if cost <= w and dp[i-1][k-1][w-cost] != -1:
                        pick_val = dp[i-1][k-1][w-cost] + val
                        if pick_val > best:
                            best = pick_val
                    dp[i][k][w] = best
        return dp

    def backtrack_role(dp, players, req, final_w):
        selected = []
        curr_req = req
        curr_w = final_w
        for i in range(len(players), 0, -1):
            if curr_req == 0: break
            cost = int(players[i-1].get('cost', 0) * 10)
            if curr_w >= cost and dp[i-1][curr_req-1][curr_w-cost] != -1:
                val = players[i-1].get('value', 0)
                if dp[i][curr_req][curr_w] == dp[i-1][curr_req-1][curr_w-cost] + val:
                    selected.append(players[i-1])
                    curr_req -= 1
                    curr_w -= cost
                    continue
        return selected

    dp_bat = solve_role(batters, req_bat)
    dp_bowl = solve_role(bowlers, req_bowl)
    dp_wkar = solve_role(wkar, req_wkar)
    
    final_bat = dp_bat[-1][req_bat] if req_bat > 0 else [0]*(budget+1)
    final_bowl = dp_bowl[-1][req_bowl] if req_bowl > 0 else [0]*(budget+1)
    final_wkar = dp_wkar[-1][req_wkar] if req_wkar > 0 else [0]*(budget+1)
    
    combined_bb = [-1] * (budget + 1)
    split_bb = [-1] * (budget + 1)
    
    for w in range(budget + 1):
        best_val = -1
        best_w1 = -1
        for w1 in range(w + 1):
            w2 = w - w1
            v1 = final_bat[w1]
            v2 = final_bowl[w2]
            if v1 != -1 and v2 != -1:
                if v1 + v2 > best_val:
                    best_val = v1 + v2
                    best_w1 = w1
        combined_bb[w] = best_val
        split_bb[w] = best_w1
        
    max_val = -1
    best_w_bb = -1
    best_w3 = -1
    
    for w in range(budget + 1):
        for w3 in range(budget + 1 - w):
            v_bb = combined_bb[w]
            v_wkar = final_wkar[w3]
            if v_bb != -1 and v_wkar != -1:
                if v_bb + v_wkar > max_val:
                    max_val = v_bb + v_wkar
                    best_w_bb = w
                    best_w3 = w3
                    
    if max_val == -1:
        return {"error": "Budget too low or not enough players to fill roles"}
        
    w1 = split_bb[best_w_bb]
    w2 = best_w_bb - w1
    w3 = best_w3
    
    team = []
    if req_bat > 0: team.extend(backtrack_role(dp_bat, batters, req_bat, w1))
    if req_bowl > 0: team.extend(backtrack_role(dp_bowl, bowlers, req_bowl, w2))
    if req_wkar > 0: team.extend(backtrack_role(dp_wkar, wkar, req_wkar, w3))
    
    return {"max_value": max_val, "team": team}


def max_subarray_peak(runs_array):
    """
    Maximum Subarray Problem (Kadane's Algorithm) - Divide & Conquer / DP approach.
    Finds the contiguous phase of matches/overs with maximum runs/impact.
    runs_array: list of ints
    Returns the max sum, start index, and end index.
    """
    if not runs_array:
        return {"max_sum": 0, "start": -1, "end": -1}
        
    max_so_far = float('-inf')
    current_max = 0
    start_idx = 0
    end_idx = 0
    temp_start = 0
    
    for i in range(len(runs_array)):
        current_max += runs_array[i]
        
        if current_max > max_so_far:
            max_so_far = current_max
            start_idx = temp_start
            end_idx = i
            
        if current_max < 0:
            current_max = 0
            temp_start = i + 1
            
    return {"max_sum": max_so_far, "start": start_idx, "end": end_idx}


def rabin_karp_search(text, pattern):
    """
    Rabin-Karp String Matching Algorithm.
    Returns the starting indices of all occurrences of pattern in text.
    """
    text = text.lower()
    pattern = pattern.lower()
    n = len(text)
    m = len(pattern)
    if m == 0 or m > n:
        return []
        
    d = 256 # number of characters in the alphabet
    q = 101 # prime number
    
    h = 1
    for i in range(m - 1):
        h = (h * d) % q
        
    p_hash = 0
    t_hash = 0
    
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q
        
    res = []
    
    for i in range(n - m + 1):
        if p_hash == t_hash:
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                res.append(i)
                
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if t_hash < 0:
                t_hash = t_hash + q
                
    return res


def merge_sort_impact(arr, key='impact_score', reverse=True):
    """
    Merge Sort implementation to sort objects based on a specific key.
    Used for sorting players by their dynamically calculated impact score.
    """
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort_impact(L, key, reverse)
        merge_sort_impact(R, key, reverse)

        i = j = k = 0

        while i < len(L) and j < len(R):
            # Compare based on key and reverse flag
            l_val = L[i].get(key, 0)
            r_val = R[j].get(key, 0)
            
            condition = l_val > r_val if reverse else l_val < r_val
            
            if condition:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            
    return arr


# =====================================================================
# PHASE 1: NEW DAA ALGORITHMS (RESUME-WORTHY UPGRADE)
# =====================================================================

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.players = [] # Store references to players that end at this node or match the prefix

class PlayerTrie:
    """
    Prefix Trie for ultra-fast autocomplete. O(M) search time.
    """
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, player_dict):
        # Insert by full name, first name, last name to allow flexible searching
        name = player_dict['name'].lower()
        parts = name.split()
        suffixes = [name] + parts
        
        for word in suffixes:
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                # Store reference in every node along the path for instant prefix retrieval
                if player_dict not in node.players:
                    node.players.append(player_dict)
            node.is_end_of_word = True

    def search_prefix(self, prefix):
        prefix = prefix.lower()
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Sort by impact or runs if needed, but here we just return the list
        return node.players[:15] # Return top 15 matches instantly


from collections import deque

def build_player_graph(partnerships, players_dict):
    """
    Builds an adjacency list graph from partnership data.
    """
    graph = {}
    for p_id in players_dict:
        graph[p_id] = set()
        
    for p in partnerships:
        p1 = p['player1_id']
        p2 = p['player2_id']
        if p1 in graph and p2 in graph:
            graph[p1].add(p2)
            graph[p2].add(p1)
            
    return graph

def shortest_path_bfs(graph, start_id, target_id):
    """
    Breadth-First Search (BFS) to find the shortest path between two players
    in the partnership network (Degrees of Separation).
    """
    if start_id not in graph or target_id not in graph:
        return None
        
    if start_id == target_id:
        return [start_id]
        
    queue = deque([[start_id]])
    visited = set([start_id])
    
    while queue:
        path = queue.popleft()
        current_node = path[-1]
        
        for neighbor in graph.get(current_node, []):
            if neighbor == target_id:
                return path + [neighbor]
                
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
                
    return None # No connection found

# =====================================================================
# PHASE 2: NEW DAA ALGORITHMS (CRICALGO PIVOT)
# =====================================================================

import math
import heapq

# 1. Quick Sort (Unit 2 - Divide & Conquer)
def quick_sort_players(arr, key='no_of_totalruns', reverse=True):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2].get(key, 0)
    left = []
    middle = []
    right = []
    for x in arr:
        val = x.get(key, 0)
        if (val > pivot if reverse else val < pivot):
            left.append(x)
        elif val == pivot:
            middle.append(x)
        else:
            right.append(x)
    return quick_sort_players(left, key, reverse) + middle + quick_sort_players(right, key, reverse)

# 2. Convex Hull - Monotone Chain (Unit 2 - Divide & Conquer)
def convex_hull(players):
    """
    Computes the convex hull of a set of 2D points (strike_rate, average).
    Players must have 'sr' and 'bat_avg'.
    """
    if len(players) <= 3:
        return players

    # Sort the points lexicographically (first by x, then by y)
    pts = sorted(players, key=lambda p: (p.get('sr', 0), p.get('bat_avg', 0)))

    # 2D cross product of OA and OB vectors
    def cross(o, a, b):
        return (a.get('sr',0) - o.get('sr',0)) * (b.get('bat_avg',0) - o.get('bat_avg',0)) - \
               (a.get('bat_avg',0) - o.get('bat_avg',0)) * (b.get('sr',0) - o.get('sr',0))

    # Build lower hull
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    return lower[:-1] + upper[:-1]

# 3. Floyd-Warshall (Unit 4 - Graph Algorithms)
def floyd_warshall_dominance(teams, matches):
    """
    teams: list of team names
    matches: list of dicts with team_1_name, team_2_name, winner, win_margin
    Computes shortest path dominance matrix.
    """
    dist = {t: {t2: float('inf') for t2 in teams} for t in teams}
    for t in teams:
        dist[t][t] = 0

    # Build initial graph from matches
    for m in matches:
        w = m.get('winner')
        l = m.get('loser')
        if not w or not l or w == 'No Result': continue
        if w in teams and l in teams:
            dist[w][l] = 1 # 1 step of dominance
            
    # Floyd Warshall
    for k in teams:
        for i in teams:
            for j in teams:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    return dist

# 4. Huffman Coding (Unit 3 - Greedy)
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def huffman_encoding(frequencies):
    """
    frequencies: dict of {dismissal_type: count}
    Returns a dict with the binary codes and the tree structure.
    """
    if not frequencies: return {}, None
    
    heap = [HuffmanNode(k, v) for k, v in frequencies.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
        
    root = heap[0]
    codes = {}
    
    def generate_codes(node, current_code):
        if node is None: return
        if node.char is not None:
            codes[node.char] = current_code
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")
        
    generate_codes(root, "")
    
    def serialize(node):
        if not node: return None
        return {
            "name": node.char if node.char else f"({node.freq})",
            "value": node.freq,
            "children": [serialize(node.left), serialize(node.right)] if node.left or node.right else []
        }
        
    def clean_tree(tree):
        if not tree: return tree
        tree['children'] = [clean_tree(c) for c in tree['children'] if c is not None]
        return tree
        
    return codes, clean_tree(serialize(root))

# 5. Greedy Fantasy (Unit 3 - Greedy vs DP)
def greedy_fantasy(batters, bowlers, wkar, req_bat, req_bowl, req_wkar, max_budget):
    """
    Greedy approach: Always pick the highest value player first, checking budget and role constraints.
    """
    budget = max_budget
    team = []
    
    bat_sorted = sorted(batters, key=lambda x: x.get('value', 0), reverse=True)
    bowl_sorted = sorted(bowlers, key=lambda x: x.get('value', 0), reverse=True)
    wkar_sorted = sorted(wkar, key=lambda x: x.get('value', 0), reverse=True)
    
    b_idx, bo_idx, wk_idx = 0, 0, 0
    
    while b_idx < len(bat_sorted) and req_bat > 0:
        p = bat_sorted[b_idx]
        if p['cost'] <= budget:
            team.append(p)
            budget -= p['cost']
            req_bat -= 1
        b_idx += 1
        
    while bo_idx < len(bowl_sorted) and req_bowl > 0:
        p = bowl_sorted[bo_idx]
        if p['cost'] <= budget:
            team.append(p)
            budget -= p['cost']
            req_bowl -= 1
        bo_idx += 1
        
    while wk_idx < len(wkar_sorted) and req_wkar > 0:
        p = wkar_sorted[wk_idx]
        if p['cost'] <= budget:
            team.append(p)
            budget -= p['cost']
            req_wkar -= 1
        wk_idx += 1
        
    return {"max_value": sum(p.get('value',0) for p in team), "team": team}

# 6. K-Means Clustering (Machine Learning / Advanced Algorithms)
import random

def k_means_clustering(players, k=3, max_iters=100):
    """
    Groups batters into k clusters based on normalized Strike Rate and Batting Average.
    """
    if not players or len(players) < k:
        return players

    # Extract features and normalize them to 0-1 range to avoid skew
    sr_vals = [p.get('sr', 0) for p in players]
    avg_vals = [p.get('bat_avg', 0) for p in players]
    
    max_sr = max(sr_vals) if max(sr_vals) > 0 else 1
    max_avg = max(avg_vals) if max(avg_vals) > 0 else 1

    for p in players:
        p['norm_sr'] = p.get('sr', 0) / max_sr
        p['norm_avg'] = p.get('bat_avg', 0) / max_avg

    # Initialize centroids randomly from the dataset
    centroids = random.sample([{'norm_sr': p['norm_sr'], 'norm_avg': p['norm_avg']} for p in players], k)
    
    def dist(p1, c2):
        return math.sqrt((p1['norm_sr'] - c2['norm_sr'])**2 + (p1['norm_avg'] - c2['norm_avg'])**2)

    clusters = []
    for _ in range(max_iters):
        # Assign players to nearest centroid
        clusters = [[] for _ in range(k)]
        for p in players:
            distances = [dist(p, c) for c in centroids]
            closest_k = distances.index(min(distances))
            clusters[closest_k].append(p)
            
        # Recalculate centroids
        new_centroids = []
        for i in range(k):
            if not clusters[i]:
                new_centroids.append(centroids[i])
                continue
            avg_sr = sum(p['norm_sr'] for p in clusters[i]) / len(clusters[i])
            avg_avg = sum(p['norm_avg'] for p in clusters[i]) / len(clusters[i])
            new_centroids.append({'norm_sr': avg_sr, 'norm_avg': avg_avg})
            
        # Check convergence
        converged = True
        for i in range(k):
            if abs(centroids[i]['norm_sr'] - new_centroids[i]['norm_sr']) > 0.001 or \
               abs(centroids[i]['norm_avg'] - new_centroids[i]['norm_avg']) > 0.001:
                converged = False
                break
                
        centroids = new_centroids
        if converged:
            break

    # Assign meaningful labels based on cluster characteristics
    # E.g. highest SR = Aggressors, highest Avg but lower SR = Anchors
    labeled_clusters = []
    for i, cluster in enumerate(clusters):
        if not cluster: continue
        avg_raw_sr = sum(p.get('sr',0) for p in cluster) / len(cluster)
        avg_raw_avg = sum(p.get('bat_avg',0) for p in cluster) / len(cluster)
        
        # Simple heuristic for labels
        if avg_raw_sr > 130 and avg_raw_avg > 30:
            role = "Elite Finishers"
        elif avg_raw_sr > 120:
            role = "Aggressors"
        elif avg_raw_avg > 35:
            role = "Anchors"
        else:
            role = "Strugglers"
            
        for p in cluster:
            p['cluster_role'] = role
            p['cluster_id'] = i
            
        labeled_clusters.extend(cluster)
        
    return labeled_clusters

# 7. Queue Simulation (Match Timeline / Worm Graph)
def simulate_match_worm(innings_data):
    """
    Simulates an over-by-over worm graph using a Queue.
    Since we only have phase data (PP, Mid, Death), we distribute those runs across overs.
    Returns the synthetic timeline for both innings.
    """
    from collections import deque
    
    worm_data = []
    
    for inn in innings_data:
        team = inn.get('batting_team', 'Unknown')
        
        # Distribute phase data
        pp_runs = inn.get('pp_runs', 0)
        mid_runs = inn.get('mid_runs', 0)
        death_runs = inn.get('death_runs', 0)
        
        pp_wkts = inn.get('pp_wickets', 0)
        mid_wkts = inn.get('mid_wickets', 0)
        death_wkts = inn.get('death_wickets', 0)
        
        # We simulate over-by-over events and push to queue
        event_queue = deque()
        
        # Powerplay (1-10)
        for o in range(1, 11):
            runs = pp_runs // 10 if o < 10 else pp_runs - (pp_runs // 10 * 9)
            wkt = 1 if o <= pp_wkts else 0
            event_queue.append({"over": o, "runs": max(0, runs), "wicket": wkt})
            
        # Middle (11-40)
        for o in range(11, 41):
            runs = mid_runs // 30 if o < 40 else mid_runs - (mid_runs // 30 * 29)
            wkt = 1 if (o - 10) <= mid_wkts and (o % 3 == 0) else 0 # Distribute wickets a bit
            event_queue.append({"over": o, "runs": max(0, runs), "wicket": wkt})
            
        # Death (41-50)
        for o in range(41, 51):
            runs = death_runs // 10 if o < 50 else death_runs - (death_runs // 10 * 9)
            wkt = 1 if (o - 40) <= death_wkts else 0
            event_queue.append({"over": o, "runs": max(0, runs), "wicket": wkt})
            
        # Process queue to build cumulative timeline
        cumulative_runs = 0
        cumulative_wkts = 0
        timeline = [{"over": 0, "total_runs": 0, "total_wickets": 0, "runs_this_over": 0, "wicket_fell": False}]
        
        while event_queue:
            event = event_queue.popleft()
            cumulative_runs += event['runs']
            cumulative_wkts += event['wicket']
            
            if cumulative_wkts > 10: 
                cumulative_wkts = 10
                
            timeline.append({
                "over": event['over'],
                "total_runs": cumulative_runs,
                "total_wickets": cumulative_wkts,
                "runs_this_over": event['runs'],
                "wicket_fell": event['wicket'] > 0
            })
            
            # Stop if all out
            if cumulative_wkts == 10:
                break
            
        worm_data.append({
            "team": team,
            "timeline": timeline
        })
        
    return worm_data
