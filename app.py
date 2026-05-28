import os
import streamlit as st
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from groq import Groq

# ── Load secrets ──────────────────────────────────────────────────────────────
load_dotenv()

ELASTIC_ENDPOINT = os.environ.get("ELASTIC_ENDPOINT", "")
ELASTIC_API_KEY  = os.environ.get("ELASTIC_API_KEY", "")
GROQ_API_KEY     = os.environ.get("GROQ_API_KEY", "")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkillPath",
    page_icon="🛤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.1;
    color: #0f172a;
    margin-bottom: 0.3rem;
}

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.1rem;
    color: #64748b;
    margin-bottom: 2rem;
}

.accent { color: #6366f1; }

.resource-card {
    background: #ffffff;
    border: 1.5px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s;
}

.resource-card:hover {
    box-shadow: 0 4px 20px rgba(99,102,241,0.12);
    border-color: #a5b4fc;
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.2rem;
}

.card-meta {
    font-size: 0.82rem;
    color: #94a3b8;
    margin-bottom: 0.5rem;
}

.card-desc {
    font-size: 0.9rem;
    color: #475569;
    margin-bottom: 0.7rem;
}

.tag {
    display: inline-block;
    background: #f1f5f9;
    color: #475569;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.75rem;
    margin-right: 4px;
    margin-bottom: 4px;
}

.tag-style {
    background: #ede9fe;
    color: #6d28d9;
}

.tag-goal {
    background: #dcfce7;
    color: #166534;
}

.ai-box {
    background: linear-gradient(135deg, #eef2ff 0%, #f0fdf4 100%);
    border: 1.5px solid #c7d2fe;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 2rem;
}

.ai-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    color: #6366f1;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}

.divider {
    border: none;
    border-top: 1.5px solid #f1f5f9;
    margin: 1.5rem 0;
}

.stButton > button {
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.8rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s;
}

.stButton > button:hover {
    background: #4f46e5;
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Clients ───────────────────────────────────────────────────────────────────
@st.cache_resource
def get_es_client():
    return Elasticsearch(ELASTIC_ENDPOINT, api_key=ELASTIC_API_KEY)

@st.cache_resource
def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)


# ── Search ────────────────────────────────────────────────────────────────────
def search_resources(query, level, learning_styles, pace, goals):
    es = get_es_client()

    must = []
    if query.strip():
        must.append({
            "multi_match": {
                "query": query,
                "fields": ["title^2", "description", "topic"],
                "fuzziness": "AUTO",
            }
        })
    else:
        must.append({"match_all": {}})

    filters = [{"term": {"free": True}}]

    if level and level != "Any":
        filters.append({"term": {"level": level.lower()}})
    if learning_styles:
        filters.append({"terms": {"learning_style": learning_styles}})
    if pace and pace != "Any":
        filters.append({"term": {"pace": pace.lower().replace(" ", "-")}})
    if goals:
        filters.append({"terms": {"goal": goals}})

    body = {
        "query": {
            "bool": {
                "must": must,
                "filter": filters,
            }
        },
        "size": 10,
    }

    try:
        resp = es.search(index="cs-resources", body=body)
        return [hit["_source"] for hit in resp["hits"]["hits"]]
    except Exception as e:
        st.error(f"Search error: {e}")
        return []


# ── AI recommendation ─────────────────────────────────────────────────────────
def get_ai_recommendation(query, level, learning_styles, pace, goals, resources):
    groq = get_groq_client()

    resource_titles = [r["title"] for r in resources[:6]]
    styles_str = ", ".join(learning_styles) if learning_styles else "any"
    goals_str  = ", ".join(goals) if goals else "general learning"

    prompt = f"""You are SkillPath, a friendly learning advisor for first-generation CS students in India.

A student is looking for: "{query}"
Their level: {level}
Learning style: {styles_str}
Pace preference: {pace}
Goals: {goals_str}

Top matching resources found: {resource_titles}

Give a warm, encouraging 2–3 sentence recommendation. Tell them which resource to start with and why it suits their learning style. Be specific, practical, and motivating. Do not use bullet points."""

    try:
        resp = groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"(AI recommendation unavailable: {e})"


# ── Resource card ─────────────────────────────────────────────────────────────
def render_card(r):
    styles_html = "".join(f'<span class="tag tag-style">{s}</span>' for s in r.get("learning_style", []))
    goals_html  = "".join(f'<span class="tag tag-goal">{g}</span>'   for g in r.get("goal", []))
    type_tag    = f'<span class="tag">{r.get("type","")}</span>'
    level_tag   = f'<span class="tag">{r.get("level","")}</span>'
    pace_tag    = f'<span class="tag">{r.get("pace","")}</span>'

    st.markdown(f"""
    <div class="resource-card">
        <div class="card-title">🔗 <a href="{r.get('url','#')}" target="_blank" style="color:#1e293b;text-decoration:none;">{r.get('title','')}</a></div>
        <div class="card-meta">{r.get('topic','')} &nbsp;·&nbsp; {type_tag} {level_tag} {pace_tag}</div>
        <div class="card-desc">{r.get('description','')}</div>
        <div>{styles_html}{goals_html}</div>
    </div>
    """, unsafe_allow_html=True)


# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-title">Skill<span class="accent">Path</span></div>
<div class="hero-sub">Free learning resources matched to <em>how you learn</em> — built for CS students in India 🇮🇳</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Filters ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "What do you want to learn?",
        placeholder="e.g. machine learning, web development, DSA, Python...",
        label_visibility="visible",
    )

with col2:
    level = st.selectbox("Level", ["Any", "Beginner", "Intermediate", "Advanced"])

col3, col4, col5 = st.columns(3)

with col3:
    learning_styles = st.multiselect(
        "Learning style",
        ["visual", "audio", "text", "hands-on", "reference"],
        placeholder="Pick your style(s)",
    )

with col4:
    pace = st.selectbox("Pace", ["Any", "self-paced", "structured", "micro-learning"])

with col5:
    goals = st.multiselect(
        "Goal",
        ["understand concepts", "build projects", "get interview-ready", "learn tools"],
        placeholder="What's your goal?",
    )

search_clicked = st.button("Find my resources →")

# ── Results ────────────────────────────────────────────────────────────────────
if search_clicked or query:
    if not query.strip() and not learning_styles and not goals and level == "Any" and pace == "Any":
        st.info("Enter a topic or pick a filter to get started.")
    else:
        with st.spinner("Finding your path..."):
            results = search_resources(query, level, learning_styles, pace, goals)

        if not results:
            st.warning("No resources matched — try broader filters or a different topic.")
        else:
            # AI recommendation
            with st.spinner("Getting your personalised recommendation..."):
                ai_text = get_ai_recommendation(query, level, learning_styles, pace, goals, results)

            st.markdown(f"""
            <div class="ai-box">
                <div class="ai-label">✦ SkillPath Recommendation</div>
                <div style="color:#1e293b;font-size:0.97rem;line-height:1.6;">{ai_text}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"### {len(results)} resource{'s' if len(results) != 1 else ''} found")

            for r in results:
                render_card(r)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;color:#94a3b8;font-size:0.82rem;">'
    'Built by <strong>Ragamrutha Chettupalli</strong> · '
    '<a href="https://github.com/RagaArohi/SkillPath" style="color:#6366f1;">GitHub</a>'
    '</div>',
    unsafe_allow_html=True,
)