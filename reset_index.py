from elasticsearch import Elasticsearch

client = Elasticsearch(
    "https://my-elasticsearch-project-b4fa48.es.us-central1.gcp.elastic.cloud",
    api_key="RndsZ2FwNEI0U3MzYXpybFV3TXA6TGNkZVNzUl9YSnhhTXhkNkxhcUppUQ=="
)

# Delete old index
if client.indices.exists(index="cs-resources"):
    client.indices.delete(index="cs-resources")
    print("Old index deleted.")

# Create new index with updated schema
client.indices.create(index="cs-resources", mappings={
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
})
print("New index created with updated schema!")