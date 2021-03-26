import os
import random
import re
import sys
from copy import deepcopy

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
    pages = corpus.keys() #list of pages
    num_pages = len(corpus)
    links = corpus[page] #set of links
    num_links = len(links)

    if num_links == 0:
        num_links = num_pages

    amongst_pages = (1 - damping_factor) / num_pages
    amongst_links = damping_factor / num_links

    probability_distribution = {}
    for pg in pages:
        probability = amongst_pages
        if pg in links:
            probability += amongst_links
        probability_distribution[pg] = probability

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #generate a sample
    pages = list(corpus.keys()) #list of pages
    parent = random.choice(pages)
    sample = []
    for i in range(n):
        sample.append(parent)
        transition = transition_model(corpus, parent, damping_factor)
        parent = random.choices(list(transition.keys()), list(transition.values()))[0]
    
    #calculate the pagerank
    page_rank = dict()
    for page in pages:
        num_appeard = sample.count(page)
        page_rank[page] = num_appeard/n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = corpus.keys()
    N = len(corpus)

    page_rank = dict()
    for page in pages:
        page_rank[page]=1/N

    while True:
        before_modification = deepcopy(page_rank)
        for page in pages:

            i_pages =[i for i in pages if page in corpus[i]]

            s = 0
            for i_page in i_pages:

                num_i_links = len(corpus[i_page])
                if num_i_links == 0:
                    num_i_links = N

                s += page_rank[i_page]/num_i_links 

            pr = (1-damping_factor)/N + damping_factor*s
            page_rank[page] = pr
        
        count = 0
        for key in page_rank:
            if abs(page_rank[key] - before_modification[key]) <= 0.001:
                count += 1

        if count == N:
            break
    
    return page_rank


if __name__ == "__main__":
    main()
