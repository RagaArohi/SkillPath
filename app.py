import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from elasticsearch import Elasticsearch
from groq import Groq
import datetime

ELASTIC_URL     = os.environ.get("ELASTIC_ENDPOINT", "")
ELASTIC_API_KEY = os.environ.get("ELASTIC_API_KEY", "")
GROQ_API_KEY    = os.environ.get("GROQ_API_KEY", "")

es          = Elasticsearch(ELASTIC_URL, api_key=ELASTIC_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

def ensure_user_paths_index():
    if not es.indices.exists(index="user_paths"):
        es.indices.create(index="user_paths", body={
            "mappings": {
                "properties": {
                    "email":           {"type": "keyword"},
                    "query":           {"type": "text"},
                    "level":           {"type": "keyword"},
                    "learning_styles": {"type": "keyword"},
                    "pace":            {"type": "keyword"},
                    "goals":           {"type": "keyword"},
                    "path":            {"type": "object", "enabled": False},
                    "created_at":      {"type": "date"},
                    "updated_at":      {"type": "date"},
                }
            }
        })

def load_user_profile(email):
    try:
        res = es.search(index="user_paths", query={"term": {"email": email}}, size=1)
        hits = res["hits"]["hits"]
        if hits:
            return hits[0]["_id"], hits[0]["_source"]
    except Exception:
        pass
    return None, None

def save_user_profile(email, query, level, learning_styles, pace, goals, path):
    ensure_user_paths_index()
    doc_id, existing = load_user_profile(email)
    now = datetime.datetime.utcnow().isoformat()
    doc = {
        "email": email,
        "query": query,
        "level": level,
        "learning_styles": learning_styles,
        "pace": pace,
        "goals": goals,
        "path": path,
        "updated_at": now,
    }
    if doc_id:
        es.update(index="user_paths", id=doc_id, body={"doc": doc})
    else:
        doc["created_at"] = now
        es.index(index="user_paths", body=doc)

def update_path_only(email, path):
    doc_id, _ = load_user_profile(email)
    if doc_id:
        es.update(index="user_paths", id=doc_id, body={
            "doc": {
                "path": path,
                "updated_at": datetime.datetime.utcnow().isoformat()
            }
        })

def search_resources(query, level, learning_styles, goals, exclude_urls=None, size=8):
    must = [{"multi_match": {
        "query": query,
        "fields": ["title", "description", "topic"],
        "fuzziness": "AUTO"
    }}]
    filters = []
    if level and level != "Any":
        filters.append({"term": {"level": level.lower()}})
    if learning_styles:
        filters.append({"terms": {"learning_style": learning_styles}})
    if goals:
        filters.append({"terms": {"goal": goals}})

    search_query = {"bool": {"must": must}}
    if filters:
        search_query["bool"]["filter"] = filters
    if exclude_urls:
        search_query["bool"]["must_not"] = [{"terms": {"url": exclude_urls}}]

    results = es.search(index="cs-resources", query=search_query, size=size)
    return results["hits"]["hits"]

def get_ai_intro(student_query, resources, learning_styles, pace, goals):
    resources_text = "\n".join(
        f"- {h['_source']['title']}: {h['_source']['description']}"
        for h in resources[:5]
    )
    prompt = f"""You are a warm senior student helping a first-gen CS student in India.

Student: "{student_query}"
Learning style: {', '.join(learning_styles) if learning_styles else 'not specified'}
Pace: {pace}
Goal: {', '.join(goals) if goals else 'not specified'}

Resources found:
{resources_text}

Write 2-3 friendly sentences:
1. Acknowledge their situation briefly
2. Tell them you've built a learning path for them and they should try Step 1 first

Sound like a helpful friend, not a formal tutor. Keep it short."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def build_path_from_hits(hits):
    path = []
    for hit in hits:
        r = hit["_source"]
        path.append({
            "title":         r.get("title", ""),
            "description":   r.get("description", ""),
            "url":           r.get("url", ""),
            "level":         r.get("level", ""),
            "topic":         r.get("topic", ""),
            "type":          r.get("type", ""),
            "pace":          r.get("pace", "flexible"),
            "learning_style": r.get("learning_style", []),
            "status":        "pending",
        })
    return path

st.set_page_config(page_title="SkillPath", page_icon="🧭")
st.title("🧭 SkillPath")
st.subheader("Free learning resources matched to how YOU learn")
st.caption("Built for first-gen CS students in India who don't know where to start.")
st.markdown("---")

email = st.text_input(
    "📧 Enter your email to save your progress",
    placeholder="you@example.com"
)

returning_user = False
if email and "@" in email:
    doc_id, profile = load_user_profile(email)
    if profile:
        returning_user = True
        st.success("Welcome back! Resuming your learning path.")
        if "path" not in st.session_state:
            st.session_state.path            = profile.get("path", [])
            st.session_state.query           = profile.get("query", "")
            st.session_state.level           = profile.get("level", "Any")
            st.session_state.learning_styles = profile.get("learning_styles", [])
            st.session_state.pace            = profile.get("pace", "self-paced")
            st.session_state.goals           = profile.get("goals", [])
            st.session_state.email           = email
            st.session_state.submitted       = True

if not returning_user and "submitted" not in st.session_state:
    query = st.text_area(
        "What do you want to learn or what's confusing you?",
        placeholder="e.g. I'm a 2nd year CS student interested in AI but don't know where to start",
        height=100
    )
    col1, col2 = st.columns(2)
    with col1:
        level = st.selectbox("Your current level:", ["Any", "Beginner", "Intermediate", "Advanced"])
        pace_raw = st.selectbox("Your pace:", [
            "Self-paced — I go at my own speed",
            "Structured — I need deadlines and schedules",
            "Micro-learning — Short bursts, 10-15 mins at a time"
        ])
    with col2:
        learning_styles = st.multiselect("How do you learn best?", [
            "visual", "audio", "text", "hands-on", "reference"
        ], placeholder="Pick all that apply")
        goals = st.multiselect("What's your goal?", [
            "understand concepts", "build projects", "get interview-ready", "learn tools"
        ], placeholder="Pick all that apply")

    if st.button("Build My Learning Path →", type="primary"):
        if not email or "@" not in email:
            st.warning("Please enter your email above to save your progress.")
        elif query.strip():
            with st.spinner("Building your personal learning path..."):
                pace_clean = pace_raw.split("—")[0].strip().lower()
                hits = search_resources(query, level, learning_styles, goals, size=6)
                if hits:
                    path     = build_path_from_hits(hits)
                    ai_intro = get_ai_intro(query, hits, learning_styles, pace_clean, goals)
                    save_user_profile(email, query, level, learning_styles, pace_clean, goals, path)
                    st.session_state.path            = path
                    st.session_state.ai_intro        = ai_intro
                    st.session_state.query           = query
                    st.session_state.level           = level
                    st.session_state.learning_styles = learning_styles
                    st.session_state.pace            = pace_clean
                    st.session_state.goals           = goals
                    st.session_state.email           = email
                    st.session_state.submitted       = True
                    st.rerun()
                else:
                    st.warning("No matches found — try broader keywords or fewer filters.")
        else:
            st.warning("Tell me what you want to learn first!")

if "submitted" in st.session_state and "path" in st.session_state:
    path  = st.session_state.path
    email = st.session_state.get("email", "")

    if "ai_intro" in st.session_state:
        st.markdown("### 💬 Your mentor says")
        st.write(st.session_state.ai_intro)

    st.markdown("### 🗺️ Your Learning Path")
    done_count   = sum(1 for r in path if r["status"] == "done")
    total        = len(path)
    st.progress(done_count / total if total else 0, text=f"{done_count} of {total} completed")

    first_pending = next((j for j, r in enumerate(path) if r["status"] == "pending"), -1)

    for i, resource in enumerate(path):
        status = resource["status"]
        badge  = "✅" if status == "done" else ("🔄" if status == "skipped" else f"Step {i+1}")

        with st.expander(f"{badge} — {resource['title']} ({resource['level'].capitalize()})", expanded=(i == first_pending)):
            st.write(resource["description"])
            col_a, col_b, col_c = st.columns(3)
            col_a.markdown(f"**Type:** {resource['type']}")
            col_b.markdown(f"**Topic:** {resource['topic']}")
            col_c.markdown(f"**Pace:** {resource['pace']}")
            if resource["learning_style"]:
                st.markdown(f"**Best for:** {', '.join(resource['learning_style'])}")
            st.markdown(f"[Open Resource →]({resource['url']})")

            if status == "pending":
                st.markdown("---")
                st.markdown("**Did this resource work for you?**")
                c1, c2, c3 = st.columns(3)
                if c1.button("✅ Yes, it worked!", key=f"yes_{i}"):
                    st.session_state.path[i]["status"] = "done"
                    if email:
                        update_path_only(email, st.session_state.path)
                    st.rerun()
                if c2.button("❌ Didn't work", key=f"no_{i}"):
                    existing_urls = [r["url"] for r in st.session_state.path]
                    replacements  = search_resources(
                        st.session_state.query,
                        st.session_state.level,
                        st.session_state.learning_styles,
                        st.session_state.goals,
                        exclude_urls=existing_urls,
                        size=3
                    )
                    if replacements:
                        st.session_state.path[i] = build_path_from_hits([replacements[0]])[0]
                        if email:
                            update_path_only(email, st.session_state.path)
                        st.success("Swapped for a better match!")
                    else:
                        st.session_state.path[i]["status"] = "skipped"
                        if email:
                            update_path_only(email, st.session_state.path)
                        st.warning("No more alternatives — marked as skipped.")
                    st.rerun()
                if c3.button("⏭️ Skip", key=f"skip_{i}"):
                    st.session_state.path[i]["status"] = "skipped"
                    if email:
                        update_path_only(email, st.session_state.path)
                    st.rerun()
            elif status == "done":
                st.success("Completed! 🎉")
            elif status == "skipped":
                st.info("Skipped — come back to this later.")

    if all(r["status"] in ("done", "skipped") for r in path):
        st.balloons()
        st.success("🎓 You've finished your learning path! Come back with a new topic to keep going.")

    st.markdown("---")
    if st.button("🔄 Start a new search"):
        for key in ["path", "submitted", "ai_intro", "query", "level", "learning_styles", "pace", "goals"]:
            st.session_state.pop(key, None)
        st.rerun()

st.markdown("---")
st.caption("Free resources only. No ads. Built for students like you. 🇮🇳")