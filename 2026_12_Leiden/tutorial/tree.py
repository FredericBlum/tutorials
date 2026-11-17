"""
Compute a simple tree.
"""
from lingpy import Wordlist

lex = Wordlist('data/data_annotated.tsv')

lex.calculate('tree', ref='cogid')

print(lex.tree.asciiArt())
