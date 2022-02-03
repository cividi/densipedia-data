.PHONY: all scrape scrape-entries scrape-cases

all: scrape

scrape: scrape-entries scrape-cases

scrape-entries:
	cd densipedia && DIR=$(CURDIR) scrapy crawl densipedia-beispiele -O data/densipedia.json -O data/densipedia.csv

scrape-cases:
	cd densipedia && DIR=$(CURDIR) scrapy crawl densipedia-cases -O data/densipedia-cases.json -O data/densipedia-cases.csv