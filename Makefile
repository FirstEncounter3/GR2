.ONESHELL:

.DEFAULT_GOAL := run

PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip

venv/bin/activate: requirements.txt
	apt install python3.10-venv
	python3 -m venv venv
	chmod +x venv/bin/activate
	. ./venv/bin/activate
	$(PIP) install -r requirements.txt

venv: venv/bin/activate
	. ./venv/bin/activate

run: venv
	$(PYTHON) main.py

clean:
	rm -rf __pycache__
	rm -rf venv
