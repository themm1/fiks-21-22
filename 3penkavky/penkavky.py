import math
from pprint import pprint
import Levenshtein
import networkx as nx
import matplotlib.pyplot as plt

class Main:
    bits_nucleobase = {
        "00": "A",
        "01": "C",
        "10": "G",
        "11": "T"
    }
    def __init__(self, input_file, output_file):
        with open(input_file, "rb") as f:
            self.content = f.read()

        tasks_count, index = self.bytes_int(0)
        for _ in range(tasks_count):
            output = []
            dnas = []
            dnas_count, index = self.bytes_int(index)
            max_diff, index = self.bytes_int(index)

            for _ in range(dnas_count):
                genomes_count, index = self.bytes_int(index)
                dna_bits, index = self.bytes_bits(index, genomes_count)
                dna = "".join(self.bits_genomes(dna_bits))
                dnas.append(dna)

            g = Graph(dnas, max_diff)
            triplets = g.get_triplets()
            output.append(str(len(triplets)))
            for triplet in triplets:
                output.append(" ".join(triplet))
            # plt.show()
            # pprint(triplets)

            with open(output_file, "a", encoding="utf-8", newline="") as f:
                f.writelines("\n".join(output) + "\n")

    def bits_genomes(self, dna):
        genomes = []
        for i in range(0, len(dna), 2):
            genomes.append(self.bits_nucleobase[dna[i:i+2]])
        return genomes
            
    def bytes_bits(self, index, genomes_count):
        if genomes_count == 0:
            return "", index + 1
        bits = []
        for i, byte in enumerate(self.content[index:index+math.ceil(genomes_count/4)]):
            if genomes_count - len(bits)/2 > 4:
                bits.extend(format(byte, "08b"))
            else:
                bits.extend(format(byte, "08b")[:2*(genomes_count - int(len(bits)/2))])
                return "".join(bits), index + i + 2
                

    def bytes_int(self, index):
        num = ""
        new_index = index
        for byte in self.content[index:]:
            char = chr(byte)
            new_index += 1
            if char != " " and char != "\n" and char != "\r":
                num += char
            else:
                return int(num), new_index
        return int(num), new_index + 1

class Graph:
    def __init__(self, DNAs, max_diff):
        self.graph = {node: set() for node in range(len(DNAs))}
        for i, dna in enumerate(DNAs):
            for j, dna2 in enumerate(DNAs):
                if i != j:
                    if Levenshtein.distance(dna, dna2) <= max_diff:
                        self.graph[i].add(j)
        # self.create_networkx_graph()

    def get_triplets(self):
        visited = {node: False for node in self.graph.keys()}
        triplets = []
        for node1 in self.graph.keys():
            for node2 in self.graph[node1]:
                for node3 in self.graph[node2]:
                    if node1 not in self.graph[node3] and node1 != node3:
                        triplets.append([str(node1), str(node2), str(node3)])
            visited[node1] = True
        for triplet in triplets:
            reversed_triplet = list(reversed(triplet))
            if reversed_triplet in triplets:
                triplets.remove(reversed_triplet)
        return triplets

    def create_networkx_graph(self):
        G = nx.Graph()
        for node, connected_nodes in self.graph.items():
            for connected_node in connected_nodes:
                G.add_edge(node, connected_node)
        nx.draw(G, with_labels=True)


# my implementation of Levenshtein Distance, which is very slow so for actual
# program I am using special library so all tasks are done much more faster
class LevenshteinDist:
    def __init__(self, str1, str2):
        self.str1 = str1
        self.str2 = str2
        self.table = [[None] * (len(self.str2)+1) for _ in range(len(self.str1)+1)]

        self.table[0][0] = 0
        for i in range(1, len(self.str2)+1):
            self.table[0][i] = i
        for i in range(1, len(self.str1)+1):
            self.table[i][0] = i
        self.fill_table()
        self.edit_dist = self.table[-1][-1]

    def fill_table(self):
        for i in range(1, len(self.str1)+1):
            for j in range(1, len(self.str2)+1):
                edit_dist = self.get_edit_dist(i, j)
                self.table[i][j] = edit_dist

    def get_edit_dist(self, row, column):
        cost = 0 if self.str1[row-1] == self.str2[column-1] else 1
        neighbors = [
            self.table[row-1][column] + 1,
            self.table[row-1][column-1] + cost,
            self.table[row][column-1] + 1
        ]
        return min(neighbors)
        

if __name__ == "__main__":
    Main("./round_3/penkavky/io_example/input.txt", "./round_3/penkavky/output.txt")
