import networkx as nx
import argparse

description = """Create a network pickle from input text."""

parser = argparse.ArgumentParser(
    description=description)

parser.add_argument('gpickle',
                    type=argparse.FileType('r'),
                    help='input pickled networkx graph')

parser.add_argument('edgelist',
                    type=argparse.FileType('w'),
                    help='edgelist output')


args = parser.parse_args()

g = nx.read_gpickle(args.gpickle)

nx.write_edgelist(g, args.edgelist,
                  delimiter='\t', data=['w'])
