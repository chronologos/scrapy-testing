import math
import scrapy

MALE_NAME_FILE = "census-dist-male-first.txt"
FEMALE_NAME_FILE = "census-dist-female-first.txt"
URL_BASE = "http://search.princeton.edu/search/index/ff/c/f/$NAME/af/c/a//lf/c/l//pf/c/p//tf/c/t//faf/c/fa//df/c/d//ef/c/e//submit/submit"
RESULTS_PER_PAGE = 20

def interpolate(URL_BASE, names, tokens):
    """Given some URL with $tokens, interpolate with corresponding names and pages."""
    url = URL_BASE
    for index, token in enumerate(tokens):
        if token in url:
            prefix, suffix = url.split(token)
            url = prefix + names[index] + suffix
    return url

def _getUrls(male_file, female_file):
    """Extract names from file."""
    names = []
    with open(male_file) as f:
        for line in f:
            names.append(line.split(" ", 2)[0].lower())

    with open(female_file) as f:
        for line in f:
            names.append(line.split(" ", 2)[0].lower())
    return names

class NumPagesSpider(scrapy.Spider):
    """Generate a list of URLs to scrape based on a name list and calculates number of pages needed to scrape"""
    name = "pagecounter"
    names = _getUrls(MALE_NAME_FILE, FEMALE_NAME_FILE)
    start_urls = [interpolate(URL_BASE, [name], ["$NAME"]) for name in names]
    url_page_map = {start_url: 0 for start_url in start_urls}
    def parse(self, response):
        final_list = []
        for result in response.css("div#results"):
            NumPagesSpider.url_page_map[response.url] = str(math.ceil(int(result.css("p::text").extract_first().split("of")[-1].strip())/RESULTS_PER_PAGE))
        # print(NumPagesSpider.url_page_map)
        for url, count in NumPagesSpider.url_page_map.items():
            for i in range(1, int(count)+1):
                print(url+"/page/"+str(i))
