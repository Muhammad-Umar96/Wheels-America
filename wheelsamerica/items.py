# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WheelsamericaItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    inventory = scrapy.Field()
    condition = scrapy.Field()
    interchange = scrapy.Field()
    variations = scrapy.Field()
    sizes = scrapy.Field()
    width = scrapy.Field()
    lugs = scrapy.Field()
    spokes = scrapy.Field()
    bolt_circle = scrapy.Field()
    finish = scrapy.Field()
    price = scrapy.Field()
    desc2 = scrapy.Field()
    Int2 = scrapy.Field()
    vehicles = scrapy.Field()
    partnumbers = scrapy.Field()
    indents = scrapy.Field()
