# Potodo
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
Potodo, a (almost) flawless TODO/progress listing CLI tool for po files.

## Installation

```bash
pip install potodo
```

## Usage

```
usage: potodo [-h] [-p path] [-e path [path ...]] [-a X] [-b X] [-f] [-o] [-n] [-c] [-j] [--version]

List and prettify the po files left to translate.

optional arguments:
  -h, --help            show this help message and exit
  -p path, --path path  execute Potodo in path
  -e path [path ...], --exclude path [path ...]
                        exclude from search
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

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://mdk.fr"><img src="https://avatars2.githubusercontent.com/u/239510?v=4" width="100px;" alt=""/><br /><sub><b>Julien Palard</b></sub></a><br /><a href="https://github.com/Seluj78/Potodo/pulls?q=is%3Apr+reviewed-by%3AJulienPalard" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/Seluj78/Potodo/commits?author=JulienPalard" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!