import sys, os, time
import networkx as nx

def calculate_score(D1, D2, g):
    # Using set intersection directly for improved performance
    common_nodes = len(set(D1).intersection(D2))
    return (len(D1) + len(D2) + common_nodes) / len(g.nodes())

def is_dominant_set(g, d):
    d_set = set(d)
    uncovered_nodes = set(g.nodes) - d_set
    for node in uncovered_nodes:
        if not any(neighbor in d_set for neighbor in g.neighbors(node)):
            return False
    return True

def calculate_D1_greed(node, g):
    D1_test = []
    g_temp = g.copy()

    # Greedy algorithm optimized with set removal
    while g_temp.nodes:
        D1_test.append(node)
        neighbors_to_remove = list(g_temp.neighbors(node)) + [node]
        g_temp.remove_nodes_from(neighbors_to_remove)
        if g_temp.nodes:
            node, _ = max(g_temp.degree, key=lambda x: x[1])
    return D1_test

def calculate_D2_greed(node, g, D1):
    D2_test = [node]
    g_temp = g.copy()
    g_temp.remove_nodes_from(list(g_temp.neighbors(node)) + [node])

    while g_temp:
        nodes_excluding_D1 = [n for n in g_temp.nodes if n not in D1]
        if nodes_excluding_D1:
            max_node = max(nodes_excluding_D1, key=lambda n: g_temp.degree(n))
        else:
            max_node, _ = max(g_temp.degree, key=lambda x: x[1])

        D2_test.append(max_node)
        g_temp.remove_nodes_from(list(g_temp.neighbors(max_node)) + [max_node])
    return D2_test

def find_longest_path(graph):
    def dfs(node, visited, path):
        visited.add(node)
        path.append(node)
        longest = list(path)  # Shallow copy for current longest path

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                new_path = dfs(neighbor, visited, path)
                if len(new_path) > len(longest):
                    longest = new_path

        path.pop()
        visited.remove(node)
        return longest

    longest_path = []
    for node in graph:
        path = dfs(node, set(), [])
        if len(path) > len(longest_path):
            longest_path = path

    return longest_path

def dominant(g):
    if len(g.nodes()) == len(g.edges()):
        longest_path = find_longest_path(g)
        D1 = [longest_path[i] for i in range(0, len(longest_path), 3)]
        D2 = [longest_path[i] for i in range(1, len(longest_path), 3)]
        if longest_path[-1] not in D2:
            D2.append(longest_path[-1])
        if is_dominant_set(g, D1) and is_dominant_set(g, D2):
            return [D1, D2]

    D1_trials = [calculate_D1_greed(node, g) for node in sorted(nx.degree_centrality(g).keys(), key=lambda n: g.degree(n), reverse=True)[:100]]
    D1 = min(D1_trials, key=len)

    g_temp = g.copy()
    g_temp.remove_nodes_from(D1)
    best_nodes = sorted(nx.degree_centrality(g_temp).items(), key=lambda x: x[1], reverse=True)[:25]
    D2_trials = [calculate_D2_greed(node, g, D1) for node, _ in best_nodes]

    D2 = min(D2_trials, key=lambda trial: calculate_score(D1, trial, g))
    print("D1 test: ", is_dominant_set(g, D1))
    print("D1 test: ", is_dominant_set(g, D2))
    return [D1, D2]

#########################################
#### Ne pas modifier le code suivant ####
#########################################


def load_graph(name):
    with open(name, "r") as f:
        state = 0
        G = None
        for l in f:
            if state == 0:  # Header nb of nodes
                state = 1
            elif state == 1:  # Nb of nodes
                nodes = int(l)
                state = 2
            elif state == 2:  # Header position
                i = 0
                state = 3
            elif state == 3:  # Position
                i += 1
                if i >= nodes:
                    state = 4
            elif state == 4:  # Header node weight
                i = 0
                state = 5
                G = nx.Graph()
            elif state == 5:  # Node weight
                G.add_node(i, weight=int(l))
                i += 1
                if i >= nodes:
                    state = 6
            elif state == 6:  # Header edge
                i = 0
                state = 7
            elif state == 7:
                if i > nodes:
                    pass
                else:
                    edges = l.strip().split(" ")
                    for j, w in enumerate(edges):
                        w = int(w)
                        if w == 1 and (not i == j):
                            G.add_edge(i, j)
                    i += 1

        return G


#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__ == "__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])

    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
        print(input_dir, "doesn't exist")
        exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
        print(input_dir, "doesn't exist")
        exit()

        # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    for graph_filename in sorted(os.listdir(input_dir)):
        # importer le graphe
        g = load_graph(os.path.join(input_dir, graph_filename))

        # calcul du dominant
        d1, d2 = dominant(g)
        D1 = sorted(d1, key=lambda x: int(x))
        D2 = sorted(d2, key=lambda x: int(x))

        # ajout au rapport
        output_file.write(graph_filename)
        for node in D1:
            output_file.write(' {}'.format(node))
        output_file.write('-')
        for node in D2:
            output_file.write(' {}'.format(node))
        output_file.write('\n')

    output_file.close()
