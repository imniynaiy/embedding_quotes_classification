import os
import weaviate
import weaviate.classes as wvc

headers = {
    "X-OpenAI-Api-Key": os.getenv("OpenAIApiKey")
}  # Replace with your OpenAI API key

client = weaviate.connect_to_local(headers=headers)

import numpy as np
from sklearn.cluster import KMeans
import pandas as pd

def perform_kmeans_clustering(client, class_name, n_clusters=5):
    """
    Perform k-means clustering on vectors stored in Weaviate
    
    Parameters:
    client: weaviate.Client
        Initialized Weaviate client
    class_name: str
        Name of the Weaviate class to analyze
    n_clusters: int
        Number of clusters for k-means
    vector_field: str
        Name of the vector field in Weaviate
        
    Returns:
    tuple:
        - DataFrame with object IDs and their cluster assignments
        - KMeans model
    """

    collection = client.collections.get(class_name)
    response = collection.query.fetch_objects(
        include_vector=True,
        return_properties=["content"],
        limit=10000
    )
    
    # Extract vectors and IDs
    vectors = []
    ids = []
    contents  = []
    for item in response.objects:
        vectors.append(item.vector['default'])
        ids.append(item.uuid)
        contents.append(item.properties['content'])
    
    # Convert to numpy array
    vectors = np.array(vectors)
    
    # Perform k-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_assignments = kmeans.fit_predict(vectors)
    
    # Create DataFrame with results
    results_df = pd.DataFrame({
        'object_id': ids,
        'content': contents,
        'cluster': cluster_assignments
    })
    
    return results_df, kmeans

def get_cluster_statistics(results_df, client, class_name, properties=None):
    """
    Get statistics and examples for each cluster
    
    Parameters:
    results_df: pd.DataFrame
        DataFrame with clustering results
    client: weaviate.Client
        Initialized Weaviate client
    class_name: str
        Name of the Weaviate class
    properties: list
        List of properties to fetch for examples
        
    Returns:
    dict: Statistics for each cluster
    """
    if properties is None:
        properties = []
        
    cluster_stats = {}
    
    for cluster in results_df['cluster'].unique():
        # Get object IDs in this cluster
        cluster_ids = results_df[results_df['cluster'] == cluster]['object_id'].tolist()
        
        # Get examples from this cluster
        query = (
            client.query
            .get(class_name, properties)
            .with_id()
            .with_where({
                "path": ["id"],
                "operator": "ContainsAny",
                "valueString": cluster_ids[:5]  # Get first 5 examples
            })
            .do()
        )
        
        cluster_stats[f"cluster_{cluster}"] = {
            "size": len(cluster_ids),
            "percentage": len(cluster_ids) / len(results_df) * 100,
            "examples": query['data']['Get'][class_name]
        }
    
    return cluster_stats


# Perform clustering
results_df, kmeans_model = perform_kmeans_clustering(
    client,
    class_name="Quotes",
    n_clusters=5
)

# 导出为 CSV 文件
# df.to_csv('output.csv', index=False)

# 导出为 Excel 文件
results_df.to_csv('output.xlsx', index=False)

# Get cluster statistics
cluster_stats = get_cluster_statistics(
    results_df,
    client,
    class_name="Quotes",
    properties=["content"]
)

# Print results
print("Clustering Results:")
print(results_df.head())
print("\nCluster Statistics:")
for cluster, stats in cluster_stats.items():
    print(f"\n{cluster}:")
    print(f"Size: {stats['size']} objects ({stats['percentage']:.2f}%)")
    print("Example titles:")
    for example in stats['examples'][:3]:
        print(f"- {example.get('title', 'No title')}")