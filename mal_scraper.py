from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup

# TODO: Find a way to limit webpages retrieved from each webpage
# https://stackoverrun.com/fr/q/9496481

class MALSpider(CrawlSpider):
    name = 'MyAnimeList'
    allowed_domains = ['myanimelist.net']
    denied_domains = ["membership","mangalist","forum","blog"]
    start_urls = [
        'https://myanimelist.net/topanime.php?type=bypopularity',
        'https://myanimelist.net/topmanga.php',
        'https://myanimelist.net/people.php',
        'https://myanimelist.net/character.php'
    ]

    rules = [
        Rule(
            LinkExtractor(canonicalize=True, unique=True, allow_domains=allowed_domains, deny_domains=denied_domains),
            callback='parse_page',
            follow=True
            )
    ]

    def parse_page(self, response):
        url = response.request.url
        if 'myanimelist.net/anime' in url or 'myanimelist.net/people' in url or 'myanimelist.net/character' in url or 'myanimelist.net/manga' in url:
            yield {
                'link': response.request.url,
                'title': response.css('title::text').get(),
                'text': BeautifulSoup(response.body).get_text().strip()
            }
