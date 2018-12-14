# Potodo
Potodo, a Flawless TODO/progress listing CLI tool for po files

## Installation

```bash
pip install potodo
```

## Usage

```bash
usage: potodo [-h] [-l] [-f] [-a ABOVE | -b BELOW] path repo

List and prettify the po files left to translate

positional arguments:
  path                  Execute Potodo in the given path
  repo                  Repo in the form of ORG/REPO to display if translation
                        is reserved in issues

optional arguments:
  -h, --help            show this help message and exit
  -l, --matching-files  Suppress normal output; instead print the name of each
                        matching po file from which output would normally have
                        been printed.
  -f, --fuzzy           Will only print files marked as fuzzys
  -a ABOVE, --above ABOVE
                        Will list all TODOs ABOVE given INT% completion
  -b BELOW, --below BELOW
                        Will list all TODOs BELOW given INT% completion
```
