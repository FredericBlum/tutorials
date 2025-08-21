# Computer-Assisted Language Comparison

## Overview

This is a readme-file with all the important information that you need.

## Code for preprocessing

This code is for documentary purposes

## Pre-processing

```shell
python3 -m venv venv/center
source venv/center/bin/activate
pip install pylexibank
pip install lexibase
```

```shell
# with csvkit installed
csvsql --query "SELECT Name,Family,Dataset,Concepts FROM languages WHERE Macroarea = 'South America' AND Concepts > 100 AND Selexion == 1 ORDER BY Family, Name" --table map/languages.csv
```

```shell
git clone https://github.com/lexibank/lexibank-analysed data/lexibank-analysed
git clone https://github.com/concepticon/concepticon-data data/concepticon --branch v3.4.0

cldf createdb data/lexibank-analysed/cldf/wordlist-metadata.json data/lexibank-analysed/lexibank.sqlite3
```

```shell
python preprocess.py
```

```shell
python tree.py
```

```shell
python -c "from lingpy import *; from lingpy.convert.strings import write_nexus; wl = Wordlist('calc'); write_nexus(wl, mode='beastwords', filename='calc.nex', ref='cogid')"
```

lencan
Chicham + cahuapanan

csvcut -t -c family,doculect,latitude,longitude data.tsv | uniq > languages.tsv




Software requirements

    PowerShell (https://learn.microsoft.com/powershell/, vermutlich vorinstalliert)
    Standard-Browser (am besten Firefox)
    Python3.13 (alles ab Python 3.9 geht aber eigentlich)
    Git (https://git-scm.com/downloads)
    Recommended: VS Codium (https://vscodium.com/#install) + Rainbow CSV Extension


Reading list

    Blum, F., Barrientos, C., Zariquiey, R. et al. A comparative wordlist for investigating distant relations among languages in Lowland South America. Sci Data 11, 92 (2024). https://doi.org/10.1038/s41597-024-02928-7
    Johann-Mattis List and Kellen van Dam. 2024. Invited paper: Computer-Assisted Language Comparison with EDICTOR 3. In Proceedings of the 5th Workshop on Computational Approaches to Historical Language Change, pages 1–11, Bangkok, Thailand. Association for Computational Linguistics. https://aclanthology.org/2024.lchange-1.1/.

Beide sind OpenSource.


9:00 - 10:00: How to build a LexiBank dataset - the role of standardized data
10:00 - 10:30: LexiBank in practice
    10:30 - 11:00: Break
11:00 - 12:00: CALC with EDICTOR (Input)
12:00 - 12:45: CALC with EDICTOR (practice I)
    12:45 - 14:00: Lunch
13:30 - 15:00: CALC with EDICTOR (practice II)
    15:00 - 15:30: Break
15:30 - 16:00: Outlook // short presentations
16:00 - 17:30: Group project
