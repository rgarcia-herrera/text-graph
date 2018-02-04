from pattern.en import parsetree
import numpy as np

s = open('data/prueba.txt').read()

tree = parsetree(s, relations=True, lemmata=True)

window = int(np.mean([len(sentence.words) for sentence in tree]) * 3)

distances = {}


for n in range(len(tree.words)):
    w = tree.words[n]
    if w.type == 'NNP':
        ego = w.string
        if ego not in distances:
            distances[ego] = {}

        for m in range(n + 1, n + window):
            if m < len(tree.words) and tree.words[m].type == 'NNP':
                alter = tree.words[m].string

                if alter != ego:
                    if alter not in distances[ego]:
                        distances[ego][alter] = []

                    distances[ego][alter].append(m - n)


for k in distances:
    for m in distances[k]:
        if len(distances[k][m]) > 4:
            print k, m, distances[k][m]
