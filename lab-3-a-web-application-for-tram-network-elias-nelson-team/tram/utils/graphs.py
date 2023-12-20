
import networkx as nx
import graphviz as gz



class Graph(nx.Graph):
    def __init__(self, start=None):
        super().__init__(start)
        self._values = {}

    # Returns an adjacency list representation of the graph
    def print_adjacency_list(self):
        adj_dict = {}
        for node in self.nodes():
            neighbors = list(super().neighbors(node))  
            adj_dict[node] = neighbors
        return adj_dict
    
    # Returns a list of all vertices in the graph
    def vertices(self):
        return self.nodes()
  
    # Returns a list of all edges in the graph
    def edges(self):
        return list(super().edges())
   
    # Returns a list of neighbors for a given vertex
    def neighbors(self, v):
        return list(super().neighbors(v))
    
    # Returns boolean saying if the graph is directed
    def is_directed(self):
        return super().is_directed()
    
    # Returns the number of vertices in the graph
    def number_of_vertices(self):
        return len(self._values)
    
    # Returns the number of vertices in the graph
    def __len__(self):
        return self.number_of_vertices()
    
    # Adds a vertex to the graph
    def add_vertex(self, a):
        super().add_node(a)
        self._values[a] = None         

    # Gets the value associated with a vertex
    def get_vertex_value(self, v):
        return self._values[v]
    
    # Sets the value associated with a vertex
    def set_vertex_value(self, v, x):
        self._values[v] = x   

    # Removes an edge from the graph
    def remove_edge(self, a, b):
        return super().remove_edge(a,b)    
    
    # Removes a vertex from the graph
    def remove_vertex(self, v):
        del self._values[v]
        return super().remove_node(v)   
    
    
    # Returns a dictionary with the shortest path to all nodes of the graph.        
    def dijkstra(self, source, cost=lambda u, v: 1):
        self.costs2attributes(cost=cost)
        return nx.shortest_path(self, source, weight='weight')
        

    # Helper function to convert costs to edge attributes
    def costs2attributes(self, cost, attr='weight'):
        for a, b in self.edges():
            self[a][b][attr] = cost(a, b)


    # Calculates the shortest distance and path between two nodes
    def shortest_path(self, source=None, target=None, weight=None, method='dijkstra', cost=lambda u, v: 1):
        shortest_path = self.dijkstra(source, cost)[target]
        shortest_path_length = 0
        
        for current_node, next_node in list(zip(shortest_path[:-1], shortest_path[1:])):
            shortest_path_length += self.get_weight(current_node, next_node)

        return shortest_path_length,shortest_path
    

    # Visualizes the shortest path
    def view_shortest(self, source, target, cost=lambda u, v: 1):
        path_length, path = self.shortest_path(source=source, target=target, cost=cost)
        
        # Create a color map for nodes on the path
        colormap = {str(node): 'orange' for node in path}
        dot = gz.Graph()

        # Add nodes with specified colors
        for node in self.nodes():
            dot.node(str(node), style = "filled", fillcolor=colormap.get(str(node), "white"))
        
        # Add edges to the graph
        for edge in self.edges():
            dot.edge(str(edge[0]), str(edge[1]))

        # Render and view the graph
        dot.render("output", view=True, format ="pdf")
     
 
class WeightedGraph(Graph):
    def __init__(self, start=None): 
        super().__init__(start)
        
    # Sets the weight of an edge
    def set_weight(self, a, b, w):
        if self.has_edge(a,b):
            self[a][b]["weight"] = w
        else:
            raise ValueError(f"No edge between {a} and {b}")
        
    # Gets the weight of an edge
    def get_weight(self, a, b):
        if self.has_edge(a, b) and "weight" in self[a][b]:
            return self[a][b]['weight']
        else:
            raise ValueError(f"No weight between {a} and {b}")