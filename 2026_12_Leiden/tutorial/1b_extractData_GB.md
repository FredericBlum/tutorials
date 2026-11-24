# Extract Data from CLDF datasets

For a quick access and preprocessing of CLDF data, we recommend the usage of SQLite.

## Extract data from Grambank

### Necessary packages

We will be working in the command line and make use of some Python packages, without writing scripts ourselfs (for the moment). I assumme you have followed the general README.md of this repository and have Python and Git installed to your computer.

First, you clone Grambank, and create a sqlite database of this:

```shell
git clone https://github.com/grambank/grambank data/grambank --depth 1 --branch v1.0.3

cldf createdb data/grambank/cldf/StructureDataset-metadata.json data/grambank.sqlite3
```

Using SQLite queries, we can now retrieve, for example, data from:

a) specific language families
b) from a specific macro-area
c) for a specific conceptlist

```sql
SELECT
  l.cldf_id,
  p.cldf_name,
  f.cldf_value,
  l.Family_name
FROM
  valuetable as f,
  languagetable as l,
  parametertable as p
ON
  f.cldf_languagereference = l.cldf_id
WHERE
  f.cldf_parameterReference = p.cldf_id
;
```

We can also use existing code from one of my project to directly loac this into Python:

```python
from ala.data import convert_data, load_data, concept2vec, feature2vec, get_db
from ala.utils import write_table, main

gb, families = load_data('grambank', 1, False)
gb_conv = feature2vec(get_db('data/grambank.sqlite3'))
data = convert_data(gb, families, gb_conv, load='grambank')
```

The output is a Python dictionary of structure `'hwan1238': ['Koreanic', 89, [vector] }`

To analyze the data, we can turn to `2_umap.py`.
