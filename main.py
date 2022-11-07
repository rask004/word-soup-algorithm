from string import ascii_uppercase
from random import choice
from copy import copy


width = 12
height = 12

directions = [
    (1,-1),
    (1,0),
    (1,1),
    (0,1),
    (-1,1),
    (-1,0),
    (-1,-1),
    (0,-1),
]

PLACEHOLDER = '.'


def find_all_idx(s, ch):
    return [i for i, c in enumerate(s) if c == ch]


def getWordPositionsFromUsedLocation(word, grid, location, ndx):
    wordPositions = []
    x, y = location
    length = len(word)
    if ndx < 0 or ndx >= length:
        raise IndexError(f"ndx should be integer from 0 to len(word) - 1, cannot be negative. params: word={word} ndx={ndx}")
    if grid[y][x] != word[ndx]:
        raise RuntimeError(f"the indexed letter for this word should match the letter at the relevant position in the grid. Params: {word} {ndx} {position} {grid}")
    for d in directions:
        xD, yD = d
        # change x, y to the start of the word
        x = x - ndx * xD
        y = y - ndx * yD
        letterLocations = [ (x + xD * i, y + yD * i) for i in range(length) ]
        locationsInBounds = [ l[0] >= 0 and l[1] >= 0 and l[0] < width and l[1] < height for l in letterLocations ]
        if False in locationsInBounds:
            # print(f"Skipped, out of puzzle bounds. Direction {d}, location {location}, word {word}")
            continue
        gridLocations = [ grid[l[1]][l[0]] for l in letterLocations ]        
        letterMatches = [ word[i] == l or PLACEHOLDER == l for i, l in enumerate(gridLocations) ]
        if False in letterMatches:
            # print(f"Skipped, bad overlap with another word. Direction {d}, location {location}, word {word}")
            continue
        wordPositions.append( (x, y, (xD, yD)) )
    return wordPositions


def getWordPositionsFromEmptyLocation(word, grid, location):
    wordPositions = []
    x, y = location
    length = len(word)
    
    for d in directions:
        xD, yD = d
        letterLocations = [ (x + xD * i, y + yD * i) for i in range(length) ]
        locationsInBounds = [ l[0] >= 0 and l[1] >= 0 and l[0] < width and l[1] < height for l in letterLocations ]
        if False in locationsInBounds:
            # print(f"Skipped, out of puzzle bounds. Direction {d}, location {location}, word {word}")
            continue
        gridLocations = [ grid[l[1]][l[0]] for l in letterLocations ]        
        letterMatches = [ word[i] == l or PLACEHOLDER == l for i, l in enumerate(gridLocations) ]
        if False in letterMatches:
            # print(f"Skipped, bad overlap with another word. Direction {d}, location {location}, word {word}")
            continue
        wordPositions.append( (x, y, (xD, yD)) )
    return wordPositions


def findWordPositions(word, puzzle):
    positions = []
    for y, line in enumerate(puzzle):
        for x, letter in enumerate(line):
            if letter == PLACEHOLDER:
                for p in getWordPositionsFromEmptyLocation(word, puzzle, (x, y)):
                    positions.append(p)
            else:
                for n in find_all_idx(word, letter):
                    for p in getWordPositionsFromUsedLocation(word, puzzle, (x, y), n):
                        positions.append(p)                
    return positions


def placeWord(word, position, puzzle):
    tmp_puzzle = copy(puzzle)
    x, y, direction = position
    xD, yD = direction
    for l in word:
        tmp_puzzle[y][x] = l
        y += yD
        x += xD
    return tmp_puzzle


def makePuzzle(words):
    puzzle = []
    for _ in range(height):
        line = [PLACEHOLDER for _ in range(width)]
        puzzle.append(line)
    
    words = sorted(words, key=lambda x: len(x))
    if len(words[-1]) > height and len(words[-1]) > width:
        raise RuntimeError("word {} too long to fit in puzzle of dimensions {}x{}".format(words[-1], width, height))
    
    available_words = [x for x in words]
    puzzle_stack = []
    puzzle_state = copy(puzzle)
    current_word = available_words[-1]
    
    while len(available_words):
        # print("processing >>", current_word)
        positions = findWordPositions(current_word, puzzle_state)
        if not len(positions):
            if not len(puzzle_stack):
                raise RuntimeError("Cannot create a puzzle using this word list with these puzzle dimensions?")
            available_words.append(current_word)
            current_word, puzzle_state = puzzle_stack.pop()
            continue
        p = choice(positions)
        puzzle_state = placeWord(current_word, p, puzzle_state)
        puzzle_stack.append( (current_word, puzzle_state) )
        available_words.pop()
        if not len(available_words):
            continue
        current_word = available_words[-1]

    
    for y in range(height):
        for x in range(width):
            if puzzle[y][x] == '.':
                puzzle[y][x] = choice(ascii_uppercase)
    return puzzle


def getWords(fp):
    words = [x.upper().strip() for x in fp.readlines()]
    return words


def showWords(words):
    for w in words:
        print(w)


def showPuzzle(puzzle):
    for row in puzzle:
        line = "".join(row)
        print(line)


def main():
    with open("wordList.txt") as fp:
        words = getWords(fp)
    puzzle = makePuzzle(words)
    print("")
    showWords(words)
    print("\n--------\n")
    showPuzzle(puzzle)


if __name__ == "__main__":
    main()
