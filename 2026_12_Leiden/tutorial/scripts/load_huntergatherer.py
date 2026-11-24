import csv
import sqlite3
from collections import defaultdict
from pyconcepticon import Concepticon

query = """
SELECT
    l.cldf_glottocode,
    l.cldf_name,
    l.family,
    p.concepticon_gloss,
    f.cldf_segments
FROM
    formtable AS f,
    languagetable AS l,
    parametertable AS p
WHERE
    f.cldf_parameterReference = p.cldf_id
        AND
    f.cldf_languageReference = l.cldf_id
        AND
    l.cldf_macroarea = 'South America'
;
"""

# Read in concept list
concepts = []
conc = Concepticon('../data/concepticon/')
clist = conc.conceptlists['Bowern-2021-342b'].concepts
concepts = [clist[item].concepticon_gloss for item in clist]


# Load sqlite
db = sqlite3.connect('../data/lexibank.sqlite3').cursor()
db.execute(query)
table = db.fetchall()

# columns that we retrieve
output_data = [['glottocode', 'doculect', 'family',  'concept', 'segments']]
languages = defaultdict(list)

for item in table:
    # check if concept is in concept list
    if item[3] in concepts:
        # print(item)
        output_data.append(item)
        if item[3] not in languages[item[0]]:
            languages[item[0]].append(item[3])

# Load as wordlist
with open('huntergatherer_sa.tsv', 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(output_data)

for lang in languages:
    # print(lang)
    missing = [['Language', 'Concept', 'Form']]
    for conc in concepts:
        if conc not in languages[lang] and conc != '':
            missing.append([lang, conc, ''])
    
    path = 'missing/' + lang + '.tsv'
    with open(path, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(missing)
