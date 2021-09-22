import random
import os

NUM_TERMS_ON_BOARD = 24

def main():
    """
    The main function is responsible for creating a metadata.yaml for use
    in the pandoc templating feature/
    """

    # read terms from file
    with open('terms', 'r') as file:
        terms = file.read()

    # split the terms into a list and remove the last
    # element (because it's an endline)
    terms = terms.split('\n')
    terms = terms[:len(terms) - 1]

    if len(terms) < NUM_TERMS_ON_BOARD:
        print("ERROR: Not enough terms in file - you have",
                len(terms),
                "terms, you need a minimum of",
                NUM_TERMS_ON_BOARD,
                "terms!")
        exit(-1)

    # randomly shuffle the terms and get letters to
    # assign the terms to
    random.shuffle(terms)
    letters = get_letters(len(terms))

    with open('metadata.yaml', 'w') as file:
        # fill in the default information
        file.write("---\n")
        file.write("title: 'bingo'\n")
        file.write("free: '\\textbf{Free}'\n")

        # write all terms to the metadata file with
        # associated letters
        for i in range(NUM_TERMS_ON_BOARD):
            next_line = letters[i] + ": '" + terms[i] + "'\n"
            file.write(next_line)

        # write end metadata symbol
        file.write("...")

def get_letters(num_letters: int) -> list[str]:
    """
    Creates a list of letters a-z of size num_letters
    :num_letters int: the range of a-z to cover
    """

    # make sure num_letters is within range
    while num_letters > 26:
        num_letters -= 26

    # fill letters list with characters
    letters = []
    for i in range(num_letters):
        letters.append(chr(i + 97))

    return letters

if __name__ == "__main__":
    main()
