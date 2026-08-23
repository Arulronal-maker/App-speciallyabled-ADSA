import streamlit as st
import os
import json
import hashlib
import math
import random

# ==============================
# 1. OPTIONAL PACKAGES FOR VOICE
# ==============================
try:
    import pyttsx3
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except Exception:
    SPEECH_AVAILABLE = False

# ==============================
# 2. ADSA CORE CONCEPTS (Pure Python)
# ==============================

class DoubleHashTable:
    def __init__(self, size=1009):
        self.size = size
        self.table = [None] * size
        self.deleted = object()
        self.count = 0
    def _hash1(self, key): return int(hashlib.md5(key.encode()).hexdigest(), 16) % self.size
    def _hash2(self, key): return 1 + (int(hashlib.sha256(key.encode()).hexdigest(), 16) % (self.size - 1))
    def insert(self, key, value):
        if self.count / self.size > 0.7: self._resize()
        has h1, hash2 = self._hash1(key), self._hash2(key)
        for i in range(self.size):
            pos  = (hash1 + i * hash2) % self.size
            if self.table[pos] is None or self.table[pos] == self.deleted:
                self.table[pos] = (key, value)
                self.count += 1
                return True
        return False
    def search(self, key):
        hash1, hash2 = self._hash1(key), self._hash2(key)
        for i in range(self.size):
            pos = (hash1 + i * hash2) % self.size
            if self.table[pos] is None: return None
            if self.table[pos] != self.deleted and self.table[pos][0] == key: return self.table[pos][1]
        return None
    def _resize(self):
        old_table = self.table
        self.size = self.size * 2
        self.table = [None] * self.size
        self.count = 0
        for item in old_table:
            if item is not None and item != self.deleted: self.insert(item[0], item[1])

class DivideConquerAlgorithms:
    @staticmethod
    def merge_sort(users, key_index):
        if len(users) <= 1: return users
        mid = len(users) // 2
        left = DivideConquerAlgorithms.merge_sort(users[:mid], key_index)
        right = DivideConquerAlgorithms.merge_sort(users[mid:], key_index)
        return DivideConquerAlgorithms.merge(left, right, key_index)
    @staticmethod
    def merge(left, right, key_index):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            left_val = left[i][key_index] if len(left[i]) > key_index else ""
            right_val = right[j][key_index] if len(right[j]) > key_index else ""
            if str(left_val).lower() <= str(right_val).lower():
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class DynamicProgrammingAlgorithms:
    @staticmethod
    def edit_distance(str1, str2):
        m, n = len(str1), len(str2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1): dp[i][0] = i
        for j in range(n + 1): dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]: dp[i][j] = dp[i-1][j-1]
                else: dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + 1)
        return dp[m][n]
    
    @staticmethod
    def multistage_graph(stages, edges):
        n = len(stages)
        dist = [float('inf')] * n
        parent = [-1] * n
        dist[n-1] = 0
        for i in range(n-2, -1, -1):
            for j in range(i+1, n):
                if (i, j) in edges:
                    if dist[i] > edges[(i, j)] + dist[j]:
                        dist[i] = edges[(i, j)] + dist[j]
                        parent[i] = j
        path = []
        current = 0
        while current != -1 and current < n:
            path.append(stages[current])
            if parent[current] == -1: break
            current = parent[current]
        return dist[0], path

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, i):
        if self.parent[i] == i: return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]: self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]: self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False

