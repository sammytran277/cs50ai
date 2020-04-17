import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    distribution = {}

    # There is a (1 - d) chance that we'll land on a random page in the corpus,
    # regardless of whether or not it is linked to the current page
    for pageName in corpus.keys():
        distribution[pageName] = (1 - damping_factor) / len(corpus)
    
    # If the page has no outgoing links, the probability of landing on any page
    # in the corpus is equal among all pages
    if len(corpus[page]) == 0:
        for pageName in distribution.keys():
            distribution[pageName] = 1 / len(corpus)
    else:
        # Probability of landing on a given page from the links
        for link in corpus[page]:
            distribution[link] += damping_factor / len(corpus[page])

    return distribution
    

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    prValues = {}

    # Set up the PageRank dictionary 
    for page in corpus.keys():
        prValues[page] = 0

    # First page the surfer chooses is random
    currentPage = random.choice(list(corpus.keys()))
    prValues[currentPage] += 1

    # Take n samples, incrementing the corresponding counter in the PageRank dictionary by 1
    for _ in range(n):
        randomSurfDist = transition_model(corpus, currentPage, damping_factor)
        sample = random.choices(list(randomSurfDist.keys()), randomSurfDist.values())
        prValues[sample[0]] += 1

    # Divide each sample count by n to get a percentage
    for page in prValues.keys():
        prValues[page] /= n

    return prValues
        

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    prValues = {}

    # Set up the PageRank dictionary 
    for page in corpus.keys():
        prValues[page] = 1 / len(corpus)

    # Continually recalculate the PageRank values until they converge
    while True:
        newPRValues = {}
        for page in prValues.keys():
            damp = (1 - damping_factor) / len(corpus)
            sum = 0

            # If the current page has no links, assume it has links to everything
            if len(corpus[page]) == 0:
                for link in corpus.keys():
                    sum += prValues[link] / len(corpus)
            else:
                for link in corpus[page]:
                    if len(corpus[link]) != 0:
                        sum += prValues[link] / len(corpus[link])
                    else:
                        sum += prValues[link] / len(corpus)
            sum *= damping_factor 
            newPRValues[page] = damp + sum
        
        # Check for convergence
        for key, value in newPRValues.items():
            if abs(prValues[key] - value) > 0.001:
                prValues = copy.deepcopy(newPRValues)
                continue
        
        prValues = copy.deepcopy(newPRValues)
        break

    return prValues



if __name__ == "__main__":
    # testDict = {"1.html": ["2.html"], "2.html": ["1.html"]}
    # print(transition_model(testDict, "1.html", DAMPING))
    # print(sample_pagerank(testDict, DAMPING, SAMPLES))
    # print(iterate_pagerank(testDict, DAMPING))
    main()
