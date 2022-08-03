![Tests](https://github.com/felipefrr/map_splc/actions/workflows/tests.yml/badge.svg) [![codecov](https://codecov.io/gh/felipefrr/map_splc/branch/main/graph/badge.svg?token=O1ZP96FUIM)](https://codecov.io/gh/felipefrr/map_splc)

# Main Path Analysis

Repository for made with the intent of providing optimal implementations of Main Path Analysis (MPA) with Search Path Link Count (SPLC). The work done here is proof of concept for my undergraduation thesis at the Institute of Mathematics and Statistics (IME) in University of São Paulo (USP).

### 📝💻 Todo
- [ ] Migrate all the code of to this repo
- [ ] Write the unit tests
- [ ] Implement my own version of SPLC
- [ ] Implement cycle removal
- [ ] Implement Main Path Search
- [ ] Create good UI

## Getting started
```
# Clone this repo and change directory
git clone git@github.com:felipefrr/map_splc.git
cd map_splc

# Create a python virtualenv on your local machine (-B might be needed to execute)
make setup-venv -B

# Alternatively, built docker image
make setup

# Run the suite of tests and checks on your local machine
make checks

# Alternatively, run the suite of tests and checks on docker
make run-checks
```

## Our checks

We cover the following aspects of setting up a python project, including: Unit Tests, Code Coverage, Linting and Type Checking.

### All wrapped in a Makefile
```
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -f .coverage
	rm -f .coverage.*

clean: clean-pyc clean-test

test: clean
	. .venv/bin/activate && py.test tests --cov=src --cov-report=term-missing --cov-fail-under 95
```

### GitHub Actions with each `git push`
```
# .github/workflows/tests.yml
name: Tests
on: push
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v1
      with:
        python-version: 3.8
        architecture: x64
    - run: make setup
    - run: make check
    - run: bash <(curl -s https://codecov.io/bash)
```

## 📃 Citation

```bibtex
@misc{map-splc-package,
  author = {Felipe Ferreira, Rafael Durelli},
  title = {Main Path Analysis - SPLC},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/felipefrr/map_splc/}}
}
```
