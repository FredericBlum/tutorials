# Computer-Assisted Language Comparison

## Overview

This is a readme-file with all the important information that you need.

## Code for preprocessing

This code is for documentary purposes

```shell
# with csvkit installed
csvsql --query "SELECT Name,Family,Dataset,Concepts FROM languages WHERE Macroarea = 'South America' AND Concepts > 100 AND Selexion == 1 ORDER BY Family, Name" --table languages.csv
```

```shell
git clone https://github.com/lexibank/lexibank-analysed data/lexibank-analysed
```


paez + barbacoan
chocoan + Yaruro
guahibo + puinave
naduhup
Misumalpan
Cochimi-Yuman
Chumashan
Muskogean + natchez + Atakapa
Miwok-Costanoan
Chicham
Lengua-Mascoy
Saliban

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


Schedule


Input 1: 30min
Group work 1: 45min

-- 15min break --

Input 2: 1h

-- lunch --

Group work 2: 2h

Input: 2x45min

Group work: 2x 90min

    10-10:45 Input: How to build a LexiBank dataset
    10:45-12:15 Group Work 1: Building a LexiBank dataset
    Lunch break
    14:00-14:45 Input: Cognates and sound correspondences in EDICTOR
    14:45-16:15 Group Work 2: Annotating a LexiBank dataset
