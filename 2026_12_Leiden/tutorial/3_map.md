# Map polygons in QGIS

This follows a published tutorial:
> Blum Frederic (2026): “Visualizing Language Polygons with (Q)GIS” in Computer-Assisted Language Comparison in Practice, 9.1: 41-53 [first published on 04/05/2026], URL: https://calc.hypotheses.org/9287, DOI: 10.15475/calcip.2026.1.5.

## Preparations

```shell
pip install pycldf
pip install csvkit
pip install cldfgeojson
pip install cldfbench

git clone https://github.com/Glottography/asher2007world
```

Additionally, we clone Glottolog:

```shell
# Clone dataset
git clone https://github.com/glottolog/glottolog-cldf

# Create SQLite database
cldf createdb glottolog-cldf/cldf/cldf-metadata.json glottolog.sqlite3

# Open database
sqlite3 data/glottolog.sqlite3
```

```sql
.mode csv
.headers on
.output data/glottocodes.csv

SELECT
    l.cldf_id AS Glottocode,
    l.Family_ID
FROM
    LanguageTable AS l
WHERE
    -- List of language-family glottocodes
    l.Family_ID IN ('pano1259', 'araw1282', 'yano1268')
;

.output stdout;
.exit
```

```shell
csvcut -c Glottocode data/glottocodes.csv | \
csvformat -E | \
cldfbench geojson.geojson --no-glottolog data/asher2007world/cldf/traditional - \
> data/amazon_polygons.geojson
```


