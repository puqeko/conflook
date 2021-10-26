# Conflook

A command line utiltiy for inspecting hard-to-read project config files such as json, yaml, and toml.

## Usage

```
conflook eg.toml database
```

Gives

```
database, Table(4)
server         String(11) 192.168.1.1
ports          Array(3)   [8001, 8001, 8002]
connection_max Integer    5000
enabled        bool       True
```

Map-like objects are shown as a list of keys followed by their type followed by a preview of their contents.

Note that if no matching key is found then conflook will show

- The shortest key for which the given key is a prefix, or
- The closest matching key as determined by difflib

For example,

```
conflook eg.toml database.p
```

Gives

```
database.ports, Array(3)
[8001, 8001, 8002]
```

## Install

To be described.

## Develop

1. Download this repository `git clone ...`.

2. [Install PDM](https://pdm.fming.dev/#installation).
   Use PDM to install python dependancies with `pdm sync`.

   PDM will keep the versions of 3rd party libraries consistent with `pdm.lock`. The 3rd party libraries which this project depend on are listed in `pyproject.toml` along with other project settings used by the [PyPI](https://pypi.org) and exposing a command when installed.

3. [Enable pre-commit](https://pre-commit.com/#install).
   Will run automatic checks for each `git commit`, as described in `.pre-commit-config.yaml`. [Pylint](https://pylint.org) will check for the things specified in `pylintrc.toml`. Sometimes these checks can be ignored with a `# pylint: disable=` comment if they are too pedantic.

PDM should install an editable package. Make sure to put `pdm run` before any commands to make sure the correct Python interpreter is being used and the projects dependancies are avaliable. For example, `pdm run conflook ...` will run this utility, `pdm run pre-commit run` will manually run pre-commit checks, and `pdm run python` will start an interactive python session.

The folder `eg/` contains example files.
