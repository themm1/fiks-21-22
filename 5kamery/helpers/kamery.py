import math
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint


class Graph:
    def __init__(self, n):
        self.nodes = range(1, n+1)
        self.edges = {node: [] for node in self.nodes}
        self.frequencies1 = {}
        self.frequencies2 = {}
        self.G = nx.Graph()
        self.populate_edges()

    # connect cameras with cabels
    def populate_edges(self):
        for node in self.nodes:
            divisors = self.get_divisors(node)
            for divisor in divisors:
                if divisor != node:
                    self.edges[divisor].append(node)

    @staticmethod
    def get_divisors(n):
        divisors = []
        for i in range(1, int(math.sqrt(n) + 1)):
            if n % i == 0:
                divisors.append(i)
                if n / i != i:
                    divisors.append(n / i)
        return divisors

    # task part 1
    def set_frequencies(self):
        for node in self.nodes:
            factorization = self.prime_factorization(node)
            self.frequencies1[node] = factorization

    # task part 1
    @staticmethod
    def prime_factorization(n):
        i = 2
        factorization = []
        while i < math.sqrt(n) + 1:
            if n % i == 0:
                factorization.append(i)
                n /= i
            else:
                i += 1
        if n != 1:
            factorization.append(n)
        return len(factorization)

    # task part 2
    def set_frequencies2(self):
        nodes = [1]
        edges = []
        seconds = 0
        self.frequencies2[1] = seconds
        while nodes:
            self.plot(special_nodes=nodes, special_edges=edges)
            seconds += 1
            nodes, edges = self.simulate_round(nodes, seconds)
        return seconds

    # task part 2
    def simulate_round(self, nodes_with_word, seconds):
        new_nodes = []
        edges = []
        for node in nodes_with_word:
            for connected_node in self.edges[node]:
                new_nodes.append(connected_node)
                self.frequencies2[connected_node] = seconds
                edges.append((node, connected_node))
        return new_nodes, edges

    # plot graph using networkx
    def plot(self, special_nodes, special_edges):
        for node, connected_nodes in self.edges.items():
            for node2 in connected_nodes:
                if (node, node2) in special_edges:
                    self.G.add_edge(node, node2, color="#DC143F", weight=3)
                else:
                    self.G.add_edge(node, node2, color="#1E90FF", weight=1)

        node_color = self.node_colors(special_nodes)
        edge_color, weights = self.edge_attrs()
        pos = nx.circular_layout(self.G)

        nx.draw(self.G, pos, node_color=node_color,
            edge_color=edge_color, width=list(weights),
            arrows=True, with_labels=True)
        plt.show()

    # create list with node colors from nx graph
    def node_colors(self, special_nodes):
        node_colors = []
        for node in self.G:
            if node in special_nodes:
                node_colors.append("#DC143C")
            else:
                node_colors.append("#1E90FF")
        return node_colors

    # get edge attrs from nx graph
    def edge_attrs(self):
        edge_colors = nx.get_edge_attributes(self.G, "color").values()
        edge_weights = nx.get_edge_attributes(self.G, "weight").values()
        return edge_colors, edge_weights


if __name__ == "__main__":
    g = Graph(15)
    g.set_frequencies()
    rounds = g.set_frequencies2()

    print(rounds)
    print(g.frequencies1 == g.frequencies2)