[comment]: <> (<p align="center"><img width=12.5% src="https://github.com/afpy/potodo/blob/master/media/Logo.png"></p>)
<p align="center"><img width=60% src="https://github.com/afpy/potodo/blob/master/media/Potodo.png"></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Build status](https://img.shields.io/github/workflow/status/afpy/potodo/Tests)
[![GitHub Issues](https://img.shields.io/github/issues/afpy/potodo.svg)](https://github.com/afpy/potodo/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![PyPI](https://img.shields.io/pypi/v/potodo)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## What is it ?

Potodo, a (almost) flawless TODO/progress listing CLI tool for po files.

### Potodo is part of poutils!

[Poutils](https://pypi.org/project/poutils) (`.po` utils) is is a metapackage to easily install usefull Python tools to use with po files
and `potodo` is a part of it! Go check out [Poutils](https://pypi.org/project/poutils) to discover the other useful tools for `po` file related translation!


## Installation

```sh
pip install potodo
```

## Usage example

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

## Development setup

Create a virtual environment
```sh
python3 -m venv venv
```

Activate it
```sh
source venv/bin/activate
```

Install the dev requirements
```sh
pip install -r requirements-dev.txt
```

Install the pre-commit hook
```sh
pre-commit install
```

Install `potodo` in a development version
```
pip install -e .
```

## Release History

* v0.19.2
    * Dropped `cache_args` to simplify cache functionality
* v0.19.1
    * Fixed a bug of division by 0
    * Replaced Travis-ci tests with github actions
* v0.19.0
    * Fixed windows support
* v0.17.3
    * Fixed a math error where the completion %age of a folder was wrong
    * Fixes on the `.potodoignore` file
* v0.17.0
    * Added tests
    * Fixed bug where github would rate limit your IP address
    * Fixed argument errors
    * Added `-l` `--matching-files` Which will print the path of files matching your arguments
* v0.16.0
    * Args passed to potodo are now cached as well ! This allows for a better control of what is cached !
    * The ignore file now works as the .gitignore does. Add a venv/ in your .potodoignore for example :)
* v0.15.0
    * Potodo now supports .potodoignore files ! You can finally ignore the venv you made 🎉
* v0.14.3
    * Added cache versioning to avoid errors when cache changes, for example if files are moved between `potodo` versions.
* v0.14.2
    * Nothing new, just code moved around ! Thanks for sticking around 🎉
* v0.14.1
    * Added `--only-reserved` option to display only reserved filed
    * Added `--reserved-dates` to display when a file was reserved
    * Added cache to cache `pofiles` to speedup the reading process
    * Added logging for verbosity
    * Added interactive option with `--interactive`
    * Added contributors in the readme
* < v0.14.1
    * Base version
 
## Contributing

1. Fork it (<https://github.com/afpy/potdo/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`

`/!\` Don't forget to bump the version in `potodo/__init__.py` when you're pushing your changes to your branch

3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


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
