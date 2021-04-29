# Makefile for Sandwalker.

PYTHON := python3

all: local-run

local-run: .venv
	source .venv/bin/activate && FLASK_ENV_CONFIG=config.cfg flask run

test: .venv
	source .venv/bin/activate && FLASK_ENV_CONFIG=config-test.cfg python tests.py

.venv:
	mkdir -p .venv
	$(PYTHON) -m venv .venv
	source .venv/bin/activate && pip3 install -r infra/requirements.txt
