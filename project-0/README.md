# **Project 0**

## **Introduction**

Project 0 is split into two parts: degrees and tic-tac-toe. In degrees, we will try to find out the degree of separation between two actors/actresses (similar to the infamous "Six Degrees of Kevin Bacon"). In tic-tac-toe, we implement the popular game's AI using the minimax algorithm that we learned in lecture 0. Details on both parts of the project are given below.

---

### **Degrees**

To find the shortest path between two actors/actresses, we will represent each actor as a node in an undirected graph. The nodes contain three instance attributes: state, parent, and action. In the context of the problem, the state is the actor/actress (it's actually an ID that maps to the name of the actor/actress, but for simplicity we'll just say it's the actor/actress), the parent is a co-star in the movie whose edge we followed to get to the current node, and the action is the movie they starred in with the parent. 

Since this is a shortest paths problem, the search algorithm of choice is breadth-first search. Breadth-first search works by checking all the immediate child nodes of the starting node, and then checking the immediate children nodes' child nodes (and so on) until the target node is found. If the entire network is exhausted and the target is not found, then there is no path from the starting node to the target node. Pseudocode for the shortest path algorithm used in degrees is shown below:

    def shortestPath(source, target):
        create a node for the source
        initialize an empty queue, which will be the frontier
        initialize an empty set, which will contain the nodes we're already explored
        add the source node to the queue

        while the frontier is not empty:
            remove a node from the frontier and add it to the explored set
            for every neighboring node (more formally called "adjacent" nodes):
                if the neighboring node is the target:
                    backtrack to get the path from source to target
                else:
                    if the neighboring node is not already in the queue and is not in the explored set:
                        add the neighboring node to the frontier

        if we exhaust the frontier and we haven't found the target, there is no path
---

### **Tic-Tac-Toe**

In this assignment, we are asked to implement almost all the functions except initial_state(), which was already done for us. While I could write a bit about each function, the interesting one to talk about is minimax(), which uses many of the other functions as helpers. Minimax is the algorithm that allows our AI to play well; it works by considering all possible moves in a given board state and looking multiple moves ahead (in the case of tic-tac-toe, the search depth is all the way until the game has reached a conclusion) to determine whether the move is good or not. We determine how good a move is based on a numerical value given to each branch in the search tree. If the computer is playing "X", it will try to maximize this value, and if the computer is playing "O", it will try to minimize this value. The functions for minimizing and maximizing the value of a given board state are based on the pseudocode given by Brian during lecture 0. The pseudocode for minimax is given below:

    def minimax(board):
        if it is X's turn to play:
            set a variable v to -inf
            set a variable optimalAction to null
            for each legal move in the position:
                if the minimized result of playing the move is greater than v:
                    set v to the minimized value
                    set optimalAction to the move we've considered
            return optimalAction
        else:
            set a variable v to inf
            set a variable optimalAction to null
            for each legal move in the position:
                if the maximized result of playing the move is less than v:
                    set v to the maximized value
                    set optimalAction to the move we've considered
            return optimalAction

        def maximize(state):
            if the game is over:
                return -1, 0, 1 depending on who won
            set v to -inf
            for each possible legal move:
                set v to the smaller of v and the minimized value of the result of playing the move
            return v

        def minimize(state):
            if the game is over:
                return -1, 0, 1 depending on who won
            set v to inf
            for each possible legal move:
                set v to the larger of v and the maximized value of the result of playing the move
            return v