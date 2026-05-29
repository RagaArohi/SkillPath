from opensearchpy import OpenSearch
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenSearch(os.environ.get("BONSAI_URL", ""), verify_certs=False)
# Delete old index if it exists
try:
    if client.indices.exists(index="cs-resources"):
        client.indices.delete(index="cs-resources")
        print("Old index deleted.")
except Exception as e:
    print(f"Note: {e}")

# Create new index with updated schema
client.indices.create(index="cs-resources", body={"mappings": {
    "properties": {
        "title":          {"type": "text"},
        "url":            {"type": "keyword"},
        "type":           {"type": "keyword"},
        "topic":          {"type": "text"},
        "level":          {"type": "keyword"},
        "free":           {"type": "boolean"},
        "description":    {"type": "text"},
        "learning_style": {"type": "keyword"},
        "pace":           {"type": "keyword"},
        "goal":           {"type": "keyword"}
    }
}})
print("New index created with updated schema!")