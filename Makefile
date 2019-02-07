# GNU Make
# https://www.gnu.org/software/make/

# Import env vars
# include .env

# Set additional variables
DIR?=$(shell pwd)

#--------------------------------------------------------
# - Default rule
#--------------------------------------------------------
.PHONY: default
default:

#--------------------------------------------------------
# - Setup Python3 venv
#--------------------------------------------------------
.PHONY: setup
setup: venv install_requirements

.PHONY: venv
venv: env/bin/activate
	python3 -m venv env

env/bin/activate:
	source $(PWD)/env/bin/activate

.PHONY: install_requirements
install_requirements:
	pip install -r requirements.txt

.PHONY: deactivate
deactivate:
	deactivate

#--------------------------------------------------------
# - Install azdevman
#--------------------------------------------------------
.PHONY: install
install:
	pip install -e .
