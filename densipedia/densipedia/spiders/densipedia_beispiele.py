import scrapy


class DensipediaBeispieleSpider(scrapy.Spider):
    name = 'densipedia-beispiele'
    allowed_domains = ['densipedia.ch']
    start_urls = ['https://www.densipedia.ch/gute-beispiele/']

    def parse(self, response):
        articles = response.css('div.view-map-results article')
        for article in articles:
            location = article.css('.location::text').get().strip()
            slug = article.css('a::attr(href)').get()
            if slug:
                slug = slug.replace('/','',1)
                city = ""
                canton = ""
                if ", " in location:
                    components = location.split(", ")
                    if len(components) > 0:
                        city = components[0]
                    if len(components) > 1:
                        canton = components[-1]
                yield {
                    'slug': slug,
                    'title': article.css('a span::text').get(),
                    'location': location,
                    'city': city,
                    'canton': canton,
                    'lat': article.css('.location::attr(data-location-lat)').get(),
                    'lng': article.css('.location::attr(data-location-lng)').get(),
                }
