import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If the number of cells is equal to the bomb count, then all the cells are bombs
        if len(self.cells) == self.count:
            return self.cells

        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If the count is ever 0, then all surrounding cells are safe
        if self.count == 0:
            return self.cells

        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If we know a cell is a mine, then we can remove that cell 
        # from the sentence and decrease the count by 1
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If we know a cell is safe, then we can remove the cell from the sentence
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Steps 1 and 2
        self.moves_made.add(cell)
        self.safes.add(cell)

        # Update the knowledge base since we know the cell is safe
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

        # Step 3: Add a new sentence to the AI's knowledge base
        neighbors = set()
        sentenceCount = count
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Add cell to neighbors set if its within bounds and
                # its current state is unknown
                if (0 <= i < self.height) and (0 <= j < self.width):
                    if (i, j) in self.mines:
                        sentenceCount -= 1
                    elif (i, j) not in self.moves_made:
                        neighbors.add((i, j))

        newInfo = Sentence(neighbors, sentenceCount)
        self.knowledge.append(newInfo)

        # Step 4: Mark additional cells as safe or as mines if it can be inferred
        for sentence in self.knowledge:
            if len(sentence.cells) == sentence.count:
                for cell in sentence.known_mines():
                    self.mines.add(cell)
            elif sentence.count == 0:
                for cell in sentence.known_safes():
                    self.safes.add(cell)
            else:
                continue
            
            # Remove the sentence so the knowledge base doesn't grow too large
            self.knowledge.remove(sentence)

        # Step 5: Add new sentences if they can be inferred from knowledge base
        for i in range(len(self.knowledge)):
            for j in range(i + 1, len(self.knowledge)):
                # Ignore when i and j are the same sentence
                if self.knowledge[i] == self.knowledge[j]:
                    continue

                # Case when set pointed to by j is a subset of i
                elif self.knowledge[i].cells.issubset(self.knowledge[j].cells):
                    inferredCells = self.knowledge[j].cells.difference(self.knowledge[i].cells)
                    inferredCount = self.knowledge[j].count - self.knowledge[i].count
                    inferredSentence = Sentence(inferredCells, inferredCount)
    
                    # Only add the sentence to knowledge if its new info
                    if inferredSentence not in self.knowledge:
                        self.knowledge.append(inferredSentence)

                # Case when set pointed to by j is a subset of i
                elif self.knowledge[j].cells.issubset(self.knowledge[i].cells):
                    inferredCells = self.knowledge[i].cells.difference(self.knowledge[j].cells)
                    inferredCount = self.knowledge[i].count - self.knowledge[j].count
                    inferredSentence = Sentence(inferredCells, inferredCount)

                    # Only add the sentence to knowledge if its new info
                    if inferredSentence not in self.knowledge:
                        self.knowledge.append(inferredSentence)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # We'll make a safe move by iterating over all the squares known to be safe,
        # and if we haven't made that move yet, we'll return that cell
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # We'll select a random move by iterating over all the cells and arbitrarily
        # picking one that hasn't been played and is not a bomb
        for i in range(self.height):
            for j in range(self.width):
                potentialCell = (i, j)
                if (potentialCell not in self.moves_made) and (potentialCell not in self.mines):
                    return potentialCell

        return None