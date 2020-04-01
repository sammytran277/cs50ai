# Project 0a: Degrees
# Given the name of two actors, displays the "path" from
# one actor to another, if it exists

import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Setting up variables to conduct breadth-first search
    srcNode = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    exploredActors = set()
    frontier.add(srcNode)

    # Keep exploring the frontier while there are still actors in the queue
    while not frontier.empty():
        currNode = frontier.remove()
        exploredActors.add(currNode.state)

        # Get all actors that have starred in a movie with the current actor
        for neighbor in neighbors_for_person(currNode.state):
            # We've found the target actor, so we're done
            if neighbor[1] == target:
                movies = []
                actors = []

                # Backtrack to get the path from source actor to target actor
                neighborNode = Node(state=neighbor[1], parent=currNode, action=neighbor[0])
                while neighborNode is not None:
                    if neighborNode.action != None:
                        movies.append(neighborNode.action)
                    if neighborNode.state != source:
                        actors.append(neighborNode.state)
                    neighborNode = neighborNode.parent
                
                # Reorganize the lists so they are in the right order
                movies.reverse()
                actors.reverse()

                # If these two lists aren't the same length, something is wrong
                assert len(movies) == len(actors)

                # Build the (movie_id, person_id) tuples and append them to the path
                path = []
                for i in range(len(movies)):
                    path.append((movies[i], actors[i]))

                return path

            # Only add a neighbor if we have not already explored their node and if they aren't already in the queue
            if not frontier.contains_state(neighbor[1]) and neighbor[1] not in exploredActors:
                newNode = Node(state=neighbor[1], parent=currNode, action=neighbor[0])
                frontier.add(newNode)

    # If we've exhausted the entire queue and haven't found the target, there is no connection
    return None


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
