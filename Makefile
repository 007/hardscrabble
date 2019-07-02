default: help

RED:=$(shell tput setaf 1)
YLW:=$(shell tput setaf 3)
GRN:=$(shell tput setaf 2)
NOP:=$(shell tput sgr0)

help:
	@echo "Popular Make Targets:"
	@echo "   ${GRN}freeze${NOP} - freeze requirements"
	@echo ""


# basic commands
freeze:
	pip freeze | grep -v pipdeptree > requirements.txt
	pipdeptree | grep -v "^ " | grep -v -e ^setuptools -e ^wheel -e ^pipdeptree | sed 's/==.*//g' > requirements.top
