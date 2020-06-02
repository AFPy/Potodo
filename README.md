# Potodo
Potodo, a (almost) flawless TODO/progress listing CLI tool for po files.

## Installation

```bash
pip install potodo
```

## Usage

```
usage: potodo [-h] [-p PATH] [-a X] [-b X] [-f] [-o] [-n] [-c] [-j]
              [--version]

Sequence and prettify the po files left to translate.

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  execute Potodo in PATH
  -e EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        exclude folders
  -a X, --above X       list all TODOs above given X% completion
  -b X, --below X       list all TODOs below given X% completion
  -f, --fuzzy           print only files marked as fuzzys
  -o, --offline         don't perform any fetching to GitHub/online
  -n, --no-reserved     don't print info about reserved files
  -c, --counts          render list with the count of remaining entries
                        (translate or review) rather than percentage done
  -j, --json            format output as JSON.
  --version             show program's version number and exit
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
