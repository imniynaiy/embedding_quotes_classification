import os
import time
import weaviate
import weaviate.classes.config as wc


headers = {
    "X-OpenAI-Api-Key": os.getenv("OpenAIApiKey")
}  # Replace with your OpenAI API key

client = weaviate.connect_to_local(headers=headers)

quotes = client.collections.get("Quotes")

def save(line):
    time.sleep(0.5)
    print(line)
    quotes.data.insert(
        properties={
            "content": line
        },
    )

def process_file(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():  # Check if line is not empty
                    save(line)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
filename = "100.txt"
process_file(filename)

client.close()