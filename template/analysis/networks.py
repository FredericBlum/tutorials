"""
This material is based on the LingPy tutorial of Mattis List (@LinguList): <https://github.com/lingpy/lingpy-tutorial/tree/v1.1>.
"""

import io
from lingpy import Wordlist
from lingpy import Tree
from lingpy.convert.strings import matrix2dst

# Load data
wl = Wordlist('example.tsv')

# Create distances
dst = matrix2dst(wl.get_distances(ref='cogid', mode='swadesh'), wl.taxa)

# Write distances to file
with io.open('example_distances.dst', 'w', encoding='utf8') as fp:
    fp.write(dst)

# print distances
print(dst)

# Create tree based on neighbor-joining algorithm
tree = Tree(wl.get_tree(ref='cogid', tree_calc='upgma', force=True))
print(tree.asciiArt())
