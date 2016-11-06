import scrapy


# INSTRUCTIONS (on mac OSX)
# install scrapy with: pip install scrapy
# run script with: scrapy scrape.py > emails.txt

MALE_NAME_FILE = "census-dist-male-first.txt"
FEMALE_NAME_FILE = "census-dist-female-first.txt"
URL_BASE = "http://search.princeton.edu/search?ff=c&f=$NAME&af=c&a=&lf=c&l=&pf=c&p=&tf=c&t=&faf=c&fa=&df=c&d=&ef=c&e=&submit=submit"

def interpolate(URL_BASE, names, tokens):
    """Given some URL with $tokens, interpolate with corresponding names."""
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


class DirectorySpider(scrapy.Spider):
    name = "PRINCETON"
    names = _getUrls(MALE_NAME_FILE, FEMALE_NAME_FILE)
    start_urls = [interpolate(URL_BASE, [name], ["$NAME"]) for name in names]

    def parse(self, response):
        for result in response.css('span.value.email'):
            print(result.css('a::attr("href")').extract_first().split(":")[1])
        




