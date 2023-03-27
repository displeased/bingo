"""
Bingo-Board generator.
"""

import subprocess
import tempfile
import argparse
import pathlib
import random
import shutil
import sys
import os

NUM_TERMS = 24

METADATA_HEADER = """---
title: 'bingo'
free: '\\textbf{Free}'
"""
METADATA_FOOTER = "..."

BUILD_DIR = pathlib.Path("build/")

PLACEHOLDER_FILE = "placeholder.md"
TEMPLATE_FILE = pathlib.Path("templates/bingo.tex")
OUTPUT_FILE = pathlib.Path("./bingoboard.pdf")


def get_letters(num_letters: int) -> list[str]:
    """
    Creates a list of letters a-z of size num_letters
    :num_letters int: the range of a-z to cover
    """
    start_letter: int = ord("a")

    if num_letters > 26:
        num_letters = (num_letters % 25) + 1

    return [chr(start_letter + i) for i in range(num_letters)]


# pylint: disable=too-many-arguments
def compile_document(
    build_dir: pathlib.Path,
    placeholder: pathlib.Path,
    metadata: pathlib.Path,
    template: pathlib.Path,
    output: pathlib.Path,
    engine: str,
) -> bool:
    """Compiles the resulting pdf document."""
    try:
        subprocess.run(
            [
                "pandoc",
                placeholder,
                "--metadata-file",
                metadata,
                "--template",
                template,
                "-o",
                output,
                "--pdf-engine",
                engine,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=10,
            cwd=build_dir,
            check=True,
        )
        return True
    except subprocess.CalledProcessError as error:
        if error.returncode == 47:
            print(f"error: pandoc could not find pdf engine '{engine}'!")
            print("consider using the -e flag to specify a different engine.")
            return False

        print("error: error occured during pandoc execution:")
        if error.stdout is not None:
            print(error.stdout.decode("utf-8"))
        return False


def main() -> None:
    """
    The main function is responsible for creating a metadata.yaml
    for use in the pandoc templating feature.
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-t",
        "--terms",
        type=pathlib.Path,
        default=pathlib.Path("./terms"),
        help="Set the path for the terms.",
    )
    parser.add_argument(
        "-e",
        "--engine",
        default="pdflatex",
        help="The latex engine to use for compilation.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        default=OUTPUT_FILE,
        help="The output file path.",
    )
    args = parser.parse_args()

    if not args.terms.is_file():
        print(f"error: file '{args.terms}' does not exist!")
        print("consider using the -t flag to specify a valid terms file.")
        sys.exit(-1)

    with open(args.terms, "r", encoding="utf-8") as file:
        content = file.read()

    terms = content.strip().split("\n")

    if len(terms) < NUM_TERMS:
        print(f"error: not enough terms in '{args.terms}'!")
        sys.exit(-1)

    random.shuffle(terms)
    letters = get_letters(len(terms))

    build_dir = pathlib.Path(tempfile.mkdtemp())
    metadata_file = build_dir / "metadata.yaml"

    with open(metadata_file, "w", encoding="utf-8") as file:
        file.write(METADATA_HEADER)

        for letter, term in zip(letters, terms):
            file.write(f"{letter}: {term}\n")

        file.write(METADATA_FOOTER)

    template_path = pathlib.Path(
        os.path.join(os.path.dirname(__file__), f"{TEMPLATE_FILE}")
    )

    placeholder_path = build_dir / PLACEHOLDER_FILE
    # pylint: disable=consider-using-with
    open(placeholder_path, "w", encoding="utf-8").close()

    run = compile_document(
        build_dir,
        placeholder_path,
        metadata_file,
        template_path,
        args.output.resolve(),
        args.engine,
    )

    os.remove(placeholder_path)
    os.remove(metadata_file)
    build_dir.rmdir()

    if not run:
        sys.exit(-1)


if __name__ == "__main__":
    main()
