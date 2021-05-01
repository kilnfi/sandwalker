# Makefile for Sandwalker.

PYTHON := python3

all: local-run

local-run: .venv
	source .venv/bin/activate && FLASK_ENV_CONFIG=../infra/config-dev.cfg flask run --host=0.0.0.0

test: .venv
	source .venv/bin/activate && FLASK_ENV_CONFIG=../infra/config-test.cfg python tests.py

.venv:
	mkdir -p .venv
	$(PYTHON) -m venv .venv
	source .venv/bin/activate && pip3 install -r infra/requirements.txt
