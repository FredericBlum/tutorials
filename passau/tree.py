"""
Compute a simple tree.
"""
from lingpy import Wordlist

lex = Wordlist('misumalpam.tsv')

lex.calculate('tree', ref='cogid')

print(lex.tree.asciiArt())