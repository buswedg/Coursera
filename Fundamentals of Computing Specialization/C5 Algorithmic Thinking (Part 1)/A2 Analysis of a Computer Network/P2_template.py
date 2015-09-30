"""
Provided code for Application portion of Module 2
"""

import random
from collections import deque

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    for neighbor in ugraph[node]:
        ugraph[neighbor].remove(node)
    del ugraph[node]

def bfs_visited(ugraph, start_node):
    '''
	Run Breadth-First search from start_node on the undirected graph.
    Return a set of nodes that were visited.'''
    visited = set()
    queue = deque()
    visited.add(start_node)
    queue.append(start_node)
    while queue:
        node = queue.popleft()
        for neighbor in ugraph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited


def cc_visited(ugraph):
    '''
	Return a set of sets. Child sets are connected components
    of the undirected graph.'''
    connected_components = []
    remaining_nodes = set(ugraph.keys())
    while remaining_nodes:
        node = remaining_nodes.pop()
        visited = bfs_visited(ugraph, node)
        connected_components.append(visited)
        remaining_nodes -= visited
    return connected_components


def largest_cc_size(ugraph):
    '''
	Return size of the largest connected component of the given
    undirected graph.'''
    if not len(ugraph):
        return 0
    return max(map(len, cc_visited(ugraph)))


def remove_node(ugraph, node):
    '''
	Remove node from the graph. This also includes removal of the node
    from its neighbors.'''
    for neighbor in ugraph[node]:
        ugraph[neighbor].remove(node)
    del ugraph[node]


def compute_resilience(ugraph, attack_order):
    '''
	Compute graph resilience (size of the largest connected component)
    after removing each of provided nodes.'''
    ugraph = copy_graph(ugraph)
    resilience = [largest_cc_size(ugraph)]
    for node in attack_order:
        remove_node(ugraph, node)
        resilience.append(largest_cc_size(ugraph))
    return resilience