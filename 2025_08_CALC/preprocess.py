"""
Query Lexibank data for different language families, compute cognates,
and create a SQLite file for further processing.
"""
# Load packages
import csv
import sqlite3
from collections import defaultdict
from tabulate import tabulate
from lingpy import Wordlist, LexStat, Alignments
from lexibase.lexibase import LexiBase
from pyconcepticon import Concepticon

# load files
query = 'query_sa.sql'

# Load sqlite
db = sqlite3.connect('data/lexibank-analysed/lexibank.sqlite')
cursor = db.cursor()

conc = Concepticon('data/concepticon/')

concepts = []
clist = conc.conceptlists['Bowern-2021-207a'].concepts
for item in clist:
    concepts.append(clist[item].concepticon_gloss)
    # print(clist[item].concepticon_id, clist[item].concepticon_gloss)


with open(query, encoding='utf8') as f:
    query = f.read()

# Execute query
cursor.execute(query)
table = cursor.fetchall()
header = ['doculect', 'latitude', 'longitude', 'glottocode', 'family', 'concept', 'form', 'tokens']

# Print 10 rows to see that the results are good
print(tabulate(
    table,
    tablefmt='pipe',
    headers=header
))

output_data = []
for item in table:
    if item[5] in concepts:
        output_data.append(item)

# Write results to tsv
with open('data.tsv', 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(header)
    writer.writerows(table)

# Load as lingpy:Wordlist()
wl = Wordlist('data.tsv')

# # compute cognates and alignments
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
lex.output('tsv', filename="data_annotated", ignore="all")

# Create sqlite
lex = LexiBase(D, dbase='data/calc.sqlite3')
lex.create('calc')
