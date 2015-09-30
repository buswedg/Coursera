import random
import timeit
import time
from matplotlib import pyplot as plt
from alg_upa_trial import UPATrial
import P1_template as prj1
import P2_template as prj2
import alg_application2_provided as app2


def er_makegraph(num_nodes, probability):
    """
    Generates random undirected graph using ER algorithm
    """
    result = {}
    if num_nodes == 0:
        return result
    for node1 in range(0, num_nodes):
        if node1 not in result:
            result[node1] = set()
        for node2 in range(0, num_nodes):
            if node2 not in result:
                result[node2] = set()
            if (random.random() < probability and node1 != node2):
                result[node1].add(node2)
                result[node2].add(node1)
    return result


def upa_makegraph(num_nodes, iter_nodes):
    """
    Generates graph by UPA algorithm where num_nodes is a total number of nodes
    and iter_nodes is a number of edges added on each iteration
    """
    result = prj1.make_complete_graph(iter_nodes)
    upa = UPATrial(iter_nodes)
    if num_nodes <= iter_nodes:
        return result
    for step in range(iter_nodes, num_nodes):
        nodes_to_be_added = upa.run_trial(iter_nodes)
        result[step] = nodes_to_be_added
        for node in nodes_to_be_added:
            result[node].add(step)
    return result


def random_order(ugraph):
    nodes = ugraph.keys()
    random.shuffle(nodes)
    return nodes


def question1():
    NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
    network_graph = app2.load_graph(NETWORK_URL)
    network_idd = prj1.in_degree_distribution(network_graph)
    network_nodes = sum(network_idd.values())
    network_edges = sum([x * y for (x, y) in network_idd.iteritems()]) / 2
    network_prob = float(network_edges) / network_nodes / (network_nodes - 1)
    print "Network_nodes", network_nodes
    print "Network_edges", network_edges
    print "Network_prob", network_prob
    print "Network_m", network_edges  /float(network_nodes)

    er_graph = er_makegraph(1347, 0.00172)
    er_idd = prj1.in_degree_distribution(er_graph)
    er_nodes = sum(er_idd.values())
    er_edges = sum([x * y for (x, y) in er_idd.iteritems()]) / 2
    print "ER_nodes", er_nodes
    print "ER_edges", er_edges

    upa_graph = upa_makegraph(1347, 2)
    upa_idd = prj1.in_degree_distribution(upa_graph)
    upa_nodes = sum(upa_idd.values())
    upa_edges = sum([x * y for (x, y) in upa_idd.iteritems()]) / 2
    print "UPA_nodes", upa_nodes
    print "UPA_edges", upa_edges

    network_resilience = prj2.compute_resilience(network_graph, random_order(network_graph))
    er_resilience = prj2.compute_resilience(er_graph, random_order(er_graph))
    upa_resilience = prj2.compute_resilience(upa_graph, random_order(upa_graph))

    plt.plot(range(len(network_resilience)), network_resilience, '-r', label='Network graph')
    plt.plot(range(len(er_resilience)), er_resilience, '-b', label='ER-generated (p = 0.00172)')
    plt.plot(range(len(upa_resilience)), upa_resilience, '-g', label='UPA-generated (m = 2)')
    plt.title('Comparison of Networks Resilience')
    plt.ylabel('Size of the largest connected component')
    plt.xlabel('Number of nodes removed')
    plt.legend()
    plt.show()

question1()


def measure_targeted_order(n, m, func):
    graph = er_makegraph(n, m)
    return timeit.timeit(lambda: func(graph), number=1)


def fast_targeted_order(ugraph):
    """
    Compute a targeted attack order consisting of nodes of maximal degree.
    """
    n = len(ugraph)
    new_graph = app2.copy_graph(ugraph)
    degree_sets = {}
    for node, neighbors in ugraph.iteritems():
        degree_sets.setdefault(len(neighbors), set()).add(node)
    order = []
    i = 0
    for k in range(n-1, 0, -1):
        if degree_sets.has_key(k):
            while len(degree_sets[k]) != 0:
                max_degree_node = degree_sets[k].pop()
                for neighbor in new_graph[max_degree_node]:
                    d = len(new_graph[neighbor])
                    degree_sets[d].remove(neighbor)
                    degree_sets.setdefault(d-1, set()).add(neighbor)
                order.append(max_degree_node)
                prj2.delete_node(new_graph, max_degree_node)
                i += 1
    if i < n:
        order.extend(new_graph.keys())
    return order


def question3():
    running_time = []
    fast_running_time = []
    rng = range(10, 1000, 10)
    for n in rng:
        upa_graph = upa_makegraph(n, 5)
        time1 = time.time()
        tmp = app2.targeted_order(upa_graph)
        running_time.append(time.time() - time1)
        fast_time1 = time.time()
        tmp2 = fast_targeted_order(upa_graph)
        fast_running_time.append(time.time() - fast_time1)
    plt.plot(rng, running_time, '-r', label = 'Targeted Order')
    plt.plot(rng, fast_running_time, '-b', label = 'Fast Targeted Order')
    plt.title('Targeted Order Function Performance (desktop Python)')
    plt.ylabel('Execution Time (msec)')
    plt.xlabel('Number of Nodes (m = 5)')
    plt.legend()
    plt.show()

#question3()


def question4():
    NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
    network_graph = app2.load_graph(NETWORK_URL)
    network_idd = prj1.in_degree_distribution(network_graph)
    network_nodes = sum(network_idd.values())
    network_edges = sum([x * y for (x, y) in network_idd.iteritems()]) / 2
    network_prob = float(network_edges) / network_nodes / (network_nodes - 1)
    print "Network_nodes", network_nodes
    print "Network_edges", network_edges
    print "Network_prob", network_prob
    print "Network_m", network_edges  /float(network_nodes)

    er_graph = er_makegraph(1347, 0.00172)
    er_idd = prj1.in_degree_distribution(er_graph)
    er_nodes = sum(er_idd.values())
    er_edges = sum([x * y for (x, y) in er_idd.iteritems()]) / 2
    print "ER_nodes", er_nodes
    print "ER_edges", er_edges

    upa_graph = upa_makegraph(1347, 2)
    upa_idd = prj1.in_degree_distribution(upa_graph)
    upa_nodes = sum(upa_idd.values())
    upa_edges = sum([x * y for (x, y) in upa_idd.iteritems()]) / 2
    print "UPA_nodes", upa_nodes
    print "UPA_edges", upa_edges

    network_resilience = prj2.compute_resilience(network_graph, fast_targeted_order(network_graph))
    er_resilience = prj2.compute_resilience(er_graph, fast_targeted_order(er_graph))
    upa_resilience = prj2.compute_resilience(upa_graph, fast_targeted_order(upa_graph))

    plt.plot(range(len(network_resilience)), network_resilience, '-r', label='Network graph')
    plt.plot(range(len(er_resilience)), er_resilience, '-b', label='ER-generated (p = 0.00172)')
    plt.plot(range(len(upa_resilience)), upa_resilience, '-g', label='UPA-generated (m = 2)')
    plt.title('Comparison of Networks Resilience')
    plt.ylabel('Size of the largest connected component')
    plt.xlabel('Number of nodes removed')
    plt.legend()
    plt.show()

#question4()