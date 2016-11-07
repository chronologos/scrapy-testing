import json
import logging
import math
import scrapy
logger = logging.getLogger("mylogger")
RESULTS_PER_PAGE = 20  # how many results displayed per page on princeton directory

class NumPagesSpider(scrapy.Spider):
    """Generate a list of URLs to scrape based on a name list and calculates number of pages needed to scrape"""
    name = "NumPagesSpider"
    with open('urls.json', 'r') as f:
        a = f.readline()
    start_urls = json.loads(a)
    logger.info(start_urls)
    url_page_map = {start_url: 0 for start_url in start_urls}
    def parse(self, response):
        logger.info("PARSER STARTED")
        result = response.css("div#results")
        count = math.ceil(int(result.css("p::text").extract_first().split("of")[-1].strip())/RESULTS_PER_PAGE)
        ret = []
        for i in range(1, count):
            ret.append(response.url+"/page/"+str(i))
        return {response.url: ret}
