# Computer-Assisted Language Comparison

## Overview

This is a README-file with all the important information that you need for following the tutorial

### Software requirements

Please install the following software:

- Python3.13 (<https://www.python.org/downloads/>)
- Git (<https://git-scm.com/downloads>)
- VS Codium (<https://vscodium.com/#install>) + Rainbow CSV Extension

### Recommended readings

These are some articles that introduce some of the principles and software used.

> Blum, F., Barrientos, C., Zariquiey, R. et al. A comparative wordlist for investigating distant relations among languages in Lowland South America. Sci Data 11, 92 (2024). https://doi.org/10.1038/s41597-024-02928-7

> List, J.-M., & van Dam, K. (2024). Invited paper: Computer-Assisted Language Comparison with EDICTOR 3. In N. Tahmasebi, S. Montariol, A. Kutuzov, D. Alfter, F. Periti, P. Cassotti, & N. Huebscher (Eds.), Proceedings of the 5th Workshop on Computational Approaches to Historical Language Change (pp. 1–11). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.lchange-1.1

## Preparing your computer

### All platforms: software installation

1. Install Python (<https://www.python.org/downloads/>) and git (<https://git-scm.com/downloads>)
2. Install VS Codium (<https://vscodium.com/#install>)
    - Watch the first 2min of the following tutorial for a short introduction to VS Codium (<https://www.youtube.com/watch?v=B-s71n0dHUk>). The rest of the video is not relevant for us.
3. Open VS Codium and select the file explorer (top left corner)
4. Select 'Open Folder' and create 'lexibank' directory
5. Install Rainbow CSV in VSCodium (Extensions --> Rainbow CSV)

The 'lexibank' folder will be the folder where all the files we use will be stored, and where the terminal is run from within VS Codium.

### MacOS and Linux

Run the following commands in your terminal from within VSC and the 'lexibank' directory. To open the terminal, either drag the bottom bar of VS Codium upwards, or select 'Terminal' > 'New Terminal' from the menu header.

```shell
cd tutorial
python3 -m venv venv/lexibank
source venv/lexibank/bin/activate # every time you open the terminal!
```

Install the necessary python packages. You might need to add `python3 -m` before `pip` on some OS.

```shell
pip install pylexibank
pip install "edictor[lingpy]"
```

Now clone the repository:

```shell
git clone https://github.com/FredericBlum/tutorials
```

### Setting up Windows

Run the following command in your powershell (open as 'admin') so you are allowed to run scripts and packages:

```shell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -force  # (powershell admin)
```

Run the following commands in your terminal from within VSC and the 'lexibank' directory. To open the terminal, either drag the bottom bar of VS Codium upwards, or select 'Terminal' > 'New Terminal' from the menu header.

```shell
py -m pip install virtualenv
py -m venv .\venv\lexibank
.\venv\lexibank\Scripts\activate
pip install edictor[lingpy]
```

Every time you open your terminal, please activate the virtual environment:

```shell
.\venv\lexibank\Scripts\activate
```

## Tutorial

All material is provided within this GitHub repository. The folder `tutorial/` includes all the data and code.

Note: MacOS and Linux use `/` to annotate folder structure. If you use Windows, change all `/` into `\` when running the code.

### Set up the folder

First, clone the repository to your local PC.

```shell
git clone https://github.com/FredericBlum/tutorials
```

Then, change your directory into the cloned repository and switch into the `tutorial` folder. There, clone the `crossandean` dataset.

```shell
cd tutorials/tutorial
git clone https://github.com/lexibank/crossandean data/crossandean/
```

### Preparing individual datasets using an SQLite query

Download the sqlite3 database here to avoid running the code and put it in the 'tutorial' folder: <https://share.eva.mpg.de/index.php/s/63k5moKTfLgMLWx>

For the hands-on-session, you do no thave to run this, since I provide you the database. But this code has been used for creating it. First, we clone Lexibank and concepticon. Then, we run `createdb` from the `lexibase` package to create the database. In the end, we run the python script `preprocess.py` to run the cognate annotation.

```shell
git clone https://github.com/lexibank/lexibank-analysed data/lexibank-analysed
git clone https://github.com/concepticon/concepticon-data data/concepticon --branch v3.4.0

cldf createdb data/lexibank-analysed/cldf/wordlist-metadata.json data/lexibank-analysed/lexibank.sqlite3
```

Run the query that retrieves the data from lexibank and a first automated cognate detection process.

```shell
pip install igraph
python preprocess.py
```

## CALC in practice: CrossAndean data

Open VS Codium and the 'lexibank' folder you created. Here, open your terminal and run the codes as written below.

```shell
git clone https://github.com/FredericBlum/tutorials
```

### Preparing the `crossandean` dataset for illustratory purposes

```shell
git clone https://github.com/lexibank/crossandean data/crossandean
cd data/crossandean
```

```shell
edictor wordlist --sqlite --name=crossandean --addon="language_family:subgroup","cognacy:cogid","partial_cognacy:cogids","alignment:alignment"
```

Then, move the created database to the `data/` folder.

### Using Edictor

We now change to the `data` folder, where the databases are stored. Here, we open Edictor via the command line. It will open in your firefox browser, but only as visualization. You do not need internet, it runs locally.

```shell
cd data
edictor server
```

Under `User`, select the database you want to work on. By saving&downloading, you can store the data in a file called `calc`. All changes made will be stored to your local copy of the SQLite file.

## Outlook

### Build a tree

Using lingpy to print a tree to the command line. It uses as input the downloaded `calc` file from the cognate annotations you have made.

```shell
python tree.py
```

### Write nexus file

We can export the file to nexus, a format used for phylogenetic analysis. Again, it uses the downloaded `calc` file by default.

```shell
python -c "from lingpy import *; from lingpy.convert.strings import write_nexus; wl = Wordlist('calc'); write_nexus(wl, mode='beastwords', filename='calc.nex', ref='cogid')"
```

### Extract language metadata

```shell
csvcut -t -c family,doculect,latitude,longitude data/data.tsv | uniq > map/languages.tsv
```
