from scrapy.spiders import CSVFeedSpider
import os

class DensipediaCasesSpider(CSVFeedSpider):
    name = 'densipedia-cases'
    allowed_domains = ['densipedia.ch']
    DIR = os.getenv('DIR', '')
    start_urls = [f'file://{DIR}/densipedia/data/densipedia.csv']

    def parse_row(self, response, row):
        yield response.follow(f'https://www.densipedia.ch/{row["slug"]}', callback=self.parse_content, cb_kwargs=dict(row=row))

    def parse_content(self, response, row):
        infoboxes = response.css('div.paragraph--type--infobox div')
        for infobox in infoboxes:
            if infobox.css('h3::text').get() == 'Kennziffern':
                facts = infobox.css('ul li::text').getall()
                facts_parsed = {}
                for key in keys:
                    facts_parsed[key] = None
                for fact in facts:
                    # fact = fact.css('::text').get()
                    if ': ' in fact:
                        fact_key, fact_value = fact.split(": ")
                        fact_key = fact_key.replace('(', '').replace(')','')
                        fact_value = fact_value.replace(' ',' ')
                        if 'Arbeitsplatzpotenzial' in fact_key:
                            fact_key = 'Anzahl Arbeitsplätze'
                            fact_value = fact_value.replace(' Beschäftigte','')
                        elif 'Anzahl Bewohner' in fact_key or 'Einwohnerpotenzial' in fact_key or 'Einwohnerzahl' in fact_key:
                            fact_key = 'Anzahl Bewohner'
                            fact_value = fact_value.replace(' Personen','')
                        elif 'dichte' in fact_key:
                            fact_key = 'Einwohnerdichte'
                            fact_value = fact_value.replace('Einwohner/km','')
                        elif 'Wohneinheiten' in fact_key:
                            fact_key = 'Anzahl Wohneinheiten'
                        elif 'Parkplatzanzahl' in fact_key or 'Parkplätze' in fact_key or 'Abstellplätze' in fact_key:
                            fact_key = 'Anzahl Parkplätze'
                        elif 'Parkplatzkoeffizient' in fact_key or 'Parkplatzquotient' in fact_key or 'Parkplatz-Koeffizient' in fact_key:
                            fact_key = 'Parkplatzkoeffizient'
                            fact_value = fact_value.replace(',','.').replace(' PP/WE','')
                            fact_value = fact_value.replace(' PP / WE','')
                        elif 'Arealgrösse' in fact_key or 'Arealfläche' in fact_key:
                            fact_key = 'Arealfläche'
                            fact_value = fact_value.replace(' m','')
                        elif 'Ausnützungsziffer' in fact_key:
                            fact_key = 'AZ'
                            fact_value = fact_value.replace(',','.').replace(' m','')
                        elif 'Bruttogeschossfläche' in fact_key:
                            fact_key = 'BGF'
                            fact_value = fact_value.replace(' m','')
                        elif 'Hauptnutzfläche' in fact_key:
                            fact_key = 'HNF'
                            fact_value = fact_value.replace(' m','')
                        elif 'Anrechenbare Geschossfläche' in fact_key:
                            fact_key = 'aGF'
                            fact_value = fact_value.replace(' m','')
                        elif 'Gewerbe' in fact_key or 'Gewerbe' in fact_key:
                            fact_key = 'Geschäftsflächen'
                            fact_value = fact_value.replace(' m','')
                        elif 'Durchschnittlicher täglicher Verkehr' in fact_key:
                            fact_key = 'Durchschnittlicher täglicher Verkehr vorher/nachher'
                        elif 'Gemeindetypologie BFS' in fact_key:
                            fact_key = 'Gemeindetyp BFS'
                        elif 'Investitionskosten' in fact_key or 'Kosten' in fact_key:
                            fact_key = 'Investitionskosten'
                            fact_value = fact_value.replace(' CHF','').replace(' Franken', '').replace(',','.')
                            if 'Mio.' in fact_value or 'Millionen' in fact_value:
                                fact_value = fact_value.replace(' Mio.','').replace(' Millionen','')
                                # fact_value = fact_value * 1000000
                        elif 'ÖV-Güterklasse' in fact_key:
                            fact_key = 'ÖV-Güteklasse'
                        fact_value = fact_value.replace('ca. ','')
                        fact_value = fact_value.replace('’','').replace('‘','').replace('²','')
                        fact_value = fact_value.replace('\'','')
                        fact_value = fact_value.replace('rund ','')
                        facts_parsed[fact_key] = fact_value
                        facts_parsed['slug'] = row['slug']
                yield facts_parsed


keys = [
    'slug',
    'Anzahl Arbeitsplätze', # 'Arbeitsplatzpotenzial',
    'Anzahl Bewohner', # 'Einwohnerpotenzial', 'Einwohnerzahl',
    'Einwohnerdichte',
    'Anzahl Wohneinheiten', # 'Wohneinheiten Neubau', 'Wohneinheiten WE',
    'Anzahl Parkplätze', # 'Parkplatzanzahl', 'Anzahl Abstellplätze', 'Parkplätze',
    'Parkplatzkoeffizient', # 'Parkplatz-Koeffizient', 'Parkplatzquotient',
    'Arealfläche', # 'Arealgrösse',
    'AZ', # Ausnützungsziffer', # 'Ausnützungsziffer AZ',
    'BGF', #'Bruttogeschossfläche', 'Bruttogeschossfläche BGF',
    'HNF', # 'Hauptnutzfläche HNF ',
    'aGF', # 'Anrechenbare Geschossfläche',
    'Geschäftsflächen', # 'Gewerbe-, Ladenfläche', 'Dienstleistungs- und Gewerbeflächen',
    'Durchschnittlicher täglicher Verkehr vorher/nachher', # 'Durchschnittlicher täglicher Verkehr DTV vorher/nachher',
    'Gemeindetyp BFS', # 'Gemeindetypologie BFS',
    'Investitionskosten', # 'Investitionskosten Neubau Schossberg', 'Kosten',
    'Länge des Abschnitts',
    'ÖV-Güteklasse', # 'ÖV-Güterklasse'
]