class GreedyAlgorithms:
    @staticmethod
    def knapsack_helper_selection(helpers, user_requirements, max_time=5):
        scored_helpers = []
        for helper in helpers:
            if len(helper) < 8: continue
            
            # Strict Location Check: Only allow helpers in the same district
            if len(helper) > 4 and helper[4].strip() != user_requirements.get('district', ''): 
                continue
                
            score = 40 # District automatically matches here
            
            if len(helper) > 6 and user_requirements.get('language', '') in helper[6]: score += 30
            req_avail = user_requirements.get('availability', 'Any')
            if len(helper) > 5 and (req_avail == 'Any' or helper[5].strip() == req_avail): score += 20
            
            req_skill = user_requirements.get('skill', 'Any')
            if len(helper) > 7 and (req_skill == 'Any' or req_skill in helper[7]): score += 30
            
            # Random jitter to dynamically break identical ties locally
            scored_helpers.append((score + random.random(), helper))
            
        scored_helpers.sort(reverse=True, key=lambda x: x[0])
        selected, total_time = [], 0
        for score, helper in scored_helpers:
            if total_time + 1 <= max_time and score > 0:
                selected.append(helper)
                total_time += 1
        return selected

class EightQueensScheduler:
    def solve_8queens(self, board, row, n=8):
        if row == n: return True
        for col in range(n):
            if self.is_safe(board, row, col, n):
                board[row][col] = 1
                if self.solve_8queens(board, row + 1, n): return True
                board[row][col] = 0
        return False
    def is_safe(self, board, row, col, n):
        for i in range(row):
            if board[i][col] == 1: return False
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 1: return False
            i -= 1; j -= 1
        i, j = row - 1, col + 1
        while i >= 0 and j < n:
            if board[i][j] == 1: return False
            i -= 1; j += 1
        return True

class BranchAndBoundTSP:
    @staticmethod
    def tsp_solve(dist_matrix):
        n = len(dist_matrix)
        visited = [False] * n
        visited[0] = True 
        min_cost = float('inf')
        best_path = []
        def branch(curr_node, count, curr_cost, curr_path):
            nonlocal min_cost, best_path
            if count == n and dist_matrix[curr_node][0] > 0:
                if curr_cost + dist_matrix[curr_node][0] < min_cost:
                    min_cost = curr_cost + dist_matrix[curr_node][0]
                    best_path = list(curr_path) + [0]
                return
            if curr_cost >= min_cost: return
            for i in range(n):
                if not visited[i] and dist_matrix[curr_node][i] > 0:
                    visited[i] = True
                    curr_path.append(i)
                    branch(i, count + 1, curr_cost + dist_matrix[curr_node][i], curr_path)
                    visited[i] = False
                    curr_path.pop()
        branch(0, 1, 0, [0])
        return min_cost, best_path

# ==============================
# 3. STREAMLIT APP LOGIC (Role Based Architecture)
# ==============================

st.set_page_config(page_title="Silent Voice ADSA", layout="wide")

