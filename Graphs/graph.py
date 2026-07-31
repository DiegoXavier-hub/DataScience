import matplotlib.pyplot as plt
import networkx as nx
import random

class Graph:
  def __init__(self):
    self.adjacency_list = {} #(node: [neighbors])

  def add_node(self, node):
    if node not in self.adjacency_list:
      self.adjacency_list[node] = set()
  
  def add_edge(self, node1, node2):
    self.add_node(node1)
    self.add_node(node2)
    self.adjacency_list[node1].add(node2)
    self.adjacency_list[node2].add(node1)

  def remove_node(self, node):
    if node in self.adjacency_list:
      for neighbor in self.adjacency_list[node]:
        self.adjacency_list[neighbor].remove(node)
      del self.adjacency_list[node]

  def remove_edge(self, node1, node2):
    if node1 in self.adjacency_list and node2 in self.adjacency_list[node1]:
      self.adjacency_list[node1].discard(node2)
      self.adjacency_list[node2].discard(node1)

  def get_neighbors(self, node):
    return self.adjacency_list.get(node, set())
  
  def visualize(self):
    G = nx.Graph()
    for node, neighbors in self.adjacency_list.items():
      for neighbor in neighbors:
        G.add_edge(node, neighbor)
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=16)
    plt.title("Graph Visualization")
    plt.show()


if __name__ == "__main__":
    
    def generate_random_graph(num_nodes, num_edges):
        g = Graph()
        for i in range(num_nodes):
            g.add_node(i)
        
        edges_added = 0
        while edges_added < num_edges:
            node1 = random.randint(0, num_nodes - 1)
            node2 = random.randint(0, num_nodes - 1)
            if node1 != node2 and node2 not in g.get_neighbors(node1):
                g.add_edge(node1, node2)
                edges_added += 1
        
        return g
    
    g = generate_random_graph(10, 8)
    g.visualize()