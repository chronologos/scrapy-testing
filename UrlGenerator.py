"""Run this to generate list of URLs to pass to NumPagesSpider."""
import json

# GLOBAL SETTINGS
MALE_NAME_FILE = "census-dist-male-first.txt"
FEMALE_NAME_FILE = "census-dist-female-first.txt"
URL_BASE = "http://search.princeton.edu/search/index/ff/c/f/$NAME/af/c/a//lf/c/l//pf/c/p//tf/c/t//faf/c/fa//df/c/d//ef/c/e//submit/submit"


def interpolate(url, names, tokens):
    """Given some URL with $tokens, interpolate with corresponding names.
        Example: www.$name.com, ['mallory'], ["$name"] becomes www.mallory.com.
    """
    for index, token in enumerate(tokens):
        if token in url:
            prefix, suffix = url.split(token)
            url = prefix + names[index] + suffix
    return url


def _getNames(male_file, female_file):
    """Extract names from namefiles."""
    names = []
    with open(male_file) as some_file:
        for line in some_file:
            names.append(line.split(" ", 2)[0].lower())

    with open(female_file) as some_file:
        for line in some_file:
            names.append(line.split(" ", 2)[0].lower())
    return names


def go():
    """ Dump URLs as json formatted file."""
    names = _getNames(MALE_NAME_FILE, FEMALE_NAME_FILE)
    start_urls = [interpolate(URL_BASE, [name], ["$NAME"]) for name in names]

    with open('urls.json', 'w') as some_file:
        a = json.dumps(start_urls)
        some_file.write(a)
    return start_urls

if __name__ == "__main__":
    go()