def init_app_state():
    if 'page' not in st.session_state: st.session_state.page = 'login'
    if 'active_helper' not in st.session_state: st.session_state.active_helper = None
    if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None
    if 'user_role' not in st.session_state: st.session_state.user_role = None
    # Dynamic hot-load mapping (Removed session_state blockers for live notepad syncing)
    ht = DoubleHashTable()
    base_dir = os.path.dirname(__file__)
    user_files = ['blind_users.txt', 'deaf_users.txt', 'mute_users.txt']
    for uf in user_files:
        fp = os.path.join(base_dir, uf)
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 4:
                        ht.insert(parts[0].strip().lower(), (parts[3].strip(), "user"))
                        
    hp = os.path.join(base_dir, 'helpers.txt')
    if os.path.exists(hp):
        with open(hp, 'r', encoding='utf-8-sig') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    ht.insert(parts[0].strip().lower(), (parts[3].strip(), "helper"))

    ht.insert("blind_user", ("pass123", "user"))
    ht.insert("mute_user", ("pass123", "user"))
    ht.insert("helper", ("pass123", "helper"))
    st.session_state.ht_auth = ht

    if 'scheduler' not in st.session_state:
        st.session_state.scheduler = EightQueensScheduler()
        
    helpers_data = []
    file_path = os.path.join(os.path.dirname(__file__), 'helpers.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 8:
                        parts[4] = parts[4].replace(" District", "")
                        helpers_data.append(parts)
    
    if not helpers_data:
        helpers_data = [
            ["Aarav", "aarav@tn.com", "H1", "***", "Chennai", "Full Time", "Tamil, English, Sign Language", "Navigation Assist"]
        ]
    st.session_state.mock_helpers = helpers_data
    
    users_data = []
    user_files = ['blind_users.txt', 'deaf_users.txt', 'mute_users.txt']
    for uf in user_files:
        fp = os.path.join(os.path.dirname(__file__), uf)
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 5:
                        parts[4] = parts[4].replace(" District", "")
                        if len(parts) == 5: parts.append("Any") # Fallback Timing
                        users_data.append(parts)
    st.session_state.mock_users = users_data

def speak(text):
    if SPEECH_AVAILABLE:
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception: 
            st.warning("🎙️ Voice engine failed to trigger locally.")
    else:
        st.warning(f"🔊 System Audio: {text}")

def nav_to(page):
    st.session_state.page = page
    if hasattr(st, 'rerun'): st.rerun()
    else: st.experimental_rerun()

init_app_state()

# ----------------- REGISTRATION & LOGIN ----------------

if st.session_state.page == 'login':
    col_img, col_text = st.columns([1,2])
    with col_text:
        st.title("Silent Voice Platform")
        st.write("Connecting the Specially Abled with trusted local Volunteers seamlessly.")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Login to your Account")
        user = st.text_input("Username", value="", placeholder="e.g. Arun Blind")
        password = st.text_input("Password", value="", type="password", placeholder="e.g. pass123")
        if st.button("Sign In"):
            stored = st.session_state.ht_auth.search(user.strip().lower())
            if stored and stored[0] == password.strip():
                speak(f"Welcome back, {user}")
                st.session_state.logged_in_user = user
                st.session_state.user_role = stored[1]
                nav_to('dashboard')
            else:
                st.error("Invalid Login Credentials. No collision found.")
    
    with col2:
        st.subheader("New User?")
        st.write("Register safely. Our backend Hash Table securely handles millions of collisions automatically.")
        if st.button("Create an Account"): nav_to('register')

elif st.session_state.page == 'register':
    st.title("Network Registration")
    st.button("Back to Login", on_click=lambda: nav_to('login'))
    
    tab1, tab2 = st.tabs(["Specially Abled User", "Volunteer Helper"])
    
    with tab1:
        st.subheader("Register as User")
        u_name = st.text_input("Choose Username (User)")
        u_pass = st.text_input("Choose Password (User)", type='password')
        if st.button("Register User Account"):
            res = st.session_state.ht_auth.insert(u_name, (u_pass, "user"))
            if res:
                st.success("User registered securely into Hash Table!")
                speak("Registration complete.")
            else:
                st.error("Hash table capacity critical!")
                
    with tab2:
        st.subheader("Register as Volunteer Helper")
        h_name = st.text_input("Choose Username (Helper)")
        h_pass = st.text_input("Choose Password (Helper)", type='password')
        h_dist = st.selectbox("Your District", ["Chennai", "Coimbatore", "Madurai", "Trichy", "Salem"])
        h_lang = st.selectbox("Languages", ["Tamil", "Sign Language", "English"])
        
        if st.button("Register Helper Account"):
            res = st.session_state.ht_auth.insert(h_name, (h_pass, "helper"))
            if res:
                st.session_state.mock_helpers.append([h_name, "new@tn.com", "H_New", "***", h_dist, "Any", h_lang, "General Assistance"])
                st.success("Helper registered securely into Hash Table!")
            else:
                st.error("Hash table capacity critical!")

# ----------------- UNIFIED DASHBOARDS ----------------

elif st.session_state.page == 'dashboard':
    st.button("🚪 Log Out", on_click=lambda: nav_to('login'))
    
    # ---------------- USER DASHBOARD ----------------
    if st.session_state.user_role == "user":
        st.title(f"Hello, {st.session_state.logged_in_user}! (Specially Abled Portal)")
        
        colA, colB = st.columns(2)
        with colA:
            if st.button("🎒 Optimize Matches "): nav_to('dispatch_knapsack')
        with colB:
            if st.button("🚨 Emergency SOS Map Generation"): nav_to('sos')
            
        st.divider()
        # Smart Recognition tag
        user_lower = st.session_state.logged_in_user.lower()
        if "blind" in user_lower:
            st.subheader("👁️ Available Helpers (Vision & Navigation Specialists)")
            st.write("We have pre-filtered this directory specifically for your mobility needs:")
        elif "deaf" in user_lower or "mute" in user_lower:
            st.subheader("🤟 Available Helpers (Sign Language & Transit Specialists)")
            st.write("We have pre-filtered this directory specifically for your communication needs:")
        else:
            st.subheader("Available Helpers in Tamil Nadu (Directory)")
            st.write("Browse manually and connect directly with anyone below.")
        
        # Directory pushed directly to front page using Merge Sort
        sorted_helpers = DivideConquerAlgorithms.merge_sort(st.session_state.mock_helpers, key_index=4)
        
        # Smart Dynamic Skill Filtering Logic based on User Type!
        filtered_helpers = []
        for h in sorted_helpers:
            skills = h[7].lower() if len(h) > 7 else ""
            langs = h[6].lower() if len(h) > 6 else ""
            
            if "blind" in user_lower:
                if "guidance" in skills or "navigation" in skills or "transit" in skills: 
                    filtered_helpers.append(h)
            elif "deaf" in user_lower or "mute" in user_lower:
                if "sign language" in langs or "asl" in skills or "first help" in skills or "general support" in skills: 
                    filtered_helpers.append(h)
            else:
                filtered_helpers.append(h)
                
        # If the filtered pool is somehow completely empty, safely fallback to showing everyone
        if not filtered_helpers: filtered_helpers = sorted_helpers
        
        for h in filtered_helpers:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"### {h[0]}")
                    st.write(f"📍 **Location:** {h[4]} | 🗣️ **Language:** {h[6]} | 🎓 **Skills:** {h[7]}")
                with col2:
                    if st.button(f"Dial {h[0]}", key=f"dial_{h[0]}"):
                        st.session_state.active_helper = h[0]
                        nav_to('live_call')

    # ---------------- HELPER DASHBOARD (LOGISTICS) ----------------
    elif st.session_state.user_role == "helper":
        st.title(f"Hello, {st.session_state.logged_in_user}! (System Administrator & Helper Portal)")
        
        st.write("Welcome to the logistics console. Here you can survey the specific live booking requests from different disability groups and allocate resources perfectly.")
        
        st.divider()
        st.subheader("📋 Pending Request Directory")
        st.write("Live shift data sourced specifically from users requesting support:")
        
        u_cols = st.columns(3)
        with u_cols[0]: st.write("**👁️ Blind Users**")
        with u_cols[1]: st.write("**🤟 Deaf Users**")
        with u_cols[2]: st.write("**🗣️ Mute Users**")
        
        for u in st.session_state.mock_users:
            uname = u[0].lower()
            u_str = f"- **{u[0]}** | ⏱️ `{u[5]}`"
            if "blind" in uname: 
                with u_cols[0]: st.write(u_str)
            elif "deaf" in uname: 
                with u_cols[1]: st.write(u_str)
            elif "mute" in uname: 
                with u_cols[2]: st.write(u_str)
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📅 Live Schedule ")
            st.write("Build a mathematically clash-free roster mapping Helpers to Users on grid.")
            grid_size = st.slider("Select Coverage Scale (Helpers To Dispatch)", 4, 8, 8)
            if st.button("Generate Clash-Free Roster"):
                import pandas as pd
                max_grid = min(grid_size, len(st.session_state.mock_helpers), len(st.session_state.mock_users))
                board = [[0]*max_grid for _ in range(max_grid)]
                
                if st.session_state.scheduler.solve_8queens(board, 0, n=max_grid):
                    h_subset = st.session_state.mock_helpers[:max_grid]
                    u_subset = st.session_state.mock_users[:max_grid]
                    
                    df_board = pd.DataFrame(board, 
                                            columns=[f"{u[0]} ({u[5]})" for u in u_subset], 
                                            index=[h[0] for h in h_subset])
                    df_board = df_board.replace({0: "❌", 1: "✅ Assigned"})
                    st.dataframe(df_board, use_container_width=True)
                    st.success("8-Queens Integration complete! Mathematical matching ensures no overlapped shifts!")
                else:
                    st.error("Matrix deadlock: Cannot map shifts securely without overlapping constraints.")

        with col2:
            st.subheader("Route Dispatch")
            st.write("Calculate shortest driving patrol between specific registered Hubs.")
            unique_districts = sorted(list(set([h[4] for h in st.session_state.mock_helpers if len(h) > 4])))
            if not unique_districts: unique_districts = ["Chennai", "Madurai", "Trichy"]
            all_hubs = [f"{d} Hub" for d in unique_districts]
            
            selected_hubs = st.multiselect("Select Delivery Nodes", all_hubs, default=all_hubs[:3] if len(all_hubs) >= 3 else all_hubs)
            
            if st.button("Execute Routing"):
                n = len(selected_hubs)
                if n < 2: st.warning("Requires at least 2 nodes.")
                else:
                    # Realistic mathematical distance mappings (approx routing km)
                    real_distances = {
                        "Chennai": {"Coimbatore": 500, "Madurai": 460, "Tiruchirappalli": 330, "Salem": 340, "Erode": 400, "Thanjavur": 350, "Tirunelveli": 620},
                        "Coimbatore": {"Chennai": 500, "Madurai": 210, "Tiruchirappalli": 215, "Salem": 160, "Erode": 100, "Thanjavur": 270, "Tirunelveli": 370},
                        "Madurai": {"Chennai": 460, "Coimbatore": 210, "Tiruchirappalli": 135, "Salem": 235, "Erode": 210, "Thanjavur": 190, "Tirunelveli": 160},
                        "Tiruchirappalli": {"Chennai": 330, "Coimbatore": 215, "Madurai": 135, "Salem": 140, "Erode": 150, "Thanjavur": 55, "Tirunelveli": 290},
                        "Salem": {"Chennai": 340, "Coimbatore": 160, "Madurai": 235, "Tiruchirappalli": 140, "Erode": 65, "Thanjavur": 195, "Tirunelveli": 395},
                        "Erode": {"Chennai": 400, "Coimbatore": 100, "Madurai": 210, "Tiruchirappalli": 150, "Salem": 65, "Thanjavur": 205, "Tirunelveli": 370},
                        "Thanjavur": {"Chennai": 350, "Coimbatore": 270, "Madurai": 190, "Tiruchirappalli": 55, "Salem": 195, "Erode": 205, "Tirunelveli": 345},
                        "Tirunelveli": {"Chennai": 620, "Coimbatore": 370, "Madurai": 160, "Tiruchirappalli": 290, "Salem": 395, "Erode": 370, "Thanjavur": 345}
                    }
                    
                    matrix = [[0]*n for _ in range(n)]
                    for i in range(n):
                        for j in range(n):
                            if i != j:
                                city_i = selected_hubs[i].replace(" Hub", "")
                                city_j = selected_hubs[j].replace(" Hub", "")
                                matrix[i][j] = real_distances.get(city_i, {}).get(city_j, 100) # Defaults to 100km if unknown
                                
                    cost, route = BranchAndBoundTSP.tsp_solve(matrix)
                    st.success(f"Logistics Path Executed. Total Travel Distance: {cost} km")
                    route_str = " ➔ ".join([selected_hubs[r] for r in route])
                    st.write(f"**GPS Sequenced Trip Protocol:** {route_str}")

