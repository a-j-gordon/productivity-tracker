import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

DATA_FILE = "projects.json"
LOG_FILE  = "daily_log.json"

st.set_page_config(
    page_title="Tracker",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Password protection ────────────────────────
def check_password():
    if st.session_state.get("authenticated"):
        return True
    st.markdown("""
    <style>
    .main .block-container { max-width: 420px !important; padding-top: 5rem !important; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('''<div style="font-family:'Playfair Display',serif;font-size:32px;font-weight:700;color:#e8e0d4;text-align:center;margin-bottom:2rem">◈ Tracker</div>''', unsafe_allow_html=True)
    pwd = st.text_input("Password", type="password", placeholder="Enter password...", label_visibility="collapsed")
    if st.button("Enter →", key="login_btn"):
        correct = st.secrets.get("APP_PASSWORD", "")
        if pwd == correct:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    return False

if not check_password():
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background: #141210 !important;
    color: #e8e0d4 !important;
}

.main { background: #141210 !important; }
.main .block-container {
    padding: 2.25rem 2.75rem;
    max-width: 1080px;
    background: #141210;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background: #0e0c0a !important; border-right: 1px solid #2a2420 !important; }
section[data-testid="stSidebar"] > div { background: #0e0c0a !important; }
section[data-testid="stSidebar"] * { color: #a89880 !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #a89880 !important;
    border-radius: 6px !important;
    width: 100% !important;
    text-align: left !important;
    padding: 8px 12px !important;
    margin-bottom: 2px !important;
    font-size: 13px !important;
    font-family: 'Outfit', sans-serif !important;
    transition: all 0.12s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(214,165,100,0.08) !important;
    border-color: rgba(214,165,100,0.2) !important;
    color: #d6a564 !important;
}

/* ── Global elements ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #1e1a16 !important;
    border: 1px solid #2e2820 !important;
    color: #e8e0d4 !important;
    border-radius: 7px !important;
    font-family: 'Outfit', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #d6a564 !important;
    box-shadow: 0 0 0 2px rgba(214,165,100,0.15) !important;
}
.stSelectbox > div > div { color: #e8e0d4 !important; }

/* Form submit buttons */
.stFormSubmitButton > button {
    background: #d6a564 !important;
    border: none !important;
    color: #0e0c0a !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    padding: 9px 20px !important;
    transition: all 0.15s !important;
}
.stFormSubmitButton > button:hover { background: #c4904e !important; }

/* Regular buttons */
.stButton > button {
    background: transparent !important;
    border: 1px solid #2e2820 !important;
    color: #a89880 !important;
    border-radius: 6px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    transition: all 0.12s !important;
}
.stButton > button:hover {
    border-color: #d6a564 !important;
    color: #d6a564 !important;
    background: rgba(214,165,100,0.06) !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background: #1a1612 !important;
    border: 1px solid #2a2420 !important;
    border-radius: 7px !important;
    color: #a89880 !important;
    font-size: 13px !important;
    font-family: 'Outfit', sans-serif !important;
}
.streamlit-expanderContent {
    background: #1a1612 !important;
    border: 1px solid #2a2420 !important;
    border-top: none !important;
}

/* Checkboxes */
.stCheckbox > label { color: #a89880 !important; font-size: 14px !important; }

/* Date input */
.stDateInput > div > div > input {
    background: #1e1a16 !important;
    border: 1px solid #2e2820 !important;
    color: #e8e0d4 !important;
    border-radius: 7px !important;
}

/* ── Typography ── */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 700;
    color: #e8e0d4;
    letter-spacing: -0.02em;
    margin-bottom: 0.15rem;
    line-height: 1.1;
}
.page-sub {
    font-size: 13px;
    color: #5a5248;
    margin-bottom: 2rem;
    letter-spacing: 0.01em;
}
.section-head {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 700;
    color: #e8e0d4;
    margin-bottom: 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #2a2420;
}
.label-sm {
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #5a5248;
    margin-bottom: 6px;
}

/* ── Metric cards ── */
.metric-box {
    background: #1a1612;
    border: 1px solid #2a2420;
    border-radius: 10px;
    padding: 1.1rem 1.25rem;
    text-align: center;
}
.metric-num {
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    font-weight: 700;
    color: #e8e0d4;
    line-height: 1;
}
.metric-lbl {
    font-size: 10px;
    color: #5a5248;
    margin-top: 5px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.metric-box-accent {
    background: #1e1a10;
    border: 1px solid #3a3010;
}
.metric-box-accent .metric-num { color: #d6a564; }

/* ── Streak / stat strip ── */
.stat-row {
    display: flex;
    gap: 10px;
    margin-bottom: 1.5rem;
}

/* ── Project cards ── */
.proj-card {
    background: #1a1612;
    border: 1px solid #2a2420;
    border-radius: 10px;
    padding: 1.1rem 1.35rem;
    margin-bottom: 8px;
    transition: border-color 0.15s;
}
.proj-card:hover { border-color: #3a3028; }
.proj-card-title {
    font-family: 'Outfit', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: #e8e0d4;
}
.proj-card-desc { font-size: 13px; color: #5a5248; margin: 4px 0 10px; }

/* ── Progress bars ── */
.prog-wrap { background: #2a2420; border-radius: 4px; height: 4px; }
.prog-fill  { height: 4px; border-radius: 4px; background: #d6a564; transition: width 0.4s ease; }

/* ── Status badges ── */
.badge { display: inline-block; padding: 2px 9px; border-radius: 99px; font-size: 11px; font-weight: 500; }
.badge-active   { background: rgba(180,140,60,0.15); color: #d6a564; border: 1px solid rgba(214,165,100,0.25); }
.badge-stalled  { background: rgba(180,80,60,0.12); color: #e07060; border: 1px solid rgba(224,112,96,0.25); }
.badge-complete { background: rgba(100,140,100,0.12); color: #80b080; border: 1px solid rgba(128,176,128,0.25); }

/* ── Priority ── */
.pri { display: inline-block; padding: 1px 7px; border-radius: 4px; font-size: 11px; font-weight: 500; }
.pri-high   { background: rgba(180,60,60,0.15); color: #e07060; }
.pri-medium { background: rgba(180,140,60,0.12); color: #c49040; }
.pri-low    { background: rgba(80,140,80,0.12); color: #70a870; }

/* ── Task rows ── */
.task-row {
    background: #1a1612;
    border: 1px solid #2a2420;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 5px;
}
.task-title      { font-size: 14px; font-weight: 500; color: #e8e0d4; }
.task-title-done { font-size: 14px; font-weight: 400; text-decoration: line-through; color: #3a3428; }
.task-meta       { font-size: 12px; color: #5a5248; margin-top: 3px; }

/* ── Priority focus cards (dashboard) ── */
.prio-card {
    background: #1a1612;
    border: 1px solid #2a2420;
    border-left: 3px solid #e07060;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 5px;
}
.prio-card-med { border-left-color: #c49040; }
.prio-card-low { border-left-color: #70a870; }

/* ── Divider ── */
.soft-div { border: none; border-top: 1px solid #2a2420; margin: 1.5rem 0; }

/* ── Week streak dots ── */
.streak-wrap { display: flex; gap: 6px; align-items: center; margin-top: 6px; }
.streak-dot  { width: 10px; height: 10px; border-radius: 50%; background: #2a2420; }
.streak-dot.active { background: #d6a564; }

/* Info boxes */
.stInfo { background: #1e1a10 !important; border-color: #3a3010 !important; color: #a89880 !important; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            d = json.load(f)
            if isinstance(d, dict):
                return d
            return {"projects": d, "activity": []}
    return {"projects": [], "activity": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_activity(data):
    today = str(date.today())
    if today not in data.get("activity", []):
        data.setdefault("activity", []).append(today)
        save_data(data)

def get_streak(data):
    activity = sorted(data.get("activity", []), reverse=True)
    if not activity:
        return 0
    streak = 0
    check = date.today()
    for a in activity:
        d = date.fromisoformat(a)
        if d == check:
            streak += 1
            check -= timedelta(days=1)
        elif d == check + timedelta(days=1):
            check = d
        else:
            break
    return streak

def get_week_activity(data):
    activity = set(data.get("activity", []))
    today = date.today()
    return [str(today - timedelta(days=6-i)) in activity for i in range(7)]

def tasks_done_this_week(projects):
    cutoff = date.today() - timedelta(days=7)
    count = 0
    for p in projects:
        for t in p.get("tasks", []):
            if t.get("done") and t.get("done_date"):
                try:
                    if date.fromisoformat(t["done_date"]) >= cutoff:
                        count += 1
                except:
                    pass
    return count

def new_id():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")

def get_progress(p):
    tasks = p.get("tasks", [])
    if not tasks: return 0
    return int(sum(1 for t in tasks if t.get("done")) / len(tasks) * 100)

def status_badge(s):
    cls = {"Active":"badge-active","Stalled":"badge-stalled","Complete":"badge-complete"}.get(s,"badge-active")
    return f'<span class="badge {cls}">{s}</span>'

def pri_badge(p):
    cls = {"High":"pri-high","Medium":"pri-medium","Low":"pri-low"}.get(p,"pri-medium")
    return f'<span class="pri {cls}">{p}</span>'

def pri_order(p):
    return {"High":0,"Medium":1,"Low":2}.get(p,1)

def move_item(lst, i, d):
    j = i + d
    if 0 <= j < len(lst):
        lst[i], lst[j] = lst[j], lst[i]
        return True
    return False

# ── Daily log helpers ──
def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            return json.load(f)
    return []

def save_log(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

# ── Session state ──────────────────────────────

if "data" not in st.session_state:
    st.session_state.data = load_data()
    log_activity(st.session_state.data)

data     = st.session_state.data
projects = data["projects"]

if "view" not in st.session_state:
    st.session_state.view = "dashboard"
if "selected_id" not in st.session_state:
    st.session_state.selected_id = None

def switch(view, pid=None):
    st.session_state.view = view
    st.session_state.selected_id = pid

def get_proj():
    return next((p for p in projects if p["id"] == st.session_state.selected_id), None)

# ── Sidebar ───────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='padding:1.5rem 0 1.5rem;border-bottom:1px solid #2a2420;margin-bottom:1.25rem'>
        <div style='font-family:"Playfair Display",serif;font-size:22px;font-weight:700;color:#e8e0d4;letter-spacing:-0.01em'>◈ Tracker</div>
        <div style='font-size:10px;color:#3a3428;margin-top:4px;letter-spacing:0.1em'>RESEARCH & PROJECTS</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋  New project", key="sb_new"):
        switch("new")

    st.markdown("<div style='margin:1.25rem 0 0.6rem;font-size:10px;color:#3a3428;letter-spacing:0.1em'>PROJECTS</div>", unsafe_allow_html=True)

    if not projects:
        st.markdown("<div style='font-size:12px;color:#3a3428;padding:4px 0'>Nothing here yet</div>", unsafe_allow_html=True)
    for p in projects:
        pct = get_progress(p)
        if st.button(f"{p['name']}", key=f"sb_{p['id']}"):
            switch("detail", p["id"])

    st.markdown("<hr style='border-color:#2a2420;margin:1.5rem 0 1rem'>", unsafe_allow_html=True)
    if st.button("◈  Dashboard", key="sb_dash"):
        switch("dashboard")
    if st.button("📝  Daily log", key="sb_log"):
        switch("daily_log")

    st.markdown("<div style='margin:1.25rem 0 0.6rem;font-size:10px;color:#3a3428;letter-spacing:0.1em'>GOALS</div>", unsafe_allow_html=True)
    if st.button("◎  Quarterly goals", key="sb_goals"):
        switch("goals_overview")
    quarters = sorted(set(g.get("quarter","") for g in data.get("goals",[]) if g.get("quarter")), reverse=True)
    for q in quarters[:4]:
        q_goals = [g for g in data.get("goals",[]) if g.get("quarter")==q]
        if st.button(f"  {q} · {len(q_goals)} goals", key=f"sb_q_{q}"):
            switch("goals_overview")

    st.markdown("<div style='margin:1.25rem 0 0.6rem;font-size:10px;color:#3a3428;letter-spacing:0.1em'>TEAM</div>", unsafe_allow_html=True)
    if st.button("👥  Team overview", key="sb_team"):
        switch("team_overview")
    for m in data.get("team", []):
        if st.button(f"  {m['name']}", key=f"sb_member_{m['id']}"):
            switch("team_member", m["id"])

# ══════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════

if st.session_state.view == "dashboard":
    active   = [p for p in projects if p.get("status") == "Active"]
    stalled  = [p for p in projects if p.get("status") == "Stalled"]
    complete = [p for p in projects if p.get("status") == "Complete"]

    streak       = get_streak(data)
    week_act     = get_week_activity(data)
    done_week    = tasks_done_this_week(projects)
    total_tasks  = sum(len(p.get("tasks",[])) for p in projects)
    total_done   = sum(sum(1 for t in p.get("tasks",[]) if t.get("done")) for p in projects)
    high_pri     = sum(1 for p in projects for t in p.get("tasks",[]) if not t.get("done") and t.get("priority")=="High")

    now = datetime.now()
    greeting = "Good morning" if now.hour < 12 else ("Good afternoon" if now.hour < 17 else "Good evening")

    st.markdown(f'<div class="page-title">{greeting}.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-sub">{now.strftime("%A, %d %B %Y")} &nbsp;·&nbsp; {len(projects)} projects</div>', unsafe_allow_html=True)

    if not projects:
        st.info("No projects yet — click ＋ New project in the sidebar to get started.")
    else:
        # Stats row
        c1,c2,c3,c4,c5 = st.columns(5)
        for col,num,lbl,acc in [
            (c1, len(active),    "Active",          False),
            (c2, f"{total_done}/{total_tasks}", "Tasks done", False),
            (c3, done_week,      "Done this week",  True),
            (c4, high_pri,       "High priority",   False),
            (c5, f"{streak}d",   "Streak",          True),
        ]:
            with col:
                accent_cls = "metric-box-accent" if acc else ""
                st.markdown(f'<div class="metric-box {accent_cls}"><div class="metric-num">{num}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

        # Week activity dots
        day_labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        today_wd   = date.today().weekday()
        dots_html  = '<div style="display:flex;gap:10px;align-items:center;margin:1rem 0 0">'
        for i, active_day in enumerate(week_act):
            day_i = (date.today() - timedelta(days=6-i)).weekday()
            lbl   = day_labels[day_i]
            cls   = "streak-dot active" if active_day else "streak-dot"
            dots_html += f'<div style="text-align:center"><div class="{cls}" style="margin:0 auto 3px"></div><div style="font-size:10px;color:#3a3428">{lbl}</div></div>'
        dots_html += "</div>"
        st.markdown(dots_html, unsafe_allow_html=True)

        st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)

        # Priority tasks
        st.markdown('<div class="label-sm">Focus — high priority tasks</div>', unsafe_allow_html=True)

        all_pending = []
        for p in projects:
            for t in p.get("tasks",[]):
                if not t.get("done"):
                    all_pending.append((p,t))
        all_pending.sort(key=lambda x: pri_order(x[1].get("priority","Medium")))

        if not all_pending:
            st.markdown('<div style="font-size:13px;color:#3a3428;padding:0.5rem 0">All clear — no pending tasks 🎉</div>', unsafe_allow_html=True)
        else:
            for p, t in all_pending[:10]:
                pri = t.get("priority","Medium")
                lc  = {"High":"prio-card","Medium":"prio-card prio-card-med","Low":"prio-card prio-card-low"}.get(pri,"prio-card prio-card-med")
                due = f' · <span style="color:#e07060">Due {t["due"]}</span>' if t.get("due") else ''
                ctx = f' · {t["context"]}' if t.get("context") else ''
                col_t, col_btn = st.columns([11,1])
                with col_t:
                    st.markdown(f"""
                    <div class="{lc}">
                        <div class="task-title">{t['text']} {pri_badge(pri)}</div>
                        <div class="task-meta">📁 {p['name']}{due}{ctx}</div>
                    </div>""", unsafe_allow_html=True)
                with col_btn:
                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                    if st.button("✓", key=f"dash_done_{t['id']}"):
                        t["done"] = True
                        t["done_date"] = str(date.today())
                        save_data(data)
                        st.rerun()

        st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)

        # All projects
        st.markdown('<div class="label-sm">All projects</div>', unsafe_allow_html=True)

        for section, sect_ps in [("Active",active),("Stalled",stalled),("Complete",complete)]:
            if sect_ps:
                st.markdown(f'<div style="font-size:10px;color:#3a3428;letter-spacing:0.08em;text-transform:uppercase;margin:1rem 0 0.5rem">{section}</div>', unsafe_allow_html=True)
                for p in sect_ps:
                    pct   = get_progress(p)
                    tasks = p.get("tasks",[])
                    done  = sum(1 for t in tasks if t.get("done"))
                    col_c, col_b = st.columns([7,1])
                    with col_c:
                        st.markdown(f"""
                        <div class="proj-card">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                                <div class="proj-card-title">{p['name']}</div>
                                {status_badge(p.get('status','Active'))}
                            </div>
                            <div class="proj-card-desc">{p.get('desc','')}</div>
                            <div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>
                            <div style="display:flex;justify-content:space-between;font-size:11px;color:#3a3428;margin-top:6px">
                                <span>{', '.join(p.get('collaborators',[])) or '—'}</span>
                                <span>{done}/{len(tasks)} tasks · {pct}%</span>
                            </div>
                        </div>""", unsafe_allow_html=True)
                    with col_b:
                        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                        if st.button("→", key=f"open_{p['id']}"):
                            switch("detail", p["id"])

# ══════════════════════════════════════════════
# NEW PROJECT
# ══════════════════════════════════════════════

elif st.session_state.view == "new":
    st.markdown('<div class="section-head">New project</div>', unsafe_allow_html=True)
    with st.form("new_proj"):
        name    = st.text_input("Project name *", placeholder="e.g. Synthetic data validation study")
        desc    = st.text_area("Description", placeholder="What is this project about?")
        status  = st.selectbox("Status", ["Active","Stalled","Complete"])
        collabs = st.text_input("Collaborators", placeholder="Sarah, James, Dr. Ahmed (comma-separated)")
        if st.form_submit_button("Create project →"):
            if not name.strip():
                st.error("Please enter a project name.")
            else:
                np = {
                    "id": new_id(), "name": name.strip(), "desc": desc.strip(),
                    "status": status,
                    "collaborators": [c.strip() for c in collabs.split(",") if c.strip()],
                    "tasks": [], "notes": "", "links": [],
                    "created": datetime.now().isoformat(),
                }
                projects.append(np)
                save_data(data)
                switch("detail", np["id"])
                st.rerun()

# ══════════════════════════════════════════════
# DETAIL
# ══════════════════════════════════════════════

elif st.session_state.view == "detail":
    p = get_proj()
    if not p:
        switch("dashboard"); st.rerun()

    pct    = get_progress(p)
    tasks  = p.get("tasks",[])
    done_c = sum(1 for t in tasks if t.get("done"))

    col_h, col_a = st.columns([5,1])
    with col_h:
        st.markdown(f'<div class="section-head">{p["name"]}</div>', unsafe_allow_html=True)
    with col_a:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("✏️ Edit", key="edit_btn"):
            switch("edit", p["id"])

    c1,c2,c3,c4 = st.columns(4)
    for col,num,lbl in [(c1,f"{pct}%","Progress"),(c2,f"{done_c}/{len(tasks)}","Tasks done"),(c3,len(p.get("collaborators",[])),"Collaborators"),(c4,len(p.get("links",[])),"Links")]:
        with col:
            st.markdown(f'<div class="metric-box"><div class="metric-num">{num}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="prog-wrap" style="height:6px;margin:1rem 0 0.5rem"><div class="prog-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)

    col_d, col_s = st.columns([5,1])
    with col_d:
        if p.get("desc"):
            st.markdown(f'<div style="font-size:13px;color:#5a5248;margin-bottom:4px">{p["desc"]}</div>', unsafe_allow_html=True)
    with col_s:
        st.markdown(status_badge(p.get("status","Active")), unsafe_allow_html=True)

    if p.get("collaborators"):
        st.markdown(f'<div style="font-size:12px;color:#3a3428;margin-top:6px">👥 {" · ".join(p["collaborators"])}</div>', unsafe_allow_html=True)

    st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)

    # ── Tasks ──
    st.markdown('<div class="label-sm">Tasks</div>', unsafe_allow_html=True)

    with st.expander("＋ Add task"):
        with st.form("add_task"):
            t_text = st.text_input("Task *", placeholder="What needs to be done?")
            tc1,tc2,tc3 = st.columns(3)
            with tc1: t_pri  = st.selectbox("Priority", ["High","Medium","Low"])
            with tc2: t_due  = st.date_input("Due date", value=None)
            with tc3: t_ctx  = st.text_input("Context", placeholder="e.g. Waiting on co-author")
            t_detail   = st.text_area("Details", placeholder="Any additional notes...", height=70)
            t_link     = st.text_input("Link (URL)", placeholder="https://...")
            if st.form_submit_button("Add task →"):
                if not t_text.strip():
                    st.error("Enter a task name.")
                else:
                    p["tasks"].append({
                        "id": new_id(), "text": t_text.strip(), "done": False,
                        "priority": t_pri,
                        "due":  str(t_due) if t_due else "",
                        "context":  t_ctx.strip(),
                        "detail":   t_detail.strip(),
                        "link":     t_link.strip(),
                        "done_date": "",
                    })
                    save_data(data); st.rerun()

    undone  = sorted([t for t in tasks if not t.get("done")], key=lambda t: pri_order(t.get("priority","Medium")))
    done_ts = [t for t in tasks if t.get("done")]

    if not undone and not done_ts:
        st.markdown('<div style="font-size:13px;color:#3a3428;padding:0.5rem 0">No tasks yet</div>', unsafe_allow_html=True)

    for t in undone + done_ts:
        orig_i = tasks.index(t)
        pri    = t.get("priority","Medium")
        is_done = t.get("done", False)
        due_str = f'Due {t["due"]} · ' if t.get("due") else ''
        ctx_str = t.get("context","")
        title_cls = "task-title-done" if is_done else "task-title"

        col_cb, col_info, col_act = st.columns([1,9,2])
        with col_cb:
            checked = st.checkbox("", value=is_done, key=f"cb_{t['id']}", label_visibility="collapsed")
            if checked != is_done:
                t["done"] = checked
                t["done_date"] = str(date.today()) if checked else ""
                save_data(data); st.rerun()
        with col_info:
            detail_part = f' &nbsp;·&nbsp; <span style="color:#3a3428">{t["detail"]}</span>' if t.get("detail") else ''
            link_part   = f' &nbsp;<a href="{t["link"]}" target="_blank" style="color:#d6a564;font-size:12px">↗ link</a>' if t.get("link") else ''
            st.markdown(f"""
            <div class="task-row" style="{'opacity:0.35' if is_done else ''}">
                <div class="{title_cls}">{t['text']} {'' if is_done else pri_badge(pri)}</div>
                <div class="task-meta">{due_str}{ctx_str}{detail_part}{link_part}</div>
            </div>""", unsafe_allow_html=True)
        with col_act:
            a1,a2,a3 = st.columns(3)
            with a1:
                if st.button("↑", key=f"up_{t['id']}"):
                    move_item(tasks, orig_i, -1); save_data(data); st.rerun()
            with a2:
                if st.button("↓", key=f"dn_{t['id']}"):
                    move_item(tasks, orig_i,  1); save_data(data); st.rerun()
            with a3:
                if st.button("✕", key=f"del_{t['id']}"):
                    tasks.pop(orig_i); save_data(data); st.rerun()

    st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)

    # ── Notes ──
    st.markdown('<div class="label-sm">Notes</div>', unsafe_allow_html=True)
    notes = st.text_area("", value=p.get("notes",""), placeholder="Decisions, blockers, updates...", height=130, label_visibility="collapsed", key="notes_ta")
    if notes != p.get("notes",""):
        p["notes"] = notes; save_data(data)

    st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)

    # ── Links ──
    st.markdown('<div class="label-sm">Links</div>', unsafe_allow_html=True)
    with st.expander("＋ Add link"):
        with st.form("add_link"):
            lc1,lc2 = st.columns([2,3])
            with lc1: l_label = st.text_input("Label", placeholder="e.g. Draft paper")
            with lc2: l_url   = st.text_input("URL",   placeholder="https://...")
            if st.form_submit_button("Add link →"):
                if l_url.strip():
                    p["links"].append({"id":new_id(),"label":l_label.strip() or l_url.strip(),"url":l_url.strip()})
                    save_data(data); st.rerun()

    for i, lnk in enumerate(p.get("links",[])):
        ll,lr = st.columns([10,1])
        with ll:
            st.markdown(f'<div style="font-size:13px;padding:5px 0">🔗 <a href="{lnk["url"]}" target="_blank" style="color:#d6a564">{lnk["label"]}</a></div>', unsafe_allow_html=True)
        with lr:
            if st.button("✕", key=f"dellnk_{lnk['id']}"):
                p["links"].pop(i); save_data(data); st.rerun()

    st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)

    # ── Reorder & delete ──
    with st.expander("↕ Reorder project"):
        pidx = next((i for i,x in enumerate(projects) if x["id"]==p["id"]), 0)
        rc1,rc2 = st.columns(2)
        with rc1:
            if st.button("↑ Move up", key="proj_up"):
                if move_item(projects, pidx, -1): save_data(data); st.rerun()
        with rc2:
            if st.button("↓ Move down", key="proj_dn"):
                if move_item(projects, pidx,  1): save_data(data); st.rerun()

    with st.expander("⚠️ Delete project"):
        st.markdown('<div style="font-size:13px;color:#5a5248;margin-bottom:0.75rem">This will permanently delete the project and all its data.</div>', unsafe_allow_html=True)
        if st.button("Delete this project", key="del_proj"):
            data["projects"] = [x for x in projects if x["id"] != p["id"]]
            save_data(data); switch("dashboard"); st.rerun()

# ══════════════════════════════════════════════
# EDIT
# ══════════════════════════════════════════════

elif st.session_state.view == "edit":
    p = get_proj()
    if not p:
        switch("dashboard"); st.rerun()

    st.markdown('<div class="section-head">Edit project</div>', unsafe_allow_html=True)
    with st.form("edit_proj"):
        name    = st.text_input("Project name *", value=p["name"])
        desc    = st.text_area("Description",     value=p.get("desc",""))
        status  = st.selectbox("Status", ["Active","Stalled","Complete"], index=["Active","Stalled","Complete"].index(p.get("status","Active")))
        collabs = st.text_input("Collaborators",  value=", ".join(p.get("collaborators",[])))
        goals_list = data.get("goals", [])
        goal_options = ["None"] + [f'{g["title"]} ({g.get("quarter","")})' for g in goals_list]
        current_goal_idx = 0
        if p.get("goal_id"):
            match = next((i+1 for i,g in enumerate(goals_list) if g["id"]==p["goal_id"]), 0)
            current_goal_idx = match
        goal_choice = st.selectbox("Quarterly goal", goal_options, index=current_goal_idx)
        c1,c2   = st.columns(2)
        with c1: save_btn = st.form_submit_button("Save changes →")
        with c2: cancel   = st.form_submit_button("Cancel")
        if save_btn:
            if not name.strip(): st.error("Enter a project name.")
            else:
                p["name"]          = name.strip()
                p["desc"]          = desc.strip()
                p["status"]        = status
                p["collaborators"] = [c.strip() for c in collabs.split(",") if c.strip()]
                if goal_choice == "None":
                    p.pop("goal_id", None)
                else:
                    chosen_idx = goal_options.index(goal_choice) - 1
                    p["goal_id"] = goals_list[chosen_idx]["id"]
                save_data(data); switch("detail", p["id"]); st.rerun()
        if cancel:
            switch("detail", p["id"]); st.rerun()

# ══════════════════════════════════════════════
# TEAM SECTION — injected below existing views
# ══════════════════════════════════════════════

elif st.session_state.view == "team_overview":
    team = data.get("team", [])
    st.markdown('<div class="section-head">Team</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Weekly check-in snapshots across your direct reports</div>', unsafe_allow_html=True)

    if st.button("＋ Add team member", key="add_member_btn"):
        switch("team_new_member")

    if not team:
        st.markdown('<div style="font-size:13px;color:#3a3428;padding:1rem 0">No team members yet — add one above.</div>', unsafe_allow_html=True)
    else:
        st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)
        for member in team:
            checkins = member.get("checkins", [])
            latest   = checkins[-1] if checkins else None
            col_card, col_btn = st.columns([7, 1])
            with col_card:
                summary_html = f'<div style="font-size:13px;color:#a89880;margin-top:6px;line-height:1.6">{latest["summary"]}</div>' if latest and latest.get("summary") else '<div style="font-size:13px;color:#3a3428;margin-top:6px">No check-ins yet</div>'
                date_html    = f'<div style="font-size:11px;color:#3a3428;margin-top:4px">Last check-in: {latest["date"]}</div>' if latest else ''
                st.markdown(f"""
                <div class="proj-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px">
                        <div class="proj-card-title">{member['name']}</div>
                        <span style="font-size:11px;color:#5a5248">{member.get('role','')}</span>
                    </div>
                    {summary_html}
                    {date_html}
                </div>""", unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                if st.button("→", key=f"open_member_{member['id']}"):
                    switch("team_member", member["id"])

elif st.session_state.view == "team_new_member":
    st.markdown('<div class="section-head">Add team member</div>', unsafe_allow_html=True)
    with st.form("new_member_form"):
        m_name = st.text_input("Name *", placeholder="e.g. Sarah")
        m_role = st.text_input("Role", placeholder="e.g. Research Associate")
        if st.form_submit_button("Add →"):
            if not m_name.strip():
                st.error("Please enter a name.")
            else:
                data.setdefault("team", []).append({
                    "id":       new_id(),
                    "name":     m_name.strip(),
                    "role":     m_role.strip(),
                    "checkins": [],
                })
                save_data(data)
                switch("team_overview")
                st.rerun()

elif st.session_state.view == "team_member":
    team   = data.get("team", [])
    member = next((m for m in team if m["id"] == st.session_state.selected_id), None)
    if not member:
        switch("team_overview"); st.rerun()

    checkins = member.get("checkins", [])

    col_h, col_a = st.columns([5, 1])
    with col_h:
        st.markdown(f'<div class="section-head">{member["name"]}</div>', unsafe_allow_html=True)
        if member.get("role"):
            st.markdown(f'<div style="font-size:13px;color:#5a5248;margin-top:-0.75rem;margin-bottom:1rem">{member["role"]}</div>', unsafe_allow_html=True)
    with col_a:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("🗑 Delete", key="del_member"):
            data["team"] = [m for m in team if m["id"] != member["id"]]
            save_data(data)
            switch("team_overview")
            st.rerun()

    # ── New check-in ──
    st.markdown('<div class="label-sm">New check-in</div>', unsafe_allow_html=True)
    with st.expander("＋ Log this week's check-in"):
        with st.form("new_checkin_form"):
            ci_date  = st.date_input("Date", value=date.today())
            ci_notes = st.text_area(
                "Your notes from the meeting *",
                placeholder="Write up what was discussed — what they're working on, progress, blockers, anything notable...",
                height=160,
            )
            ci_goals = st.text_area(
                "Goals / actions agreed",
                placeholder="What did they commit to by next check-in?",
                height=80,
            )
            if st.form_submit_button("Save & summarise with Claude →"):
                if not ci_notes.strip():
                    st.error("Please add your meeting notes.")
                else:
                    with st.spinner("Summarising with Claude..."):
                        try:
                            import anthropic
                            client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
                            prompt = f"""You are summarising a weekly check-in meeting note for a manager.

Person: {member['name']} ({member.get('role','')})
Date: {ci_date}
Manager's notes: {ci_notes}
Goals/actions agreed: {ci_goals}

Write a concise, structured summary with three short sections:
1. **Working on** — what they are currently focused on
2. **Progress** — what's going well or has been completed
3. **Blockers & needs** — anything stuck, at risk, or needing support

Keep each section to 2-3 sentences max. Be direct and factual. Return plain text only, no markdown formatting."""

                            msg = client.messages.create(
                                model="claude-sonnet-4-6",
                                max_tokens=500,
                                messages=[{"role":"user","content":prompt}]
                            )
                            summary = msg.content[0].text
                        except Exception as e:
                            summary = f"(Summary unavailable: {e})"

                    member["checkins"].append({
                        "id":      new_id(),
                        "date":    str(ci_date),
                        "notes":   ci_notes.strip(),
                        "goals":   ci_goals.strip(),
                        "summary": summary,
                    })
                    save_data(data)
                    st.rerun()

    # ── Latest snapshot ──
    if checkins:
        latest = checkins[-1]
        st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)
        st.markdown('<div class="label-sm">Latest snapshot</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:11px;color:#3a3428;margin-bottom:0.75rem">Check-in {latest["date"]}</div>', unsafe_allow_html=True)

        if latest.get("summary"):
            for line in latest["summary"].split("\n"):
                line = line.strip()
                if not line: continue
                if line.startswith(("1.","2.","3.","Working on","Progress","Blockers")):
                    st.markdown(f'<div style="font-size:12px;font-weight:600;color:#d6a564;margin:10px 0 3px;letter-spacing:0.05em;text-transform:uppercase">{line}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="font-size:13px;color:#a89880;line-height:1.6">{line}</div>', unsafe_allow_html=True)

        if latest.get("goals"):
            st.markdown('<div style="font-size:12px;font-weight:600;color:#d6a564;margin:12px 0 3px;letter-spacing:0.05em;text-transform:uppercase">Goals for next week</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:13px;color:#a89880;line-height:1.6">{latest["goals"]}</div>', unsafe_allow_html=True)

    # ── History ──
    if len(checkins) > 1:
        st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)
        st.markdown('<div class="label-sm">History</div>', unsafe_allow_html=True)
        for ci in reversed(checkins[:-1]):
            with st.expander(f"Check-in — {ci['date']}"):
                if ci.get("summary"):
                    st.markdown(f'<div style="font-size:13px;color:#a89880;line-height:1.6;white-space:pre-line">{ci["summary"]}</div>', unsafe_allow_html=True)
                if ci.get("goals"):
                    st.markdown(f'<div style="font-size:12px;color:#5a5248;margin-top:8px">Goals: {ci["goals"]}</div>', unsafe_allow_html=True)
                if ci.get("notes"):
                    with st.expander("Raw notes"):
                        st.markdown(f'<div style="font-size:12px;color:#5a5248;line-height:1.6">{ci["notes"]}</div>', unsafe_allow_html=True)
                if st.button("🗑 Delete this check-in", key=f"del_ci_{ci['id']}"):
                    member["checkins"] = [c for c in checkins if c["id"] != ci["id"]]
                    save_data(data)
                    st.rerun()

# ══════════════════════════════════════════════
# QUARTERLY GOALS
# ══════════════════════════════════════════════

elif st.session_state.view == "goals_overview":
    goals = data.get("goals", [])
    st.markdown('<div class="section-head">Quarterly goals</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Research team objectives — track progress through linked projects</div>', unsafe_allow_html=True)

    col_btn, col_q = st.columns([2, 3])
    with col_btn:
        if st.button("＋ Add goal", key="add_goal_btn"):
            switch("goals_new")
    with col_q:
        quarters = sorted(set(g.get("quarter","") for g in goals if g.get("quarter")), reverse=True)
        if quarters:
            selected_q = st.selectbox("Filter by quarter", ["All"] + quarters, label_visibility="collapsed")
        else:
            selected_q = "All"

    filtered = [g for g in goals if selected_q == "All" or g.get("quarter") == selected_q]

    if not filtered:
        st.markdown('<div style="font-size:13px;color:#3a3428;padding:1rem 0">No goals yet — add one above.</div>', unsafe_allow_html=True)
    else:
        st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)
        for goal in filtered:
            linked = [p for p in projects if p.get("goal_id") == goal["id"]]
            done_linked   = [p for p in linked if p.get("status") == "Complete"]
            avg_pct = int(sum(get_progress(p) for p in linked) / len(linked)) if linked else 0

            col_card, col_open = st.columns([7, 1])
            with col_card:
                linked_names = ", ".join(p["name"] for p in linked) if linked else "No projects linked"
                st.markdown(f"""
                <div class="proj-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                        <div class="proj-card-title">{goal['title']}</div>
                        <span style="font-size:11px;color:#5a5248;background:#1e1a16;border:1px solid #2a2420;border-radius:99px;padding:2px 9px">{goal.get('quarter','')}</span>
                    </div>
                    <div class="proj-card-desc">{goal.get('desc','')}</div>
                    <div class="prog-wrap"><div class="prog-fill" style="width:{avg_pct}%"></div></div>
                    <div style="display:flex;justify-content:space-between;font-size:11px;color:#3a3428;margin-top:6px">
                        <span>📁 {linked_names}</span>
                        <span>{len(done_linked)}/{len(linked)} projects done · {avg_pct}%</span>
                    </div>
                </div>""", unsafe_allow_html=True)
            with col_open:
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                if st.button("→", key=f"open_goal_{goal['id']}"):
                    switch("goal_detail", goal["id"])

elif st.session_state.view == "goals_new":
    st.markdown('<div class="section-head">New goal</div>', unsafe_allow_html=True)
    with st.form("new_goal_form"):
        g_title   = st.text_input("Goal *", placeholder="e.g. Establish synthetic data validation framework")
        g_desc    = st.text_area("Description", placeholder="What does success look like?")
        g_quarter = st.text_input("Quarter", placeholder="e.g. Q2 2026")
        if st.form_submit_button("Add goal →"):
            if not g_title.strip():
                st.error("Please enter a goal.")
            else:
                data.setdefault("goals", []).append({
                    "id":      new_id(),
                    "title":   g_title.strip(),
                    "desc":    g_desc.strip(),
                    "quarter": g_quarter.strip(),
                    "notes":   "",
                })
                save_data(data)
                switch("goals_overview")
                st.rerun()

elif st.session_state.view == "goal_detail":
    goals  = data.get("goals", [])
    goal   = next((g for g in goals if g["id"] == st.session_state.selected_id), None)
    if not goal:
        switch("goals_overview"); st.rerun()

    linked     = [p for p in projects if p.get("goal_id") == goal["id"]]
    unlinked   = [p for p in projects if not p.get("goal_id")]
    avg_pct    = int(sum(get_progress(p) for p in linked) / len(linked)) if linked else 0
    done_count = sum(1 for p in linked if p.get("status") == "Complete")

    col_h, col_a = st.columns([5, 1])
    with col_h:
        st.markdown(f'<div class="section-head">{goal["title"]}</div>', unsafe_allow_html=True)
        if goal.get("quarter"):
            st.markdown(f'<div style="font-size:12px;color:#5a5248;margin-top:-0.75rem;margin-bottom:1rem">{goal["quarter"]}</div>', unsafe_allow_html=True)
    with col_a:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("✏️ Edit", key="edit_goal_btn"):
            switch("goal_edit", goal["id"])

    c1, c2, c3 = st.columns(3)
    for col, num, lbl in [(c1, f"{avg_pct}%", "Avg progress"), (c2, f"{done_count}/{len(linked)}", "Projects done"), (c3, len(linked), "Linked projects")]:
        with col:
            st.markdown(f'<div class="metric-box"><div class="metric-num">{num}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="prog-wrap" style="height:6px;margin:1rem 0 0.75rem"><div class="prog-fill" style="width:{avg_pct}%"></div></div>', unsafe_allow_html=True)

    if goal.get("desc"):
        st.markdown(f'<div style="font-size:13px;color:#5a5248;margin-bottom:1rem">{goal["desc"]}</div>', unsafe_allow_html=True)

    st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)

    # Linked projects
    st.markdown('<div class="label-sm">Linked projects</div>', unsafe_allow_html=True)

    if not linked:
        st.markdown('<div style="font-size:13px;color:#3a3428;padding:0.5rem 0">No projects linked yet</div>', unsafe_allow_html=True)
    else:
        for p in linked:
            pct = get_progress(p)
            tasks = p.get("tasks", [])
            done  = sum(1 for t in tasks if t.get("done"))
            col_c, col_u, col_o = st.columns([6, 2, 1])
            with col_c:
                st.markdown(f"""
                <div class="proj-card" style="margin-bottom:6px">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                        <div class="proj-card-title">{p['name']}</div>
                        {status_badge(p.get('status','Active'))}
                    </div>
                    <div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>
                    <div style="font-size:11px;color:#3a3428;margin-top:5px">{done}/{len(tasks)} tasks · {pct}%</div>
                </div>""", unsafe_allow_html=True)
            with col_u:
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                if st.button("Unlink", key=f"unlink_{p['id']}"):
                    p.pop("goal_id", None)
                    save_data(data); st.rerun()
            with col_o:
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                if st.button("→", key=f"golink_{p['id']}"):
                    switch("detail", p["id"])

    # Link a project
    if unlinked:
        st.markdown("<div style='margin-top:0.75rem'></div>", unsafe_allow_html=True)
        with st.expander("＋ Link a project"):
            link_choice = st.selectbox("Choose project", [p["name"] for p in unlinked], label_visibility="collapsed")
            if st.button("Link project →", key="link_proj_btn"):
                chosen = next(p for p in unlinked if p["name"] == link_choice)
                chosen["goal_id"] = goal["id"]
                save_data(data); st.rerun()

    # Notes
    st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)
    st.markdown('<div class="label-sm">Notes</div>', unsafe_allow_html=True)
    g_notes = st.text_area("", value=goal.get("notes",""), placeholder="Progress notes, context, decisions...", height=120, label_visibility="collapsed", key="goal_notes")
    if g_notes != goal.get("notes",""):
        goal["notes"] = g_notes; save_data(data)

    st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)
    with st.expander("⚠️ Delete goal"):
        st.markdown('<div style="font-size:13px;color:#5a5248;margin-bottom:0.75rem">This will delete the goal. Linked projects will be unlinked but not deleted.</div>', unsafe_allow_html=True)
        if st.button("Delete goal", key="del_goal_btn"):
            for p in linked:
                p.pop("goal_id", None)
            data["goals"] = [g for g in goals if g["id"] != goal["id"]]
            save_data(data); switch("goals_overview"); st.rerun()

elif st.session_state.view == "goal_edit":
    goals = data.get("goals", [])
    goal  = next((g for g in goals if g["id"] == st.session_state.selected_id), None)
    if not goal:
        switch("goals_overview"); st.rerun()

    st.markdown('<div class="section-head">Edit goal</div>', unsafe_allow_html=True)
    with st.form("edit_goal_form"):
        g_title   = st.text_input("Goal *",       value=goal["title"])
        g_desc    = st.text_area("Description",   value=goal.get("desc",""))
        g_quarter = st.text_input("Quarter",      value=goal.get("quarter",""))
        c1, c2 = st.columns(2)
        with c1: save_g = st.form_submit_button("Save →")
        with c2: cancel = st.form_submit_button("Cancel")
        if save_g:
            if not g_title.strip(): st.error("Enter a goal title.")
            else:
                goal["title"]   = g_title.strip()
                goal["desc"]    = g_desc.strip()
                goal["quarter"] = g_quarter.strip()
                save_data(data); switch("goal_detail", goal["id"]); st.rerun()
        if cancel:
            switch("goal_detail", goal["id"]); st.rerun()

# ══════════════════════════════════════════════
# DAILY LOG
# ══════════════════════════════════════════════

elif st.session_state.view == "daily_log":
    logs = load_log()
    today_str = str(date.today())
    today_log = next((l for l in logs if l["date"] == today_str), None)

    st.markdown('<div class="section-head">Daily log</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Write up what you did today — Claude will clean it up and build your weekly summary</div>', unsafe_allow_html=True)

    # ── Today's entry ──
    st.markdown('<div class="label-sm">Today</div>', unsafe_allow_html=True)

    with st.form("daily_log_form"):
        existing_raw = today_log.get("raw", "") if today_log else ""
        raw_notes = st.text_area(
            "",
            value=existing_raw,
            placeholder="Just write freely — what did you work on today? Meetings, progress made, decisions, blockers, anything notable. Don't worry about formatting, Claude will clean it up.",
            height=200,
            label_visibility="collapsed",
        )
        if st.form_submit_button("Save & clean with Claude →"):
            if not raw_notes.strip():
                st.error("Add some notes first.")
            else:
                with st.spinner("Claude is tidying your notes..."):
                    try:
                        import anthropic
                        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY",""))
                        prompt = f"""A researcher has written up their work day in rough notes. Clean this into a concise, well-structured daily log entry.

Date: {today_str}
Raw notes: {raw_notes}

Format as 3-5 bullet points covering:
- What was worked on / completed
- Key decisions or progress made
- Anything blocked or outstanding

Keep it factual, concise, and in first person. Plain text only, use • for bullets."""

                        msg = client.messages.create(
                            model="claude-sonnet-4-6",
                            max_tokens=400,
                            messages=[{"role":"user","content":prompt}]
                        )
                        cleaned = msg.content[0].text
                    except Exception as e:
                        cleaned = raw_notes
                        st.warning(f"Couldn't reach Claude ({e}) — saved raw notes.")

                entry = {
                    "date":    today_str,
                    "raw":     raw_notes.strip(),
                    "cleaned": cleaned,
                }
                if today_log:
                    for i, l in enumerate(logs):
                        if l["date"] == today_str:
                            logs[i] = entry
                            break
                else:
                    logs.append(entry)

                save_log(logs)
                st.rerun()

    # Show today's cleaned entry if it exists
    if today_log and today_log.get("cleaned"):
        st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)
        st.markdown('<div class="label-sm">Today\'s cleaned entry</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background:#1a1612;border:1px solid #2a2420;border-radius:10px;padding:1.1rem 1.35rem">', unsafe_allow_html=True)
        for line in today_log["cleaned"].split("\n"):
            line = line.strip()
            if not line: continue
            st.markdown(f'<div style="font-size:14px;color:#a89880;line-height:1.8;padding:2px 0">{line}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)

    # ── Weekly summary ──
    st.markdown('<div class="label-sm">Weekly summary</div>', unsafe_allow_html=True)

    # Get this week's logs (Mon–today)
    today_dt   = date.today()
    week_start = today_dt - timedelta(days=today_dt.weekday())
    week_logs  = [l for l in logs if week_start <= date.fromisoformat(l["date"]) <= today_dt]

    col_info, col_btn = st.columns([4, 1])
    with col_info:
        st.markdown(f'<div style="font-size:13px;color:#5a5248">{len(week_logs)} entries this week ({week_start.strftime("%d %b")} – {today_dt.strftime("%d %b")})</div>', unsafe_allow_html=True)
    with col_btn:
        gen_summary = st.button("Generate →", key="gen_weekly")

    if gen_summary:
        if not week_logs:
            st.warning("No log entries this week yet.")
        else:
            with st.spinner("Building your weekly summary..."):
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY",""))

                    all_entries = "\n\n".join([
                        f"--- {l['date']} ---\n{l.get('cleaned', l.get('raw',''))}"
                        for l in sorted(week_logs, key=lambda x: x["date"])
                    ])

                    goals_text = ""
                    if data.get("goals"):
                        this_quarter_goals = [g for g in data["goals"] if g.get("quarter","") in [
                            f"Q{((date.today().month-1)//3)+1} {date.today().year}",
                            f"Q{((date.today().month-1)//3)+1}{date.today().year}",
                        ]]
                        if this_quarter_goals:
                            goals_text = "\n\nCurrent quarterly goals:\n" + "\n".join(f"- {g['title']}" for g in this_quarter_goals)

                    prompt = f"""You are summarising a researcher's work week based on their daily log entries.

{all_entries}{goals_text}

Write a structured weekly summary with four sections:

1. **What I accomplished** — key outputs, completions, progress made (3-5 bullets)
2. **Patterns & themes** — what dominated the week, recurring themes, how time was spent (2-3 sentences)
3. **Progress against quarterly goals** — how this week's work connects to the stated goals, or where there are gaps (2-3 sentences; if no goals provided, skip this section)
4. **Going into next week** — anything outstanding, blockers to address, momentum to carry forward (2-3 bullets)

Be direct, insightful, and specific. Plain text, use • for bullets."""

                    msg = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=700,
                        messages=[{"role":"user","content":prompt}]
                    )
                    weekly = msg.content[0].text
                    st.session_state.weekly_summary = weekly
                except Exception as e:
                    st.error(f"Couldn't generate summary: {e}")

    if st.session_state.get("weekly_summary"):
        st.markdown(f'<div style="background:#1a1612;border:1px solid #2a2420;border-radius:10px;padding:1.35rem 1.5rem;margin-top:0.75rem">', unsafe_allow_html=True)
        current_section = None
        for line in st.session_state.weekly_summary.split("\n"):
            line = line.strip()
            if not line: continue
            if line.startswith(("1.","2.","3.","4.","**What","**Patterns","**Progress","**Going")):
                clean = line.lstrip("1234. ").replace("**","")
                st.markdown(f'<div style="font-size:11px;font-weight:600;color:#d6a564;letter-spacing:0.08em;text-transform:uppercase;margin:14px 0 5px">{clean}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="font-size:13px;color:#a89880;line-height:1.7;padding:1px 0">{line}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr class='soft-div'>", unsafe_allow_html=True)

    # ── Past entries ──
    past = [l for l in sorted(logs, key=lambda x: x["date"], reverse=True) if l["date"] != today_str]
    if past:
        st.markdown('<div class="label-sm">Past entries</div>', unsafe_allow_html=True)
        for l in past[:14]:
            d = date.fromisoformat(l["date"])
            with st.expander(d.strftime("%A, %d %B %Y")):
                if l.get("cleaned"):
                    for line in l["cleaned"].split("\n"):
                        line = line.strip()
                        if line:
                            st.markdown(f'<div style="font-size:13px;color:#a89880;line-height:1.7">{line}</div>', unsafe_allow_html=True)
                if l.get("raw") and l["raw"] != l.get("cleaned",""):
                    with st.expander("Raw notes"):
                        st.markdown(f'<div style="font-size:12px;color:#5a5248;line-height:1.6">{l["raw"]}</div>', unsafe_allow_html=True)
                if st.button("🗑 Delete", key=f"del_log_{l['date']}"):
                    logs = [x for x in logs if x["date"] != l["date"]]
                    save_log(logs)
                    st.rerun()
