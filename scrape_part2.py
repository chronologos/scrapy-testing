import scrapy


# INSTRUCTIONS (on mac OSX)
# install scrapy with: pip install scrapy
# run script with: scrapy scrape.py > emails.txt

class DirectorySpider(scrapy.Spider):
    name = "PRINCETON"
    start_urls = []
    with open("urls") as f:
        for line in f:
            start_urls.append(line)
    def parse(self, response):
        for result in response.css('div.entry.vcard'):
            data = [0,0,0,0,0]
            for field in result.css('div.user-info').css('span.field'):
                if "Name:" in field.css('span.key').extract_first():
                    data[0] = (field.css('span.value').css('a::text').extract_first()) # name, already comma delimited
                    data[1] = field.css('span.value').css('a::attr(href)').extract_first().split(":", 2)[1] # email
                    continue
                if "Dept:" in field.css('span.key').extract_first():
                    data[2] = ";".join(field.css('span.value::text').extract()) # dept
                    data[2] = data[2].replace(",",";")
                    continue
                if "Mail:" in field.css('span.key').extract_first():
                    data[3] = ";".join(field.css('span.value::text').extract()) # mailbox
                    data[3] = data[3].replace(",",";")
            for field in result.css('div.contact-info').css('span.field'):
                if "Phone:" in field.css('span.key').extract_first():
                    data[4] = (field.css('span.value.tel::text').extract_first()) # phone number
            csv_line = ",".join([str(d) for d in data])
            print(csv_line)
