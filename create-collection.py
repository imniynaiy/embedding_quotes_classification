import os
import weaviate
import weaviate.classes.config as wc


headers = {
    "X-OpenAI-Api-Key": os.getenv("OpenAIApiKey")
}  # Replace with your OpenAI API key

client = weaviate.connect_to_local(headers=headers)

client.collections.create(
    name="Quotes",
    properties=[
        wc.Property(name="content", data_type=wc.DataType.TEXT),
    ],
    # Define the vectorizer module
    vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
)

client.close()