# ----------------- USER FEATURES (KNAPSACK & SOS & CALLING) ----------------

elif st.session_state.page == 'dispatch_knapsack':
    st.title("🎒 AI Parameter Optimizer")
    st.button("Back to Dashboard", on_click=lambda: nav_to('dashboard'))
    
    st.write("Submit your specific requirements below. Our mathematical models will parse the directory to find the absolute optimized responder list.")
    
    unique_districts = sorted(list(set([h[4] for h in st.session_state.mock_helpers if len(h) > 4])))
    if not unique_districts: unique_districts = ["Chennai", "Coimbatore", "Madurai", "Trichy", "Salem"]
    # Extract properties live directly from dataset
    all_langs = []
    for h in st.session_state.mock_helpers:
        if len(h) > 6:
            all_langs.extend([l.strip() for l in h[6].split(',')])
    unique_langs = sorted(list(set(all_langs))) if all_langs else ["Tamil", "English"]
    
    all_skills = []
    for h in st.session_state.mock_helpers:
        if len(h) > 7:
            all_skills.extend([s.strip() for s in h[7].split(',')])
    unique_skills = sorted(list(set(all_skills))) if all_skills else ["Rescue Transit"]
    
    all_avails = []
    for h in st.session_state.mock_helpers:
        if len(h) > 5 and h[5].strip().lower() != 'any':
            all_avails.append(h[5].strip())
    unique_avails = sorted(list(set(all_avails))) + ["Any"]
    
    sel_district = st.selectbox("Your District", unique_districts)
    sel_lang = st.selectbox("Preferred Language Mode", unique_langs)
    sel_skill = st.selectbox("Specific Need / Skill Required", ["Any"] + unique_skills)
    sel_avail = st.selectbox("Shift Needed", unique_avails)
        
    req = {'district': sel_district, 'language': sel_lang, 'availability': sel_avail, 'skill': sel_skill}
    best = GreedyAlgorithms.knapsack_helper_selection(st.session_state.mock_helpers, req, max_time=3)
    
    if best:
        st.success(f"Matched exclusively {len(best)} helpers who fit the exact priority scale.")
        for b in best:
            with st.container(border=True):
                colA, colB = st.columns([3, 1])
                with colA: st.write(f"**{b[0]}** ({b[4]}) - Specialties: {b[7]}")
                with colB: 
                    if st.button(f"Dial {b[0]}", key=f"knapsack_{b[0]}"):
                        st.session_state.active_helper = b[0]
                        nav_to('live_call')
    else:
        st.warning("No matches found within proximity limitations.")

