all: clean build

build:
	python3 generate-metadata.py
	pandoc --quiet metadata.yaml --template templates/bingo.tex -o bingoboard.pdf --pdf-engine=xelatex

clean:
	rm -f bingoboard.pdf metadata.yaml

.PHONY: all build clean
