import os
import weaviate
import json

headers = {
    "X-OpenAI-Api-Key": os.getenv("OpenAIApiKey")
}  # Replace with your OpenAI API key

client = weaviate.connect_to_local(headers=headers)


try:
    # Work with the client here - e.g.:
    assert client.is_live()

    metainfo = client.get_meta()
    print(json.dumps(metainfo, indent=2))
    pass

finally:  # This will always be executed, even if an exception is raised
    client.close()  # Close the connection & release resources