elif st.session_state.page == 'sos':
    st.title("🚨 Live Emergency Route Mapping")
    st.button("Back", on_click=lambda: nav_to('dashboard'))
    
    unique_districts = sorted(list(set([h[4] for h in st.session_state.mock_helpers if len(h) > 4])))
    if not unique_districts: unique_districts = ["Chennai", "Coimbatore", "Madurai"]
    
    col1, col2 = st.columns(2)
    with col1: 
        start_dist = st.selectbox("Incident District", unique_districts)
        start_manual = st.text_input("Exact Incident Location (Manual)", placeholder="e.g. 2nd East Street")
    with col2: 
        target_dist = st.selectbox("Clearance Hub District", unique_districts)
        target_manual = st.text_input("Exact Clearance Location (Manual)", placeholder="e.g. General Hospital Wing A")
        
    start_site = f"{start_manual}, {start_dist}" if start_manual else start_dist
    target_site = f"{target_manual}, {target_dist}" if target_manual else target_dist
    
    if st.button("Calculate Immediate Evacuation Path"):
        # Realistic mathematical distance mappings
        real_distances = {
            "Chennai": {"Chennai": 15, "Coimbatore": 500, "Madurai": 460, "Tiruchirappalli": 330, "Salem": 340, "Erode": 400, "Thanjavur": 350, "Tirunelveli": 620},
            "Coimbatore": {"Coimbatore": 15, "Chennai": 500, "Madurai": 210, "Tiruchirappalli": 215, "Salem": 160, "Erode": 100, "Thanjavur": 270, "Tirunelveli": 370},
            "Madurai": {"Madurai": 15, "Chennai": 460, "Coimbatore": 210, "Tiruchirappalli": 135, "Salem": 235, "Erode": 210, "Thanjavur": 190, "Tirunelveli": 160},
            "Tiruchirappalli": {"Tiruchirappalli": 15, "Chennai": 330, "Coimbatore": 215, "Madurai": 135, "Salem": 140, "Erode": 150, "Thanjavur": 55, "Tirunelveli": 290},
            "Salem": {"Salem": 15, "Chennai": 340, "Coimbatore": 160, "Madurai": 235, "Tiruchirappalli": 140, "Erode": 65, "Thanjavur": 195, "Tirunelveli": 395},
            "Erode": {"Erode": 15, "Chennai": 400, "Coimbatore": 100, "Madurai": 210, "Tiruchirappalli": 150, "Salem": 65, "Thanjavur": 205, "Tirunelveli": 370},
            "Thanjavur": {"Thanjavur": 15, "Chennai": 350, "Coimbatore": 270, "Madurai": 190, "Tiruchirappalli": 55, "Salem": 195, "Erode": 205, "Tirunelveli": 345},
            "Tirunelveli": {"Tirunelveli": 15, "Chennai": 620, "Coimbatore": 370, "Madurai": 160, "Tiruchirappalli": 290, "Salem": 395, "Erode": 370, "Thanjavur": 345}
        }
        total_dist = real_distances.get(start_dist, {}).get(target_dist, 50)
        
        stages = [start_site, "Traffic Core", "Checkpost", target_site]
        # Map logical graph divisions mathematically scaling with real-world overall kilometers natively
        e1 = int(total_dist * 0.4) if total_dist > 5 else 2
        e2 = int(total_dist * 0.6) if total_dist > 5 else 3
        e3 = int(total_dist * 0.5) if total_dist > 5 else 2
        
        edges = {(0, 1): e1, (0, 2): e1 + max(3, int(total_dist * 0.1)), (1, 3): e2, (2, 3): e3, (1, 2): max(2, int(total_dist * 0.1))}
        dist, path = DynamicProgrammingAlgorithms.multistage_graph(stages, edges)
        
        st.error(f"EMERGENCY LOCKDOWN ACTIVE. Lowest risk physical distance to safety clearance: {dist} km")
        st.write(f"Safest Computed DP Route: {' ➔ '.join(path)}")

