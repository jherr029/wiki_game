def get_drop_categories():
    """Returns a list of strings from caterogies_to_drop.txt"""
    with open('categories_to_drop.txt') as f:
        content = f.readlines()

    return [x.rstrip() for x in content]