from pattern.en import parsetree
import numpy as np
import networkx as nx
import argparse

description = """Create a network pickle from input text."""

parser = argparse.ArgumentParser(
    description=description)

parser.add_argument('text',
                    type=argparse.FileType('r'),
                    help='input flat text file')

parser.add_argument('gpickle',
                    type=argparse.FileType('wb'),
                    help='')

args = parser.parse_args()

tree = parsetree(args.text.read(),
                 relations=True, lemmata=True)

window = int(np.mean([len(sentence.words) for sentence in tree]) * 3)

# create list of distances of co-ocurrences within window
distances = {}
for n in range(len(tree.words)):
    w = tree.words[n]
    if w.type == 'NNP':
        ego = w.string
        if ego not in distances:
            distances[ego] = {}
        # seek alters for ego
        for m in range(n + 1, n + window):
            if m < len(tree.words) and tree.words[m].type == 'NNP':
                alter = tree.words[m].string

                if alter != ego:
                    if alter not in distances[ego]:
                        distances[ego][alter] = []
                    # append distance from ego to alter
                    distances[ego][alter].append(m - n)


# remove pairs with few co-ocurrences
filtered = {}
for k in distances:
    for m in distances[k]:
        if len(distances[k][m]) > 4:
            filtered[(k, m)] = distances[k][m]

# will create an undirected graph, so a,b == b,a
flipped = {}
for pair in filtered:
    if pair not in flipped and (pair[1], pair[0]) not in flipped:
        # compute normalized proximity
        flipped[pair] = (window
                         - np.mean(filtered[pair]
                                   + filtered.get((pair[1], pair[0]),
                                                  []))) / window


# create graph

g = nx.Graph()

for pair in flipped:
    g.add_edge(*pair, w=flipped[pair])

nx.write_gpickle(g, args.gpickle)