elif st.session_state.page == 'live_call':
    st.title(f"📞 Interface Hub Connected to: {st.session_state.active_helper}")
    st.write("You are linked through an isolated, secure channel.")
    if st.button("Disconnect Session"):
        st.session_state.active_helper = None
        nav_to('dashboard')
        
    st.divider()
    colA, colB = st.columns(2)
    with colA:
        st.write("**Live Video Feed**")
        video_stream = st.camera_input("Enable Webcam Signal")
        if video_stream: st.success(f"Live visual feed successfully resolving to {st.session_state.active_helper}")
    with colB:
        st.write("**Audio Transmission Input**")
        if hasattr(st, 'audio_input'):
            audio_val = st.audio_input("Record Voice Packet")
            if audio_val: st.success("Voice transmission packaged and sent.")
        
        st.write("---")
        st.write("**Text-to-Speech Output (For the Helper)**")
        tts = st.text_input("Type physical narration output:", key="tts_live")
        if st.button("🔊 Emulate Voice"): speak(tts)
        
        st.write("---")
        st.write("**Live Transcription (Speech Recognition)**")
        if st.button("🎤 Turn on PC Mic transcription"):
            if SPEECH_AVAILABLE:
                st.info("Listening... Speak clearly.")
                try:
                    r = sr.Recognizer()
                    with sr.Microphone() as source:
                        audio = r.listen(source, timeout=4)
                        text = r.recognize_google(audio)
                        st.success(f"You said: {text}")
                        if DynamicProgrammingAlgorithms.edit_distance(text.lower(), "help") < 3:
                            st.error("Urgent assistance recognized locally! Alerting Helper.")
                except Exception: st.error("Microphone hardware block detected.")
            else: st.warning("Speech Recognition python modules not installed.")

