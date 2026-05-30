import os
import datetime
import streamlit as st
from dotenv import load_dotenv
from opensearchpy import OpenSearch
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

st.set_page_config(
    page_title="SkillPath",
    page_icon="🛤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700;800&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f !important;
    color: #e2e8f0 !important;
}
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; }

.main, .block-container {
    background-color: #0a0a0f !important;
    padding-top: 2rem !important;
}

section[data-testid="stSidebar"] { background-color: #0a0a0f !important; }

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3rem; font-weight: 800;
    line-height: 1.1; color: #ffffff; margin-bottom: 0.3rem;
}
.hero-sub {
    font-size: 1rem; color: #475569; margin-bottom: 2rem;
}
.accent { color: #a78bfa; }

.step-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem; font-weight: 700;
    color: #ffffff; margin-bottom: 0.3rem;
}
.step-sub { font-size: 0.9rem; color: #475569; margin-bottom: 1rem; }
.section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem; font-weight: 700;
    color: #7c3aed; text-transform: uppercase;
    letter-spacing: 0.12em; margin-bottom: 0.8rem;
}

.resource-card {
    background: #13131f;
    border: 1.5px solid #1e1e2e;
    border-radius: 14px; padding: 1.2rem 1.4rem;
    margin-bottom: 0.9rem; transition: border-color 0.2s;
}
.resource-card:hover { border-color: #3b2f6e; }
.resource-card.active-step { border-color: #7c3aed; box-shadow: 0 0 0 1px #7c3aed22; }
.resource-card.done-step { opacity: 0.45; }
.resource-card.skipped-step { opacity: 0.3; }

.card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem; font-weight: 700;
    color: #f1f5f9; margin-bottom: 0.2rem;
}
.card-meta { font-size: 0.78rem; color: #334155; margin-bottom: 0.5rem; }
.card-desc { font-size: 0.88rem; color: #64748b; margin-bottom: 0.7rem; line-height: 1.5; }

.tag {
    display: inline-block; background: #1e1e2e; color: #475569;
    border-radius: 6px; padding: 2px 9px;
    font-size: 0.72rem; margin-right: 4px; margin-bottom: 4px;
}
.tag-style { background: #2d1f6e; color: #a78bfa; }
.tag-goal  { background: #0f2e1f; color: #34d399; }
.tag-done  { background: #0f2e1f; color: #34d399; }
.tag-step  { background: #7c3aed; color: #fff; font-weight: 700; }

.ai-box {
    background: #13131f;
    border: 1.5px solid #2d1f6e;
    border-radius: 14px; padding: 1.3rem 1.5rem; margin-bottom: 1.5rem;
}
.ai-label {
    font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem;
    font-weight: 700; color: #7c3aed;
    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem;
}
.ai-text { color: #94a3b8; font-size: 0.92rem; line-height: 1.65; }

.path-progress {
    background: #13131f; border-radius: 14px;
    padding: 1rem 1.3rem; margin-bottom: 1.2rem;
    display: flex; justify-content: space-between; align-items: center;
}
.path-label {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700; color: #ffffff; font-size: 0.95rem;
}
.path-count { color: #7c3aed; font-weight: 700; font-size: 0.95rem; }

.filter-panel {
    background: #13131f; border: 1.5px solid #1e1e2e;
    border-radius: 14px; padding: 1.2rem 1.4rem; margin-bottom: 1.2rem;
}

.divider { border: none; border-top: 1px solid #1e1e2e; margin: 1.5rem 0; }

.stButton > button {
    background: #7c3aed !important; color: white !important; border: none !important;
    border-radius: 10px !important; padding: 0.55rem 1.8rem !important;
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 700 !important;
    font-size: 0.95rem !important; cursor: pointer !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #6d28d9 !important; }

.stTextInput > div > div > input {
    background: #13131f !important; color: #e2e8f0 !important;
    border: 1.5px solid #1e1e2e !important; border-radius: 10px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: none !important;
}

.stRadio > div { gap: 0.5rem; }
.stRadio label { color: #94a3b8 !important; }
.stCheckbox label { color: #94a3b8 !important; }
.stSelectbox > div > div { background: #13131f !important; color: #e2e8f0 !important; border-color: #1e1e2e !important; }
.stMultiSelect > div > div { background: #13131f !important; color: #e2e8f0 !important; border-color: #1e1e2e !important; }

div[data-testid="stExpander"] {
    background: #13131f !important; border: 1.5px solid #1e1e2e !important;
    border-radius: 14px !important;
}
div[data-testid="stExpander"] summary { color: #a78bfa !important; }

.stSpinner > div { border-top-color: #7c3aed !important; }
.stWarning { background: #1a1410 !important; color: #f59e0b !important; border-color: #78350f !important; }
.stSuccess { background: #0f2e1f !important; color: #34d399 !important; border-color: #065f46 !important; }

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_es_client():
    return OpenSearch(os.environ.get("BONSAI_URL", ""), verify_certs=False)

@st.cache_resource
def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)


def ensure_user_paths_index():
    es = get_es_client()
    if not es.indices.exists(index="user_paths"):
        es.indices.create(index="user_paths", body={
            "mappings": {"properties": {
                "email":           {"type": "keyword"},
                "query":           {"type": "text"},
                "level":           {"type": "keyword"},
                "learning_styles": {"type": "keyword"},
                "pace":            {"type": "keyword"},
                "goals":           {"type": "keyword"},
                "path":            {"type": "object", "enabled": False},
                "created_at":      {"type": "date"},
                "updated_at":      {"type": "date"},
            }}
        })

def load_user_profile(email):
    try:
        es = get_es_client()
        res = es.search(index="user_paths", query={"term": {"email": email}}, size=1)
        hits = res["hits"]["hits"]
        if hits:
            return hits[0]["_id"], hits[0]["_source"]
    except Exception:
        pass
    return None, None

def save_user_profile(email, query, level, learning_styles, pace, goals, path):
    ensure_user_paths_index()
    es = get_es_client()
    doc_id, _ = load_user_profile(email)
    now = datetime.datetime.utcnow().isoformat()
    doc = {
        "email": email, "query": query, "level": level,
        "learning_styles": learning_styles, "pace": pace,
        "goals": goals, "path": path, "updated_at": now,
    }
    if doc_id:
        es.update(index="user_paths", id=doc_id, body={"doc": doc})
    else:
        doc["created_at"] = now
        es.index(index="user_paths", body=doc)

def update_path_only(email, path):
    es = get_es_client()
    doc_id, _ = load_user_profile(email)
    if doc_id:
        es.update(index="user_paths", id=doc_id, body={"doc": {
            "path": path,
            "updated_at": datetime.datetime.utcnow().isoformat()
        }})


def search_resources(query, level, learning_styles, pace, goals, exclude_urls=None, size=8):
    es = get_es_client()
    must = [{"multi_match": {
        "query": query, "fields": ["title^2", "description", "topic"],
        "fuzziness": "AUTO",
    }}] if query.strip() else [{"match_all": {}}]

    filters = [{"term": {"free": True}}]
    if level and level != "Any":
        filters.append({"term": {"level": level.lower()}})
    if learning_styles:
        filters.append({"terms": {"learning_style": learning_styles}})
    if pace and pace != "Any":
        filters.append({"term": {"pace": pace.lower().replace(" ", "-")}})
    if goals:
        filters.append({"terms": {"goal": goals}})

    body = {"query": {"bool": {"must": must, "filter": filters}}, "size": size}
    if exclude_urls:
        body["query"]["bool"]["must_not"] = [{"terms": {"url": exclude_urls}}]

    try:
        resp = es.search(index="cs-resources", body=body)
        return [hit["_source"] for hit in resp["hits"]["hits"]]
    except Exception as e:
        st.error(f"Search error: {e}")
        return []


def get_ai_recommendation(query, level, learning_styles, pace, goals, resources):
    groq = get_groq_client()
    resource_titles = [r["title"] for r in resources[:6]]
    prompt = f"""You are SkillPath, a friendly learning advisor for first-generation CS students in India.

A student is looking for: "{query}"
Their level: {level}
Learning style: {', '.join(learning_styles) if learning_styles else 'any'}
Pace preference: {pace}
Goals: {', '.join(goals) if goals else 'general learning'}

Top matching resources: {resource_titles}

Give a warm, encouraging 2–3 sentence recommendation. Tell them which resource to start with and why it suits their learning style. Be specific, practical, motivating. No bullet points."""

    try:
        resp = groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"(AI recommendation unavailable: {e})"


def build_path(resources):
    return [{
        "title":          r.get("title", ""),
        "description":    r.get("description", ""),
        "url":            r.get("url", ""),
        "level":          r.get("level", ""),
        "topic":          r.get("topic", ""),
        "type":           r.get("type", ""),
        "pace":           r.get("pace", "flexible"),
        "learning_style": r.get("learning_style", []),
        "goal":           r.get("goal", []),
        "status":         "pending",
    } for r in resources]


def render_card(r, step_num=None, show_feedback=False, idx=None, email=None):
    status = r.get("status", "pending")
    card_class = "resource-card"
    if status == "done":      card_class += " done-step"
    elif status == "skipped": card_class += " skipped-step"
    elif show_feedback:       card_class += " active-step"

    styles_html = "".join(f'<span class="tag tag-style">{s}</span>' for s in r.get("learning_style", []))
    goals_html  = "".join(f'<span class="tag tag-goal">{g}</span>'   for g in r.get("goal", []))
    type_tag    = f'<span class="tag">{r.get("type","")}</span>'
    level_tag   = f'<span class="tag">{r.get("level","")}</span>'
    pace_tag    = f'<span class="tag">{r.get("pace","")}</span>'
    step_badge  = f'<span class="tag tag-step">Step {step_num}</span> ' if step_num else ""
    done_badge  = '<span class="tag tag-done">✅ Done</span> '           if status == "done" else ""
    skip_badge  = '<span class="tag">⏭️ Skipped</span> '                 if status == "skipped" else ""

    st.markdown(f"""
    <div class="{card_class}">
        <div class="card-title">{step_badge}{done_badge}{skip_badge}
            <a href="{r.get('url','#')}" target="_blank"
               style="color:#f1f5f9;text-decoration:none;">🔗 {r.get('title','')}</a>
        </div>
        <div class="card-meta">{r.get('topic','')} &nbsp;·&nbsp; {type_tag} {level_tag} {pace_tag}</div>
        <div class="card-desc">{r.get('description','')}</div>
        <div>{styles_html}{goals_html}</div>
    </div>
    """, unsafe_allow_html=True)

    if show_feedback and status == "pending":
        c1, c2, c3, _ = st.columns([2, 2, 2, 4])
        if c1.button("✅ It worked!", key=f"yes_{idx}"):
            st.session_state.path[idx]["status"] = "done"
            if email: update_path_only(email, st.session_state.path)
            st.rerun()
        if c2.button("❌ Didn't work", key=f"no_{idx}"):
            existing_urls = [r2["url"] for r2 in st.session_state.path]
            replacements = search_resources(
                st.session_state.query, st.session_state.level,
                st.session_state.learning_styles, st.session_state.pace,
                st.session_state.goals, exclude_urls=existing_urls, size=3
            )
            if replacements:
                st.session_state.path[idx] = build_path([replacements[0]])[0]
                if email: update_path_only(email, st.session_state.path)
                st.success("Swapped for a better match!")
            else:
                st.session_state.path[idx]["status"] = "skipped"
                if email: update_path_only(email, st.session_state.path)
                st.warning("No more alternatives — marked as skipped.")
            st.rerun()
        if c3.button("⏭️ Skip", key=f"skip_{idx}"):
            st.session_state.path[idx]["status"] = "skipped"
            if email: update_path_only(email, st.session_state.path)
            st.rerun()


defaults = {
    "step": 0, "query": "", "level": "Any",
    "learning_styles": [], "pace": "Any", "goals": [],
    "email": "", "path": [], "ai_text": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def show_progress(step, total=4):
    pct = int((step - 1) / total * 100)
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <div style="display:flex;justify-content:space-between;
                    font-size:0.72rem;color:#334155;margin-bottom:6px;
                    font-family:'Space Grotesk',sans-serif;font-weight:700;
                    text-transform:uppercase;letter-spacing:0.08em;">
            <span style="color:#7c3aed;">Step {step} of {total}</span>
            <span>{pct}% done</span>
        </div>
        <div style="background:#13131f;border-radius:99px;height:5px;">
            <div style="background:linear-gradient(90deg,#7c3aed,#a78bfa);
                        width:{pct}%;height:5px;border-radius:99px;
                        transition:width 0.4s;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def step_label(text, sub=None):
    st.markdown(f"""
    <div class="step-label">{text}</div>
    {"" if not sub else f'<div class="step-sub">{sub}</div>'}
    """, unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-title">Skill<span class="accent">Path</span></div>
<div class="hero-sub">Free learning resources matched to <em>how you learn</em> — built for CS students in India 🇮🇳</div>
""", unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── STEP 0: Email ─────────────────────────────────────────────────────────────
if st.session_state.step == 0:
    step_label("Let's save your progress 💾", "Enter your email to pick up where you left off — no password needed.")

    email = st.text_input("Email", placeholder="you@example.com", label_visibility="collapsed")

    col_skip, col_next = st.columns([2, 3])
    with col_skip:
        if st.button("Skip — don't save"):
            st.session_state.email = ""
            st.session_state.step  = 1
            st.rerun()
    with col_next:
        if st.button("Continue →"):
            if email and "@" in email:
                st.session_state.email = email
                _, profile = load_user_profile(email)
                if profile:
                    st.session_state.path            = profile.get("path", [])
                    st.session_state.query           = profile.get("query", "")
                    st.session_state.level           = profile.get("level", "Any")
                    st.session_state.learning_styles = profile.get("learning_styles", [])
                    st.session_state.pace            = profile.get("pace", "Any")
                    st.session_state.goals           = profile.get("goals", [])
                    st.session_state.step            = 5
                else:
                    st.session_state.step = 1
                st.rerun()
            else:
                st.warning("Please enter a valid email.")


# ── STEP 1: Topic ─────────────────────────────────────────────────────────────
elif st.session_state.step == 1:
    show_progress(1)
    step_label("What do you want to learn? 🎯", "Type a topic — anything you're curious about.")

    query = st.text_input("Topic", value=st.session_state.query,
        placeholder="e.g. Python, machine learning, cybersecurity, DSA...",
        label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Next →"):
        if query.strip():
            st.session_state.query = query.strip()
            st.session_state.step  = 2
            st.rerun()
        else:
            st.warning("Please enter a topic to continue.")


# ── STEP 2: Level + Learning style ───────────────────────────────────────────
elif st.session_state.step == 2:
    show_progress(2)
    step_label("How much do you already know? 📚",
               f'Learning: <strong style="color:#a78bfa">{st.session_state.query}</strong>')

    level = st.radio("Your level", ["Beginner", "Intermediate", "Advanced", "Not sure"],
        index=0, horizontal=True, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    step_label("How do you learn best? 🧠", "Pick everything that fits you.")

    style_options = {
        "📹 Watch videos": "visual",
        "🎧 Listen to podcasts/lectures": "audio",
        "📖 Read articles/docs": "text",
        "💻 Build things hands-on": "hands-on",
        "📋 Use cheatsheets/references": "reference",
    }
    selected_styles = []
    cols = st.columns(2)
    for i, (label, value) in enumerate(style_options.items()):
        with cols[i % 2]:
            if st.checkbox(label, value=value in st.session_state.learning_styles):
                selected_styles.append(value)

    st.markdown("<br>", unsafe_allow_html=True)
    col_back, col_next = st.columns([1, 3])
    with col_back:
        if st.button("← Back"):
            st.session_state.step = 1; st.rerun()
    with col_next:
        if st.button("Next →"):
            st.session_state.level           = "Any" if level == "Not sure" else level
            st.session_state.learning_styles = selected_styles
            st.session_state.step            = 3
            st.rerun()


# ── STEP 3: Pace + Goal ───────────────────────────────────────────────────────
elif st.session_state.step == 3:
    show_progress(3)
    step_label("What's your pace? ⏱️", "Be honest — there's no wrong answer.")

    pace_options = {
        "🐢 Self-paced — I go at my own speed": "self-paced",
        "📅 Structured — I like a weekly schedule": "structured",
        "⚡ Micro-learning — 10–15 min sessions": "micro-learning",
        "🤷 No preference": "Any",
    }
    pace_label = st.radio("Pace", list(pace_options.keys()), label_visibility="collapsed")
    pace = pace_options[pace_label]

    st.markdown("<br>", unsafe_allow_html=True)
    step_label("What's your goal? 🏁", "Pick everything that applies.")

    goal_options = {
        "🧩 Understand concepts deeply": "understand concepts",
        "🛠️ Build real projects": "build projects",
        "💼 Get interview-ready": "get interview-ready",
        "🔧 Learn tools & frameworks": "learn tools",
    }
    selected_goals = []
    for label, value in goal_options.items():
        if st.checkbox(label, value=value in st.session_state.goals):
            selected_goals.append(value)

    st.markdown("<br>", unsafe_allow_html=True)
    col_back, col_next = st.columns([1, 3])
    with col_back:
        if st.button("← Back"):
            st.session_state.step = 2; st.rerun()
    with col_next:
        if st.button("Build my learning path →"):
            st.session_state.pace  = pace
            st.session_state.goals = selected_goals
            st.session_state.step  = 4
            st.rerun()


# ── STEP 4: Build path ────────────────────────────────────────────────────────
elif st.session_state.step == 4:
    show_progress(4)

    chips = [f'<span class="tag">{st.session_state.query}</span>']
    if st.session_state.level != "Any":
        chips.append(f'<span class="tag">{st.session_state.level}</span>')
    for s in st.session_state.learning_styles:
        chips.append(f'<span class="tag tag-style">{s}</span>')
    if st.session_state.pace != "Any":
        chips.append(f'<span class="tag">{st.session_state.pace}</span>')
    for g in st.session_state.goals:
        chips.append(f'<span class="tag tag-goal">{g}</span>')
    st.markdown(f'<div style="margin-bottom:1.2rem;">{"".join(chips)}</div>', unsafe_allow_html=True)

    with st.spinner("Building your learning path..."):
        results = search_resources(
            st.session_state.query, st.session_state.level,
            st.session_state.learning_styles, st.session_state.pace,
            st.session_state.goals, size=6
        )

    if not results:
        results = search_resources(
            st.session_state.query, st.session_state.level,
            [], "Any", [], size=6
        )

    if not results:
        results = search_resources(
            st.session_state.query, "Any", [], "Any", [], size=6
        )

    if not results:
        st.warning(f"We don't have resources for **{st.session_state.query}** yet. Try Python, Machine Learning, Cybersecurity, Web Dev, or DSA.")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Try a different topic"):
            st.session_state.step  = 1
            st.session_state.query = ""
            st.rerun()
        st.stop()
    else:
        with st.spinner("Getting your personalised recommendation..."):
            ai_text = get_ai_recommendation(
                st.session_state.query, st.session_state.level,
                st.session_state.learning_styles, st.session_state.pace,
                st.session_state.goals, results
            )
        path = build_path(results)
        st.session_state.path    = path
        st.session_state.ai_text = ai_text

        if st.session_state.email:
            save_user_profile(
                st.session_state.email, st.session_state.query,
                st.session_state.level, st.session_state.learning_styles,
                st.session_state.pace, st.session_state.goals, path
            )

        st.session_state.step = 5
        st.rerun()


# ── STEP 5: Learning path view ────────────────────────────────────────────────
elif st.session_state.step == 5:
    path  = st.session_state.path
    email = st.session_state.email

    if st.session_state.ai_text:
        st.markdown(f"""
        <div class="ai-box">
            <div class="ai-label">✦ SkillPath Recommendation</div>
            <div class="ai-text">{st.session_state.ai_text}</div>
        </div>
        """, unsafe_allow_html=True)

    done_count = sum(1 for r in path if r["status"] == "done")
    total      = len(path)
    pct        = int(done_count / total * 100) if total else 0

    st.markdown(f"""
    <div class="path-progress">
        <span class="path-label">🗺️ Your Learning Path</span>
        <span class="path-count">{done_count}/{total} done</span>
    </div>
    <div style="background:#13131f;border-radius:99px;height:6px;margin-bottom:1.5rem;">
        <div style="background:linear-gradient(90deg,#7c3aed,#a78bfa);
                    width:{pct}%;height:6px;border-radius:99px;transition:width 0.4s;"></div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔧 Refine your results"):
        st.markdown('<div style="color:#475569;font-size:0.88rem;margin-bottom:1rem;">Adjust filters to find better matches.</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            new_level = st.selectbox("Level",
                ["Any", "Beginner", "Intermediate", "Advanced"],
                index=["Any", "Beginner", "Intermediate", "Advanced"].index(
                    st.session_state.level if st.session_state.level in ["Any", "Beginner", "Intermediate", "Advanced"] else "Any"
                ),
            )
            new_pace = st.selectbox("Pace",
                ["Any", "self-paced", "structured", "micro-learning"],
                index=["Any", "self-paced", "structured", "micro-learning"].index(
                    st.session_state.pace if st.session_state.pace in ["Any", "self-paced", "structured", "micro-learning"] else "Any"
                ),
            )
        with col2:
            style_opts = ["visual", "audio", "text", "hands-on", "reference"]
            new_styles = st.multiselect("Learning style", style_opts,
                default=[s for s in st.session_state.learning_styles if s in style_opts])
            goal_opts = ["understand concepts", "build projects", "get interview-ready", "learn tools"]
            new_goals = st.multiselect("Goals", goal_opts,
                default=[g for g in st.session_state.goals if g in goal_opts])

        if st.button("🔄 Apply filters"):
            st.session_state.level           = new_level
            st.session_state.pace            = new_pace
            st.session_state.learning_styles = new_styles
            st.session_state.goals           = new_goals
            with st.spinner("Refreshing your path..."):
                new_results = search_resources(
                    st.session_state.query, new_level, new_styles, new_pace, new_goals, size=6
                )
            if new_results:
                st.session_state.path = build_path(new_results)
                if email:
                    save_user_profile(email, st.session_state.query, new_level,
                        new_styles, new_pace, new_goals, st.session_state.path)
                st.rerun()
            else:
                st.warning("No resources matched — try broadening your filters.")

    first_pending = next((i for i, r in enumerate(path) if r["status"] == "pending"), -1)

    for i, resource in enumerate(path):
        render_card(resource, step_num=i+1, show_feedback=(i == first_pending),
                    idx=i, email=email if email else None)

    if all(r["status"] in ("done", "skipped") for r in path):
        st.balloons()
        st.success("🎓 You've finished your learning path! Start over to explore a new topic.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Start over"):
        for key in ["step","query","level","learning_styles","pace","goals","path","ai_text","email"]:
            st.session_state.pop(key, None)
        st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;color:#1e1e2e;font-size:0.8rem;">'
    'Built by <strong style="color:#334155">Ragamrutha Chettupalli</strong> · '
    '<a href="https://github.com/RagaArohi/SkillPath" style="color:#7c3aed;">GitHub</a>'
    '</div>',
    unsafe_allow_html=True,
)