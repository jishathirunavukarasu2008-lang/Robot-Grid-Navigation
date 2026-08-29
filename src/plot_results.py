import matplotlib.pyplot as plt

experiments = [
    "Simple Grid",
    "Obstacle Grid",
    "No Path"
]

nodes_expanded = [14, 17, 1]

plt.figure(figsize=(8, 5))
plt.bar(experiments, nodes_expanded)

plt.title("BFS Nodes Expanded in Different Grid Configurations")
plt.xlabel("Experiment")
plt.ylabel("Nodes Expanded")

plt.tight_layout()
plt.savefig("bfs_nodes_expanded.png", dpi=300)
plt.show()
