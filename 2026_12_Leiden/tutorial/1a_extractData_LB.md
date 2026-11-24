# Extract Data from CLDF datasets

For a quick access and preprocessing of CLDF data, we recommend the usage of SQLite.

## Extract data from Lexibank

### Necessary packages

We will be working in the command line and make use of some Python packages, without writing scripts ourselfs (for the moment). I assumme you have followed the general README.md of this repository and have Python and Git installed to your computer.

First, you clone LexiBank, and create a sqlite database of this:

```shell
git clone https://github.com/lexibank/lexibank-analysed data/lexibank-analysed
git clone https://github.com/concepticon/concepticon-data data/concepticon --branch v3.4.0

cldf createdb data/lexibank-analysed/cldf/wordlist-metadata.json data/lexibank.sqlite3
```

Using SQLite queries, we can now retrieve, for example, data from:

a) specific language families
b) from a specific macro-area
c) for a specific conceptlist

```sql
-- Choose rows you want to extract
SELECT
    l.cldf_name,
    l.cldf_latitude,
    l.cldf_longitude,
    l.cldf_glottocode,
    l.family,
    p.concepticon_gloss,
    f.cldf_form,
    f.cldf_segments
-- Choose tables from which to extract
FROM
    formtable AS f,
    languagetable AS l,
    parametertable AS p
-- Set conditions and merger
WHERE
    -- Only the 100 concepts from the Leipzig-Jakarta list
    -- p.core_concept like '%Tadmor-2009-100%'
    --    AND
    f.cldf_parameterReference = p.cldf_id
        AND
    f.cldf_languageReference = l.cldf_id
        AND
    l.cldf_macroarea is 'South America'
;
```

We can implement this directly in Python:

```python
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

# Load sqlite
db = sqlite3.connect('data/lexibank.sqlite3')
cursor = db.cursor()

conc = Concepticon('data/concepticon/')

concepts = []
# Read in concept list
clist = conc.conceptlists['Bowern-2021-342b'].concepts
concepts = [clist[item].concepticon_gloss for item in clist]

# Execute query
cursor.execute(query)
table = cursor.fetchall()

# columns that we retrieve
output_data = [['glottocode', 'doculect', 'family',  'concept', 'segments']]
languages = defaultdict(list)

for item in table:
    # check if concept is in concept list
    if item[3] in concepts:
        # print(item)
        output_data.append(item)
        if item[3] not in languages[item]:
            languages[item].append(item[3])

# Load as wordlist
with open('output_data.tsv', 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(output_data)

for lang in languages:
    missing = ['Language', 'Concept', 'Form']
    for conc in concepts:
        if conc not in languages[lang]:
            missing.append([lang, conc, ''])
    
    path = 'data/missing_' + lang + '.tsv'
    with open(path, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(missing)
```
