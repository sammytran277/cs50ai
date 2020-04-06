# Project 1a: Knights
# Use AI to solve "Knights and Knaves" style puzzles given a
# knowledge base by the user

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A can be a knight or a knave
    Or(AKnight, AKnave),
    # A cannot be both a knight and a knave
    Not(And(AKnight, AKnave)),
    # If A is a knight, then A is both a knight and a knave
    (Implication(AKnight, And(AKnight, AKnave))),
    # If A is a knave, then A is not both a knight and a knave
    (Implication(AKnave, Not(And(AKnight, AKnave))))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A can be a knight or a knave
    Or(AKnight, AKnave),
    # A cannot be both a knight and a knave
    Not(And(AKnight, AKnave)),
    # B can be a knight or a knave
    Or(BKnight, BKnave),
    # B cannot be both a knight and a knave
    Not(And(BKnight, BKnave)),
    # If A is a knight, then A and B are knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is a knave, then A and B are not knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A can be a knight or a knave
    Or(AKnight, AKnave),
    # A cannot be both a knight and a knave
    Not(And(AKnight, AKnave)),
    # B can be a knight or a knave
    Or(BKnight, BKnave),
    # B cannot be both a knight and a knave
    Not(And(BKnight, BKnave)),
    # If A is a knight, then either A and B are both knights or both knaves
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # If A is a knave, then either A and B are both not knights or both not knaves
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # If B is a knight, then either A is a knight and B is a knave, or A is a knave and B is a knight
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # If B is a knave, then either A and B are knights or A and B are knaves
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A can be a knight or a knave
    Or(AKnight, AKnave),
    # A cannot be both a knight and a knave
    Not(And(AKnight, AKnave)),
    # B can be a knight or a knave
    Or(BKnight, BKnave),
    # B cannot be both a knight and a knave
    Not(And(BKnight, BKnave)),
    # C can be a knight or a knave
    Or(CKnight, CKnave),
    # C cannot be both a knight or a knave
    Not(And(CKnight, CKnave)),
    # A said "I am a knight" or "I am a knave" (we don't know which)
    Or(
        And(Implication(AKnight, AKnight), Implication(AKnave, Not(AKnight))),
        And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))
    ),
    # If B is a knight, then A said "I am a knave"
    Implication(
        BKnight,
        And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))
    ),
    # If B is a knave, then A did not say "I am a knave"
    Implication(
        BKnave,
        Not(And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave))))
    ),
    # If B is a knight, then C is a knave
    Implication(BKnight, CKnave),
    # If B is a knave, then C is not a knave
    Implication(BKnave, Not(CKnave)),
    # If C is a knight, then A is a knight
    Implication(CKnight, AKnight),
    # If C is a knave, then A is not a knight
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
