# Potodo
![Build status](https://github.com/AFPy/Potodo/workflows/Tests/badge.svg)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
![PyPI](https://img.shields.io/pypi/v/potodo)

Potodo, a (almost) flawless TODO/progress listing CLI tool for po files.

### Potodo is part of poutils!

[Poutils](https://pypi.org/project/poutils) (`.po` utils) is is a metapackage to easily install usefull Python tools to use with po files
and `potodo` is a part of it! Go check out [Poutils](https://pypi.org/project/poutils) to discover the other useful tools for `po` file related translation!

## Installation

```bash
pip install potodo
```

## Usage

```
usage: potodo [-h] [-p path] [-e path [path ...]] [-a X] [-b X] [-f] [-o] [-n] [-c] [-j] [--exclude-fuzzy] [--exclude-reserved] [--only-reserved] [--show-reservation-dates] [--no-cache] [-i] [-l] [--version] [-v]

List and prettify the po files left to translate.

optional arguments:
  -h, --help            show this help message and exit
  -p path, --path path  execute Potodo in path
  -e path [path ...], --exclude path [path ...]
                        exclude from search
  -a X, --above X       list all TODOs above given X% completion
  -b X, --below X       list all TODOs below given X% completion
  -f, --only-fuzzy      print only files marked as fuzzys
  -o, --offline         don't perform any fetching to GitHub/online
  -n, --no-reserved     don't print info about reserved files
  -c, --counts          render list with the count of remaining entries (translate or review) rather than percentage done
  -j, --json            format output as JSON
  --exclude-fuzzy       select only files without fuzzy entries
  --exclude-reserved    select only files that aren't reserved
  --only-reserved       select only only reserved files
  --show-reservation-dates
                        show issue creation dates
  --no-cache            Disables cache (Cache is disabled when files are modified)
  -i, --interactive     Activates the interactive menu
  -l, --matching-files  Suppress normal output; instead print the name of each matching po file from which output would normally have been printed.
  --version             show program's version number and exit
  -v, --verbose         Increases output verbosity
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

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://mdk.fr"><img src="https://avatars2.githubusercontent.com/u/239510?v=4" width="100px;" alt=""/><br /><sub><b>Julien Palard</b></sub></a><br /><a href="https://github.com/Seluj78/Potodo/pulls?q=is%3Apr+reviewed-by%3AJulienPalard" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/Seluj78/Potodo/commits?author=JulienPalard" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/awecx"><img src="https://avatars1.githubusercontent.com/u/43954001?v=4" width="100px;" alt=""/><br /><sub><b>Antoine</b></sub></a><br /><a href="https://github.com/Seluj78/Potodo/pulls?q=is%3Apr+reviewed-by%3Aawecx" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/Seluj78/Potodo/commits?author=awecx" title="Code">💻</a></td>
    <td align="center"><a href="https://juleslasne.com"><img src="https://avatars0.githubusercontent.com/u/4641317?v=4" width="100px;" alt=""/><br /><sub><b>Jules Lasne (jlasne)</b></sub></a><br /><a href="https://github.com/Seluj78/Potodo/pulls?q=is%3Apr+reviewed-by%3ASeluj78" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/Seluj78/Potodo/commits?author=Seluj78" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/christopheNan"><img src="https://avatars2.githubusercontent.com/u/35002064?v=4" width="100px;" alt=""/><br /><sub><b>Christophe Nanteuil</b></sub></a><br /><a href="https://github.com/Seluj78/Potodo/pulls?q=is%3Apr+reviewed-by%3AchristopheNan" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/Seluj78/Potodo/commits?author=christopheNan" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/grenoya"><img src="https://avatars3.githubusercontent.com/u/996321?v=4" width="100px;" alt=""/><br /><sub><b>Claire Revillet</b></sub></a><br /><a href="https://github.com/Seluj78/Potodo/pulls?q=is%3Apr+reviewed-by%3Agrenoya" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/Seluj78/Potodo/commits?author=grenoya" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
