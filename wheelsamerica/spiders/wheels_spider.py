import scrapy
from wheelsamerica.items import WheelsamericaItem


class WheelsSpiderSpider(scrapy.Spider):
    name = "wheels_spider"
    url = "https://wheelsamerica.com/shop/"

    def start_requests(self):
        yield scrapy.Request(
            url='https://wheelsamerica.com/',
            callback=self.parse,
            dont_filter=True
        )


    def parse(self, response):
        self.logger.info(f"Scraping page: {response.url}")
        
        product_links = response.css('div.product-small.box div.box-text a.woocommerce-LoopProduct-link::attr(href)').getall()
        if not product_links:
            product_links = response.css('p.name.product-title a::attr(href)').getall()
        
        self.logger.info(f"Found {len(product_links)} products on this page")
        
        for link in product_links:
            yield response.follow(link, self.parse_wheel_details)

        next_page = response.css('ul.page-numbers a.next::attr(href)').get() 
        if next_page:
            self.logger.info(f"Following next page: {next_page}")
            yield response.follow(next_page, self.parse)

    def parse_wheel_details(self, response):
        self.logger.info(f"Parsing wheel detail - URL: {response.url}")
        
        item = WheelsamericaItem()
        
        title = response.css('h1.product-title.product_title.entry-title::text').get()
        item['title'] = title.strip() if title else None
        
        inventory = response.css('p.stock.in-stock::text').get()
        item['inventory'] = inventory.split(' ')[0] if inventory else None
                 
        condition = response.css('div.wheel-specs p:nth-child(1) strong::text').get()
        item['condition'] = condition.split(' ')[-1] if condition else None

        int_vari = response.css('div.wheel-specs p:nth-child(2) strong::text').get()
        if int_vari:
            parts = int_vari.split('||')
            item['interchange'] = parts[0].split(':')[-1].strip() if ':' in parts[0] else parts[0].strip()
            item['variations'] = parts[-1].split(':')[-1].strip() if len(parts) > 1 and ':' in parts[-1] else None
        else:
            item['interchange'] = None
            item['variations'] = None

        size = width = lugs = spokes = bolt_circle = finish = None
        
        table_rows = response.css('table.wheel-spec-table tbody tr')
        for row in table_rows:
            tds = row.css('td')
            if len(tds) >= 6:
                size = tds[0].css('::text').get()
                width = tds[1].css('::text').get()
                lugs = tds[2].css('::text').get()
                spokes = tds[3].css('::text').get()
                bolt_circle = tds[4].css('::text').get()
                finish = tds[5].css('::text').get()
        
        item['sizes'] = size
        item['width'] = width
        item['lugs'] = lugs
        item['spokes'] = spokes
        item['bolt_circle'] = bolt_circle
        item['finish'] = finish
        
        price = "".join(response.css('div.product-price-container p.price.product-page-price span.woocommerce-Price-amount.amount bdi ::text').getall()).strip()
        item['price'] = price if price else None
        
        item['desc2'] = response.css('div.panel.entry-content p:nth-of-type(2)::text').get()
        
        int2 = response.css('div.panel.entry-content h5::text').get()
        item['Int2'] = int2.split(':')[-1].strip() if int2 and ':' in int2 else int2
        
        item['vehicles'] = response.css('div.panel.entry-content p:nth-of-type(4) i::text').getall()
        item['partnumbers'] = response.css('div.panel.entry-content p:nth-of-type(5) i::text').getall()
        item['indents'] = response.css('div.panel.entry-content p:nth-of-type(6) i::text').getall()
        
        yield item