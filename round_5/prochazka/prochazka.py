def main(input_file, output_file):
    with open(input_file, "r") as f:
        content = f.read().split("\n")

    i = 1
    output = []
    while i < len(content):
        [nodes_count, edges_count] = [int(num) for num in content[i].split(" ")]
        i += 1
        g = Graph(nodes_count)
        for edge in content[i:i+edges_count]:
            [start_node, target_node] = [int(num) for num in edge.split(" ")]
            g.add_edge(start_node, target_node)
        i += edges_count

        edges_to_add = g.fix_circuit()
        if not edges_to_add:
            output.append("Ano.")
        else:
            edges_to_add_string = "\n".join([f"{edge[0]} {edge[1]}" for edge in edges_to_add])
            output.extend(["Ne.", str(len(edges_to_add)), edges_to_add_string])
        
    with open(output_file, "w", newline="") as f:
        f.write("\n".join(output))

class Graph:
    def __init__(self, nodes_count):
        self.nodes = range(nodes_count)
        self.edges = {node: [] for node in range(nodes_count)}

    def add_edge(self, start_node, target_node):
        self.edges[start_node].append(target_node)
        self.edges[target_node].append(start_node)

    def fix_circuit(self):
        odd_degree_nodes = [node for node in self.nodes if len(self.edges[node]) % 2 != 0]
        edges = []
        for i in range(0, len(odd_degree_nodes), 2):
            edges.append((odd_degree_nodes[i], odd_degree_nodes[i+1]))
        return edges

main("./round_5/prochazka/io_example/input.txt", "./round_5/prochazka/output.txt")