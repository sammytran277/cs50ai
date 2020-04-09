# **Project 1**

Like Project 0, Project 1 is split into two parts: knights and minesweeper. In knights, we use propositional logic and the power of AI to solve "Knights and Knaves" style puzzles. In minesweeper, we also use propositional logic, but in this case, we're trying to build an AI that plays minesweeper well (not perfect though, because sometimes you just have to make a random move).

---

### **Knights**

In knights, we are asked to develop the knowledge bases necessary to solve the 4 puzzles. In general, my approach to all the puzzles was to start by listing what I know about the structure of the problems. That is to say, I know that a character can be a knight or a knave, but not both. After that, I looked at what the problem tells us. Whenever a character says something like "I am a knight", there are two cases. If a character, A, is a knight, then "I am a knight" is true because knights always tell the truth. If A is actually a knave, then "I am a knight" is false, since knaves always lie. In the knowledge base, we encode this by saying that if A is a knight, then A is a knight (more formally, AKnight *implies* AKnight) and if A is a knave, then A is not a knight (AKnave *implies* not AKnight). We do this for all the information given to us in the puzzle, and if we did it right, running the puzzle file will print out whether each character is a knight or a knave. Once we have an answer, we can verify the solution ourselves by making sure there are no contradictions.

---

### **Minesweeper**

In minesweeper, we build an AI that is capable of playing minesweeper well (not perfectly however, because sometimes, you just have to pick a random move). To do so, we use the power of propositional logic to infer which squares on the board must be mines, and which squares on the board are guaranteed to be safe. As the AI makes more safe moves, it adds more information to its knowledge base by combining new information with what it already knows. For instance, if the AI already knows that there must be 2 mines in the set {A, B, C} (where A, B, and C are the coordinates of cells on the board) and later on, it learns that C is safe (perhaps by clicking on C), then it can infer that there must be 2 mines in {A, B}, and since the number of mines matches the length of the set, A and B are both cells that contain a mine. From my testing, the AI I have built seems to run fairly quickly and performed well on boards of varying sizes.

