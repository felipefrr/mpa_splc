.PHONY: setup-venv setup clean-pyc clean-test test mypy lint docs check

setup-venv:
	python3 -m venv .venv && . .venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements.dev
	pip install -r requirements.prod

setup:
	 DOCKER_BUILDKIT=1 docker build -t dev -f Dockerfile .

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -f .coverage
	rm -f .coverage.*
	find . -name '.pytest_cache' -exec rm -fr {} +

clean: clean-pyc clean-test
	find . -name '.my_cache' -exec rm -fr {} +
	rm -rf logs/

test: clean
	. .venv/bin/activate && py.test tests --benchmark-disable --cov=src --cov-report=term-missing --cov-fail-under 95

mypy:
	. .venv/bin/activate && mypy src

lint:
	. .venv/bin/activate && pylint src -j 4 --reports=y

docs: FORCE
	cd docs; . .venv/bin/activate && sphinx-apidoc -o ./source ./src
	cd docs; . .venv/bin/activate && sphinx-build -b html ./source ./build
FORCE:

checks: test lint mypy clean

run-checks:
	docker run --rm -it --name run-checks -v $(shell pwd):/opt -t dev make checks

bash:
	docker run --rm -it --name run-checks -v $(shell pwd):/opt -t dev bash

performance-compare:
	@echo [ === BENCHMARK === ]
	pytest --disable-warnings --benchmark-save=edge_weights --benchmark-verbose --benchmark-save-data benchmarks/benchmark_edge_weights_functions.py
	pytest --disable-warnings --benchmark-save=edge_weights_heavy --benchmark-verbose --benchmark-save-data benchmarks/benchmark_edge_weights_heavy.py -k 'test_calc_splc_optimized'

heavy-benchmark:
	pytest --disable-warnings --benchmark-save=heavy_functions --benchmark-verbose --benchmark-save-data benchmarks/benchmark_optimized.py > benchmark_output.txt

heavy-benchmark-main-path:
	pytest --disable-warnings --benchmark-save=heavy_functions --benchmark-verbose --benchmark-save-data benchmarks/benchmark_optimized.py > benchmark_main_path_output.txt