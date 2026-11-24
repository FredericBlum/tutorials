# Computer-Assisted Language Comparison

## Overview

This is a README-file with all the important information that you need for following the tutorial

### Software requirements

Please install the following software:

- Python v3.15 (<https://www.python.org/downloads/>)
- Git (<https://git-scm.com/downloads>)
- VS Codium (<https://vscodium.com/#install>) + Rainbow CSV Extension

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
