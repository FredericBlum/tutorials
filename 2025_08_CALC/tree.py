"""
Compute a simple tree.
"""
from lingpy import Wordlist

lex = Wordlist('data/calc')

lex.calculate('tree', ref='cogid')

print(lex.tree.asciiArt())
