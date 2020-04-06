# **Project 1**

Like Project 0, Project 1 is split into two parts: knights and minesweeper. In knights, we use propositional logic and the power of AI to solve "Knights and Knaves" style puzzles. In minesweeper, we also use propositional logic, but in this case, we're trying to build an AI that plays minesweeper well (not perfect though, because sometimes you just have to make a random move).

---

### **Knights**

In knights, we are asked to develop the knowledge bases necessary to solve the 4 puzzles. In general, my approach to all the puzzles was to start by listing what I know about the structure of the problems. That is to say, I know that a character can be a knight or a knave, but not both. After that, I looked at what the problem tells us. Whenever a character says something like "I am a knight", there are two cases. If a character, A, is a knight, then "I am a knight" is true because knights always tell the truth. If A is actually a knave, then "I am a knight" is false, since knaves always lie. In the knowledge base, we encode this by saying that if A is a knight, then A is a knight (more formally, AKnight *implies* AKnight) and if A is a knave, then A is not a knight (AKnave *implies* not AKnight). We do this for all the information given to us in the puzzle, and if we did it right, running the puzzle file will print out whether each character is a knight or a knave. Once we have an answer, we can verify the solution ourselves by making sure there are no contradictions.

---

### **Minesweeper**

TBD

