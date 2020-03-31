class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier = []
    
    def push(self, node):
        self.frontier.append(node)
    
    def containsState(self, state):
        return any(node.state == state for node in self.frontier)
    
    def isEmpty(self):
        return len(self.frontier) == 0

    def pop(self):
        if self.isEmpty():
            raise Exception("Empty StackFrontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def pop(self):
        if self.isEmpty():
            raise Exception("Empty QueueFrontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze:
    def __init__(self, mazeFile):
        self.mazeFile = mazeFile
        self.mazeLayout = []
        self.mazeHeight = 0
        self.mazeWidth = 0
        self.numExplored = 0
        self.startState = None
        self.goalState = None
        self.shortestPath = None

        self.parseMazeFile()

    def parseMazeFile(self):
        """Parses maze file, sets maze layout and finds start and endpoint of the maze"""
        
        with open(self.mazeFile) as f:
            for row in f:
                self.mazeLayout.append(row.rstrip().split())

        for row in self.mazeLayout:
            for node in row:
                if node == "A":
                    self.startState = (self.mazeLayout.index(row), row.index(node))
                elif node == "B":
                    self.goalState = (self.mazeLayout.index(row), row.index(node))

        self.mazeHeight = len(self.mazeLayout)
        self.mazeWidth = len(self.mazeLayout[0])

    def printShortestPath(self):
        """Prints the shortest path from start to end"""

        assert self.shortestPath != None

        for i in range(self.mazeHeight):
            for j in range(self.mazeWidth):
                if (i, j) in self.shortestPath[1] and (i, j) != self.startState and (i, j) != self.goalState:
                    print("*", end=" ")
                else:
                    print(self.mazeLayout[i][j], end=" ")
            print()

    def getShortestPath(self):
        """Find the shortest path from start to end"""

        start = Node(state=self.startState, parent=None, action=None)
        frontier = QueueFrontier()
        explored = set()
        
        frontier.push(start)

        while (not frontier.isEmpty()):
            currNode = frontier.pop()
            self.numExplored += 1

            # If the node contains a goal state, then we're done
            if currNode.state == self.goalState:
                actions = []
                cells = []

                # Backtrack to get path 
                while currNode.parent is not None:
                    actions.append(currNode.action)
                    cells.append(currNode.state)
                    currNode = currNode.parent
                
                # Reorder path from start to end
                actions.reverse()
                cells.reverse()
                self.shortestPath = (actions, cells)
                
                return len(self.shortestPath[0])

            # Mark node as explored so we don't revisit
            explored.add(currNode.state)

            # Add neighboring nodes if they have not been explored and aren't in the frontier
            for d, a in self.getValidDirections(currNode):
                newChild = Node(state=(d[0], d[1]), parent=currNode, action=a)
                if newChild.state not in explored and not frontier.containsState(newChild):
                    frontier.push(newChild)

    def getValidDirections(self, node):
        """Return a list of node states representing valid neighbors"""
        up, down = (-1, 0), (1, 0)
        left, right = (0, -1), (0, 1)
        directions = [up, down, left, right]

        validDirections = []
        for d in directions:
            potentialNeighbor = (node.state[0] + d[0], node.state[1] + d[1])
            
            # Check for invalid indexes
            if (potentialNeighbor[0] < 0) or (potentialNeighbor[0] > self.mazeHeight - 1) or (potentialNeighbor[1] < 0) or (potentialNeighbor[1] > self.mazeWidth - 1):
                continue
            
            # Add node if it isn't a wall
            elif self.mazeLayout[potentialNeighbor[0]][potentialNeighbor[1]] != "1":
                validDirections.append((potentialNeighbor, d))

        return validDirections


    def __str__(self):
        maze = ""
        for row in self.mazeLayout:
            for cell in row:
                maze += str(cell) + " "
            maze += "\n"
        return maze


if __name__ == "__main__":
    file = input("Enter filename to test: ")
    maze = Maze(file)
    print("\nMaze Layout:\n{}".format(maze))
    print("Length of Shortest Path: {}\n".format(maze.getShortestPath()))
    print("Shortest Path:")
    maze.printShortestPath()