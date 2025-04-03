def euclidean_distance(point1, point2):
    return sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)) ** 0.5

def initialize_centroids(data):
    return [data[0], data[1], data[2]]  

def assign_clusters(data, centroids):

    clusters = {0: [], 1: [], 2: []}  

    for point in data:
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        closest_centroid = distances.index(min(distances))
        clusters[closest_centroid].append(point)
    
    return clusters

def update_centroids(clusters):
    new_centroids = []
    
    for cluster_points in clusters.values():
        if cluster_points:
            new_centroid = tuple(sum(dim) / len(cluster_points) for dim in zip(*cluster_points))
            new_centroids.append(new_centroid)
        else:
            new_centroids.append((0, 0)) 
    
    return new_centroids

def k_means(data, max_iters=100):
    centroids = initialize_centroids(data)

    for _ in range(max_iters):
        clusters = assign_clusters(data, centroids)
        new_centroids = update_centroids(clusters)

        if new_centroids == centroids:  # Check convergence
            break

        centroids = new_centroids  # Update 

    return centroids, clusters

data = [(1, 2), (2, 3), (3, 4), (8, 7), (8, 8), (25, 30), (24, 29), (23, 28)]
centroids, clusters = k_means(data)

print("Final Centroids:", centroids)
for cluster_id, points in clusters.items():
    print(f"Cluster {cluster_id}: {points}")
