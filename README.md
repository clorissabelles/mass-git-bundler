# mass-git-bundler
A simple python script to bundle a list of repositories from a simple csv file.

Note: this tool does not clean up the cloned repositories afterwards, doing so yourself is easy as they are all cloned into a repositories folder.

## Usage
```shell
python bundle.py <path to repositories.csv file>
```

## repositories.csv file format
Each line should consist of two values:
1. The friendly name for the repository.
2. The clone url for the repository

### Example
```csv
mass-git-bundler,https://github.com/clorissabelles/mass-git-bundler.git
```