# Potodo
Potodo, a (almost) flawless TODO/progress listing CLI tool for po files

## Installation

```bash
pip install potodo
```

## Usage

```
usage: potodo [-h] [-p PATH] [-l] [-f] [-o] [-n] [-a ABOVE] [-b BELOW]

List and prettify the po files left to translate

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Execute Potodo in the given path
  -l, --matching-files  Suppress normal output; instead print the name of each matching po file from which output would normally have been printed.
  -f, --fuzzy           Will only print files marked as fuzzys
  -o, --offline         Will not do any fetch to GitHub/online if given
  -n, --no-reserved     Will not print the info about reserved files
  -j, --json            Will produce JSON-formatted output
  -a ABOVE, --above ABOVE
                        Will list all TODOs ABOVE given INT% completion
  -b BELOW, --below BELOW
                        Will list all TODOs BELOW given INT% completion
```

## Contributing

You can run the tests using `tox` locally like:

    tox -p auto

before commiting.

A pre-commit hook like:
```sh
cat <<EOF > .git/hooks/pre-commit
#!/bin/sh
exec tox -s -p all
EOF
```
may help.