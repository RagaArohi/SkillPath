from dotenv
import load_dotenv
load_dotenv()
import streamlit as st
from elasticsearch import Elasticsearch
from groq import Groq

# Keys
import os
# Keys — loaded from environment variables
ELASTIC_URL    = os.environ.get("ELASTIC_URL", "")
ELASTIC_API_KEY = os.environ.get("ELASTIC_API_KEY", "")
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")
# Connect
es = Elasticsearch(ELASTIC_URL, api_key=ELASTIC_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

def search_resources(query, level, learning_styles, goals):
    must = [{"multi_match": {"query": query, "fields": ["title", "description", "topic"]}}]
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

    results = es.search(index="cs-resources", query=search_query, size=5)
    return results["hits"]["hits"]

def get_ai_response(student_query, resources, learning_styles, pace, goals):
    resources_text = ""
    for hit in resources:
        r = hit["_source"]
        resources_text += f"- {r['title']}: {r['description']} (Level: {r['level']}, URL: {r['url']})\n"

    prompt = f"""You are a warm, helpful senior student guiding first-generation CS students in India.

Student said: "{student_query}"
Their learning style: {', '.join(learning_styles) if learning_styles else 'not specified'}
Their pace preference: {pace}
Their goal: {', '.join(goals) if goals else 'not specified'}

Based on these free resources:
{resources_text}

Write a friendly 3-4 sentence response that:
1. Acknowledges their specific situation
2. Recommends the single best resource and explains exactly why it matches HOW they learn
3. Gives one concrete action they can take today

Sound like a helpful friend, not a formal tutor."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- UI ---
st.set_page_config(page_title="PathFinder — CS Resource Guide", page_icon="🧭")

st.title("🧭 PathFinder")
st.subheader("Free learning resources matched to how YOU learn")
st.caption("Built for first-gen CS students in India who don't know where to start.")
st.markdown("---")

# Step 1 — What do you want to learn
query = st.text_area(
    "What do you want to learn or what's confusing you?",
    placeholder="e.g. I'm a 2nd year CS student interested in AI but don't know where to start",
    height=100
)

col1, col2 = st.columns(2)

with col1:
    level = st.selectbox("Your current level:", ["Any", "Beginner", "Intermediate", "Advanced"])
    pace = st.selectbox("How do you like to learn?", [
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

if st.button("Find My Resources →", type="primary"):
    if query.strip():
        with st.spinner("Finding resources matched to how you learn..."):
            pace_clean = pace.split("—")[0].strip().lower()
            hits = search_resources(query, level, learning_styles, goals)

            if hits:
                ai_response = get_ai_response(query, hits, learning_styles, pace_clean, goals)

                st.markdown("### 💬 My Recommendation")
                st.write(ai_response)

                st.markdown("### 📚 Resources Matched To You")
                for hit in hits:
                    r = hit["_source"]
                    with st.expander(f"**{r['title']}** — {r['level'].capitalize()}"):
                        st.write(r["description"])
                        col_a, col_b, col_c = st.columns(3)
                        col_a.markdown(f"**Type:** {r['type']}")
                        col_b.markdown(f"**Topic:** {r['topic']}")
                        col_c.markdown(f"**Pace:** {r.get('pace', 'flexible')}")
                        st.markdown(f"**Best for:** {', '.join(r.get('learning_style', []))}")
                        st.markdown(f"[Open Resource →]({r['url']})")
            else:
                st.warning("No exact matches found — try selecting fewer filters or different keywords.")
    else:
        st.warning("Tell me what you want to learn first!")

st.markdown("---")
st.caption("Free resources only. No ads. Built for students like you. 🇮🇳")