# Preparation for running CLDF/Lexibank/Edictor on Windows

## Installing Python

In case you haven't installed python on your computer, please download and install python. You can then open something that is probably called 'Windows PowerShell' and test whether the code `python --version` works. If this is not the case, you probably need to add python to your `PATH`, which means adding python to the system so that it recognizes the `python` command. You will probably need to restart your computer afterwards. Here is a good tutorial on how to do this: <https://realpython.com/add-python-to-path/>

## Installing git

Similar to having python ready, you need to have git installed. Git is a versioned data management system which is often used to share and publish code and data. The most common platform to use git is GitHub, a Microsoft owned project where most of the code from modern programming is stored. We recommend to interact with GitHub using the command line (another word for 'shell'), and many of our scripts make use of this functionality as well.

Here you can find all the stuff that is necessary to install git: <https://git-scm.com/download/win>

Similar to the python installation, you will need to add Git to the `PATH` and restart your PC.

## Activate long file name

We will have a local clone of Glottolog on our PCs, and Glottolog makes extensive use of subfolders, resisting in veeery long paths to files. No problem for MacOS and Linux, but on Windows you will have to switch this on explicitly so that it does work.

We need to proceed in two steps. First, set the system configuration so that it allows long filenames. Here is a good visual tutorial on how this is done: <https://www.howtogeek.com/266621/how-to-make-windows-10-accept-file-paths-over-260-characters/>

In a second step, you need to run the following command from your Windows PowerShell:
`git config --global core.longpaths true`

## Reproducting the dictionary extraction

You are now ready to reproduce the workflow of our paper. We have shared all the code on GitHub, and sent you an invitite to the repository. If you don't have one yet, you will need to create an account on GitHUb. If you have problems accessing the repository, please contact me.

Once you have access, you can _clone_ the repository to your PC using the PowerShell:

`git clone https://github.com/FredericBlum/ExtractingWordlistsFromDictionaries`

You can then open a PowerShell in that folder, and run all the code as indicated in the README.md of the repository. For some commands, you might need to adapt to some Windows-specific practices. Changing directories, for example, might need the full path to the folder (e.g. `cd folder/to/dictionary/vonprincedaakaka`) instead of the relative path (e.g. `cd vonprincedaakaka`). But those are things that you just need to try out with the help of a search engine.

## Editors combining text editing and terminals

A common tool to use PowerShells/Terminals are editors such as VisualStudio Code or PyCharm, which combine in a single layout the functionality of a TextEditor, the handling of terminals, and the handling of folder structures. My personal recommendation is VS Code, since it is more modular than PyCharm, and offers all necessary tools without making too many assumptions about stuff.

## General comment about encodings

While MacOS and Linux are Unicode UTF-8 based, Windows often uses different encodings which cannot be read by other operating systems. All CLDF sets are ALWAYS written in Unicode, and most programs do that. There is one very important exception: Microsoft Word. You should never ever use Microsoft Word in a CLDF context, since those files will not be interoperable with other users. Instead, you can use text editors such as VS Code, or, if you want to have spreadsheets, LibreOffice. LibreOffice will ask you explictily about the file encoding and has UTF-8 as default.
