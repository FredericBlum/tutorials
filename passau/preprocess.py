"""
Query Lexibank data for six different language families, compute cognates,
and create individual SQLite files for further processing.
"""
# Load packages
import csv
import sqlite3
from tabulate import tabulate
from lingpy import Wordlist, LexStat, Alignments
from lexibase.lexibase import LexiBase

# load files
query = 'query.sql'

# Load sqlite
db = sqlite3.connect('cldf-resources/lexibank-analysed/lexibank2.sqlite3')
cursor = db.cursor()

with open(query, encoding='utf8') as f:
    query = f.read()

# Execute query
cursor.execute(query)
table = cursor.fetchall()
header = ['doculect', 'latitude', 'longitude', 'glottocode', 'family', 'concept', 'form', 'tokens']

# Print 10 rows to see that the results are good
print(tabulate(
    table[:10],
    tablefmt='pipe',
    headers=header
))

# Write results to tsv
with open('data.tsv', 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(header)
    writer.writerows(table)

# Load as lingpy:Wordlist()
wl = Wordlist('data.tsv')

# compute cognates and alignments
lex = LexStat(wl)
lex.get_scorer(runs=10000)
lex.cluster(threshold=0.55, method='lexstat', cluster_method='infomap', ref='cogid')

# Align data
alms = Alignments(lex, ref='cogid')
alms.align()
alms.add_entries('morphemes', 'tokens', lambda x: '')

# Output data
D = {0: ['doculect', 'family', 'value', 'form', 'concept', 'tokens', 'cogid', 'morphemes', 'alignment', 'note']}

checkup = []
for idx in alms:
    entry = [alms[idx, 'doculect'], alms[idx, 'concept'], alms[idx, 'form']]
    # Remove duplicates
    if entry not in checkup:
        D[idx] = [alms[idx, h] for h in D[0]]
        checkup.append(entry)

wl = Wordlist(D)
# lex.output('tsv', filename="bosavi", ignore="all")

# Create sqlite
lex = LexiBase(D, dbase='data/calc.sqlite3')
lex.create('calc')
