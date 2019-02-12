# GNU Make
# https://www.gnu.org/software/make/

# Import env vars
# include .env

# Set additional variables
DIR?=$(shell pwd)
VENV_NAME?=venv
VENV_ACTIVATE=source ./$(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

#--------------------------------------------------------
# - Default rule
#--------------------------------------------------------
.PHONY: default
default:

#--------------------------------------------------------
# - Setup Python3 venv
#--------------------------------------------------------
.PHONY: setup
setup: venv

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	$(VENV_ACTIVATE)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -e .

run: venv
	azdevman
