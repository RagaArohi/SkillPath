"""
auto_update.py — SkillPath Weekly Resource Updater
----------------------------------------------------
Discovers new free tech learning resources using Groq + LLaMA,
then indexes them into Bonsai (OpenSearch) if they don't already exist.

Run manually:   python auto_update.py
Run weekly:     Schedule via GitHub Actions (see .github/workflows/update.yml)
"""

import os
import json
import time
import sys
from dotenv import load_dotenv
from opensearchpy import OpenSearch
from groq import Groq

load_dotenv()

# ── Clients ───────────────────────────────────────────────────────────────────
es = OpenSearch(
    os.environ.get("BONSAI_URL", ""),
    verify_certs=False,
)
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

INDEX = "cs-resources"

# ── Topic batches — rotates weekly ────────────────────────────────────────────
TOPIC_BATCHES = [
    ["Python", "JavaScript", "Web Development", "Data Structures & Algorithms"],
    ["Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision"],
    ["Data Science", "SQL", "Data Engineering", "Data Visualization"],
    ["Cloud Computing AWS", "Cloud Computing GCP", "DevOps", "Docker & Kubernetes"],
    ["Cybersecurity", "Linux", "Networking", "System Design"],
    ["React", "Node.js", "Flutter", "Mobile Development"],
    ["Open Source", "Git & GitHub", "Career in Tech", "Competitive Programming"],
    ["Rust", "Go", "TypeScript", "Backend Development"],
    ["Artificial Intelligence", "Prompt Engineering", "AI Ethics", "AI Tools"],
    ["Database Design", "PostgreSQL", "MongoDB", "Redis"],
    ["iOS Development", "Android Development", "Game Development", "Unity"],
    ["UI/UX Design", "Figma", "Accessibility", "Design Systems"],
]

SCHEMA_DESCRIPTION = """
Each resource must have exactly these fields:
- title: string
- url: string (real, working URL starting with https://)
- type: one of [course, video, roadmap, practice, reference, podcast, book]
- topic: string
- level: one of [beginner, intermediate, advanced]
- free: true
- description: string (1-2 sentences)
- learning_style: list from [visual, audio, text, hands-on, reference]
- pace: one of [self-paced, structured, micro-learning]
- goal: list from [understand concepts, build projects, get interview-ready, learn tools]
"""


def get_weekly_batch():
    week = int(time.strftime("%W"))
    return TOPIC_BATCHES[week % len(TOPIC_BATCHES)]


def discover_resources(topics: list, count_per_topic: int = 3) -> list:
    topics_str = ", ".join(topics)
    prompt = f"""You are a learning resource expert. Generate exactly {count_per_topic} FREE online learning resources for EACH of these topics: {topics_str}.

Rules:
- Only completely free resources (no paywall, no credit card)
- Only real resources with working URLs
- Use well-known platforms: YouTube, freeCodeCamp, Khan Academy, MIT OpenCourseWare, Coursera (audit), edX (audit), Kaggle, fast.ai, roadmap.sh, The Odin Project, MDN, official docs, etc.
- Mix levels and learning styles across the set

{SCHEMA_DESCRIPTION}

Respond ONLY with a valid JSON array. No explanation, no markdown fences. Start with [ and end with ]."""

    print(f"\n🔍 Discovering: {topics_str}...")

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.3,
        )
        raw = (response.choices[0].message.content or "").strip()

        # Strip markdown fences if present
        if "```" in raw:
            parts = raw.split("```")
            for part in parts:
                if not part:
                    continue
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("["):
                    raw = part
                    break

        resources = json.loads(raw)
        print(f"   ✔ Got {len(resources)} resources")
        return resources

    except json.JSONDecodeError as e:
        print(f"   ✘ JSON error: {e}")
        return []
    except Exception as e:
        print(f"   ✘ Error: {e}")
        return []


def resource_exists(title: str) -> bool:
    """Check if a resource with this title already exists in the index."""
    try:
        result = es.search(
            index=INDEX,
            body={
                "query": {"match_phrase": {"title": title}},
                "size": 1,
            },
        )
        return result["hits"]["total"]["value"] > 0
    except Exception:
        return False


def validate_resource(r: dict) -> bool:
    required = ["title", "url", "type", "topic", "level", "free",
                "description", "learning_style", "pace", "goal"]
    valid_types  = {"course", "video", "roadmap", "practice", "reference", "podcast", "book"}
    valid_levels = {"beginner", "intermediate", "advanced"}
    valid_paces  = {"self-paced", "structured", "micro-learning"}

    for field in required:
        if field not in r:
            return False
    if r.get("type")  not in valid_types:  return False
    if r.get("level") not in valid_levels: return False
    if r.get("pace")  not in valid_paces:  return False
    if not isinstance(r.get("learning_style"), list): return False
    if not isinstance(r.get("goal"), list):           return False
    if not str(r.get("url", "")).startswith("http"):  return False
    return True


def index_resource(r: dict) -> bool:
    try:
        es.index(index=INDEX, body=r)
        return True
    except Exception as e:
        print(f"   ✘ Index error: {e}")
        return False


def get_index_count() -> int:
    try:
        return es.count(index=INDEX)["count"]
    except Exception:
        return -1


def run_update(topics=None, count_per_topic=3):
    print("=" * 60)
    print("  SkillPath — Auto Resource Updater")
    print("=" * 60)

    if topics is None:
        topics = get_weekly_batch()

    print(f"\n📋 Topics: {', '.join(topics)}")
    print(f"📈 Resources before: {get_index_count()}")

    new_resources = discover_resources(topics, count_per_topic)

    if not new_resources:
        print("\n⚠️  Nothing discovered. Try again later.")
        return

    added = skipped = invalid = 0

    print(f"\n📑 Processing {len(new_resources)} resources...")

    for r in new_resources:
        title = r.get("title", "Unknown")

        if not validate_resource(r):
            print(f"   ✘ Invalid schema — {title}")
            invalid += 1
            continue

        if resource_exists(title):
            print(f"   ~ Duplicate  — {title}")
            skipped += 1
            continue

        if index_resource(r):
            print(f"   ✔ Added      — {title} ({r.get('topic')} · {r.get('level')})")
            added += 1
        else:
            invalid += 1

    print("\n" + "=" * 60)
    print(f"  ✅ Added:    {added}")
    print(f"  ~  Skipped:  {skipped} (duplicates)")
    print(f"  ✘  Invalid:  {invalid}")
    print(f"  📈 Total now: {get_index_count()}")
    print("=" * 60)


if __name__ == "__main__":
    # Optional: pass topics as args
    # python auto_update.py "Rust" "Go" "TypeScript"
    if len(sys.argv) > 1:
        run_update(topics=sys.argv[1:])
    else:
        run_update()