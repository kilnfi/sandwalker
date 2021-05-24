# Makefile for Sandwalker.

PYTHON := python3

all: local-run

local-run: .venv
	source .venv/bin/activate && flask run --host=127.0.0.1

test: .venv
	source .venv/bin/activate && DATABASE_URI="sqlite:///:memory:" python tests.py

.venv:
	mkdir -p .venv
	$(PYTHON) -m venv .venv
	source .venv/bin/activate && pip3 install -r requirements.txt
