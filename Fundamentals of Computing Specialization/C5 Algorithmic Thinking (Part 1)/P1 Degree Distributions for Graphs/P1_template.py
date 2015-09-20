"""Compute indegree of a graph and degree distibution."""
EX_GRAPH0 = {
    0: set([1, 2]),
    1: set(),
    2: set()
}

EX_GRAPH1 = {
    0: set([1, 4, 5]),
    1: set([2, 6]),
    2: set([3]),
    3: set([0]),
    4: set([1]),
    5: set([2]),
    6: set()
}

EX_GRAPH2 = {
    0: set([1, 4, 5]),
    1: set([2, 6]),
    2: set([3, 7]),
    3: set([7]),
    4: set([1]),
    5: set([2]),
    6: set(),
    7: set([3]),
    8: set([1, 2]),
    9: set([0, 3, 4, 5, 6, 7])
}

def make_complete_graph(num_nodes):
    """
    Return dictionary of a directed graph with a specified
    number of nodes (num_nodes).
    """
    graph = {}
    if num_nodes < 1:
        return graph
    for node in range(0, num_nodes):
        neighbors = set([])
        for dummy_i in range(0, num_nodes):
            if dummy_i != node:
                neighbors.add(dummy_i)
        graph[node] = neighbors
    return graph

def compute_in_degrees(digraph):
    """
    Compute the in-degrees for nodes in graph. 	
    """
    result = {}
    if digraph == {}:
            return result
    for node in digraph:
        count = 0
        for dummy_node in digraph:
            if node in digraph[dummy_node]:
                count += 1
        result[node] = count         
    return result;
    
def in_degree_distribution(digraph):
    """
    Compute the unnormalized distribution of the in-degrees
    of the graph.
    """
    degree_dist = {}
    in_degrees_dict = compute_in_degrees(digraph)
    for node in in_degrees_dict:
        in_degrees = in_degrees_dict[node]
        if degree_dist.has_key(in_degrees):
            degree_dist[in_degrees] += 1
        else:
            degree_dist[in_degrees] = 1
    return degree_dist