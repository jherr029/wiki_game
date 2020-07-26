import sys
import random
import wikipedia

from time import time
from functools import wraps

from utils import get_drop_categories

def main():
    # get_random_wikipage()
    starting_page = get_random_wikipage()
    ending_page = get_random_wikipage()

    # starting_page = get_wiki_page('Barack Obama')
    # ending_page = get_wiki_page('University District, Seattle')

    # current_page = get_wiki_page(starting_page)
    child_pages = get_wiki_links(starting_page)

    master_search_list = []
    master_search_list.append(child_pages)

    print(starting_page, 'has', len(child_pages), 'child-pages.')
    print(master_search_list)

    ret = wikipedia_game_search(master_search_list, ending_page)

    if ret == 1:
        print('Loser')

    print('Done?')
    # page_categories = get_wiki_categories(page)

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:', f.__name__, 'took:', te - ts, 'sec')
        return result
    return wrap

@timing
def wikipedia_game_search(master_search_list, ending_page):
    match = False

    for search_list in master_search_list:
        if search_for_end_page(search_list, ending_page):
            return 0

        random.shuffle(search_list)
        for page in search_list:
            print('Searching on', page)
            new_links = get_wiki_links(page)
            
            if new_links == None:
                continue

            if search_for_end_page(new_links, ending_page):
                return 0

            master_search_list.append(new_links)

    return 1

    # while (child_pages and not match):
    #     match = search_for_end_page(child_pages, ending_page)
    
    #     random_page = get_random_page_from_pages(child_pages)
    #     child_pages.remove(random_page.title)



def get_random_wikipage():
    """Return a random wikipedia page"""
    random_page = wikipedia.random()
    print(random_page)
    return random_page


def get_wiki_page(title_page):
    """Return wikipediaPage of specified title"""
    page = wikipedia.page(title=title_page)
    return page


def get_wiki_categories(wikipedia_page):
    """Return a list of cateogires of the page.
    """
    if type(wikipedia_page) == str:
        wikipedia_page = get_wiki_page(wikipedia_page)

    categories = wikipedia_page.categories
    drop_list = get_drop_categories()
    categories = [x for x in categories if x not in drop_list]

    return categories


def get_wiki_links(title_of_page):
    try:
        wikipedia_page = get_wiki_page(title_of_page)
        links = wikipedia_page.links
    except wikipedia.PageError:
        print('Could not find wikipedia page for', title_of_page)
        links = None
    except wikipedia.DisambiguationError:
        print('Need to DisambiguationError error for', title_of_page)
        links = None
    return links


def search_for_end_page(pages, end_page):
    if end_page.title in pages:
        print('PASS')
        return True
    
    return False
    
    
def get_random_page_from_pages(pages):
    random_page = random.choice(pages)
    return get_wiki_page(random_page)




if __name__ == '__main__':
    main()