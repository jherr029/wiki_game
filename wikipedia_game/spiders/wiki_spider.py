import time
import scrapy

class WikiSpider(scrapy.Spider):
    name = "wiki"

    allowed_domains = ["en.wikipedia.org"]
    
    start_urls = ['http://en.wikipedia.org/wiki/Investment_management']

    def parse(self, response):
        # This for loop will run through all href's to wiki articles

        # Old method -- did not cover list
        #for i, href in enumerate(response.css(r"p a[href*='/wiki/']::attr(href)").extract()):

        # New method -- covers list and is using xpath
        # TODO avoid iterating through citations if you use *
        for i, href in enumerate(response.xpath("//p/a/@href|//div[@class='mw-parser-output']/ul/li/@href").extract()):

            # Gets the href and the link
            # paragraph_links_overview = response.css('p a').getall()

            # Gets the title used for the href
            # paragraph_links_title = response.css('p a::text').getall()

            # Gets the href link to the article
            # paragraph_link = response.css(r'p a::atr(href)').getall()

            url = response.urljoin(href)

            print()
            print('Crawling:', url )
            print()

            req = scrapy.Request(url, callback=self.parse_links_title)

            time.sleep(5)

            print("my request:", req)

            yield req

            if i == 2:
                break

    def parse_links_title(self, response):
        data = {}

        """Removes ' - Wikipedia' from the string"""
        data['parent'] = response.css('title::text').extract()[0][:-12]

        # for artcle in enumerate(response.xpath("//p/a/@href|//div[@class='mw-parser-output']/ul/li/@href").extract()):
        raw_articles = response.xpath("//p/a/@href|//div[@class='mw-parser-output']/ul/li/*/@href").extract()

        """Use only href that contain /wiki/"""
        wiki_articles = [article for article in raw_articles if "/wiki/" in article]
        """Removes /wiki/ from the string"""
        articles = [article[6:] for article in wiki_articles]
        """Keeps only unique entries"""
        data['child'] = list(dict.fromkeys(articles))

        # data['title'] = response.css(r"p a[href*='/wiki/']::attr(href)").extract()
        
        yield data
    
