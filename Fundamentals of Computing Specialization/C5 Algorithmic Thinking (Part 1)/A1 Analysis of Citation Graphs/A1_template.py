import random
import alg_load_graph
from alg_dpa_trial import DPATrial
import matplotlib.pyplot as plt


CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def make_complete_graph(num_nodes):
    graph = {}
    for node in xrange(num_nodes):
        nodes = set([])
        for to_node in xrange(num_nodes):
            if node != to_node:
                nodes.add(to_node)
        graph[node] = nodes

    return graph


def compute_in_degrees(digraph):
    degrees = dict.fromkeys(digraph, 0)
    for node in digraph:
        for edge in digraph[node]:
            degrees[edge] += 1

    return degrees


def in_degree_distribution(digraph):
    computed = compute_in_degrees(digraph)
    distrib = {}
    for node in computed:
        degree = computed[node]
        if degree not in distrib:
            distrib[degree] = 1
        else:
            distrib[degree] += 1

    return distrib


def norm_dist(digraph):
    distribution = in_degree_distribution(digraph)
    sum_nodes = len(digraph)
    normalized = dict.fromkeys(distribution)
    for degree in distribution:
        normalized[degree] = distribution[degree] / float(sum_nodes)

    return normalized


def digraph_rand(num_nodes, prob):
    digraph = {}
    for node_i in xrange(num_nodes):
        edges = []
        for node_j in xrange(num_nodes):
            a = random.random()
            if a < prob and node_i != node_j:
                edges.append(node_j)
        digraph[node_i] = edges
    return digraph


def dpa_digraph_gen(target_node, step_node):
    dpa_graph = DPATrial(step_node)
    directed_graph = make_complete_graph(step_node)
    for i in range(step_node, target_node):
        directed_graph[i] = dpa_graph.run_trial(i)

    return directed_graph


############# Question 1

def question_1():
    citation_graph = alg_load_graph.load_graph(CITATION_URL)

    out_degrees = 0
    for node in citation_graph:
        out_degrees += len(citation_graph[node])

    x_vals, y_vals = [], []
    norm = norm_dist(citation_graph)
    for degree in norm:
        x_vals.append(degree)
        y_vals.append(norm[degree])

    plt.loglog(x_vals, y_vals, color="blue", linestyle='None', marker=".", markersize=6)
    plt.xlabel("Log Number of Degrees")
    plt.ylabel("Log Distribution")
    plt.title("Normalized Distribution of High Energy Physics Theory Papers")
    plt.show()


#question_1()


############# Question 2

def question_2():
    citation_graph = alg_load_graph.load_graph(CITATION_URL)

    out_degrees = 0
    for node in citation_graph:
        out_degrees += len(citation_graph[node])

    x_vals, y_vals = [], []
    norm = norm_dist(citation_graph)
    for degree in norm:
        x_vals.append(degree)
        y_vals.append(norm[degree])

    x_d0, y_d0 = [], []
    d0 = digraph_rand(5000, 0.2)
    norm_0 = norm_dist(d0)
    for degree in norm_0:
        x_d0.append(degree)
        y_d0.append(norm_0[degree])        
    
    x_d1, y_d1 = [], []
    d1 = digraph_rand(5000, 0.6)
    norm_1 = norm_dist(d1)
    for degree in norm_1:
        x_d1.append(degree)
        y_d1.append(norm_1[degree])
        
    x_d2, y_d2 = [], []
    d2 = digraph_rand(5000, 0.9)
    norm_2 = norm_dist(d2)
    for degree in norm_2:
        x_d2.append(degree)
        y_d2.append(norm_2[degree])

    plt.loglog(x_vals, y_vals, color="cyan", linestyle='None', marker=".", markersize=6)
    plt.loglog(x_d0, y_d0, color="blue", linestyle='None', marker=".", markersize=6)
    plt.loglog(x_d1, y_d1, color="black", linestyle='None', marker=".", markersize=6)
    plt.loglog(x_d2, y_d2, color="red", linestyle='None', marker=".", markersize=6)
    plt.xlabel("Log Number of Degrees")
    plt.ylabel("Log Distribution")
    plt.title("Normalized Distribution for Random Generated Digraphs")
    plt.show()


#question_2()
    
    
############# Question 3-5

def question_35():
    citation_graph = alg_load_graph.load_graph(CITATION_URL)

    out_degrees = 0
    for node in citation_graph:
        out_degrees += len(citation_graph[node])

    x_vals, y_vals = [], []
    norm = norm_dist(citation_graph)
    for degree in norm:
        x_vals.append(degree)
        y_vals.append(norm[degree])


    target_node = 27770
    step_node = 13

    dpa_graph = dpa_digraph_gen(target_node, step_node)

    x_dpavals, y_dpavals = [], []
    norm_dpa = norm_dist(dpa_graph)
    for degree in norm_dpa:
        x_dpavals.append(degree)
        y_dpavals.append(norm_dpa[degree])

    plt.loglog(x_vals, y_vals, color="cyan", linestyle='None', marker=".", markersize=6)
    plt.loglog(x_dpavals, y_dpavals, color="black", linestyle='None', marker=".", markersize=6)
    plt.xlabel("Log Number of Degrees")
    plt.ylabel("Log Distribution")
    plt.title("Normalized Distribution of High Energy Physics Theory Papers")
    plt.show()


#question_35()