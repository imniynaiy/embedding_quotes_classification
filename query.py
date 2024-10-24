import os
import weaviate

headers = {
    "X-OpenAI-Api-Key": os.getenv("OpenAIApiKey")
}  # Replace with your OpenAI API key

client = weaviate.connect_to_local(headers=headers)
collection = client.collections.get("Quotes")

response = client.collections.list_all()

print(response)

response = collection.query.fetch_objects()

for o in response.objects:
    print(o.properties)

response = collection.query.fetch_objects(
    include_vector=True,
    return_properties=["content"],
    limit=10000
)

for o in response.objects:
    print(o.properties)

print(response.objects[0].vector["default"])

client.close()