define TARGET_HELP
Available targets:
    all       # install dependencies
    install   # build and install program
    uninstall # uninstall program
    dist      # create distribution archive
    check     # run type checks and lints
    setup     # install dependencies
    clean     # clean build/run artifacts
    help      # show this help message
endef
export TARGET_HELP

all: setup

setup:
	poetry lock --no-update
	poetry install --no-root

install:
	poetry build -f wheel
	pip install dist/*.whl

uninstall:
	pip uninstall bingo -y

dist:
	poetry build -f sdist

check:
	poetry run mypy --install-types --non-interactive
	poetry run mypy
	poetry run pylint bingo

fmt:
	poetry run black bingo

help:
	@echo "$$TARGET_HELP"

clean:
	rm -rf .mypy_cache/ **/__pycache__/ dist/


.PHONY: all setup install uninstall dist check fmt help clean
