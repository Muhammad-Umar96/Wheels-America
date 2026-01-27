import scrapy
from wheelsamerica.items import WheelsamericaItem


class WheelsSpiderSpider(scrapy.Spider):
    name = "wheels_spider"
    url = "https://wheelsamerica.com/shop/"
    
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, meta={'page_num': 1})

    def parse(self, response):
        page_num = response.meta.get('page_num', 1)
        self.logger.info(f"Scraping page {page_num}")
        
        wheels = response.css('div.product-small.box')
        for wheel in wheels:
            info = wheel.css('div.image-fade_in_back a::attr(href)').get()
            yield scrapy.Request(url=info, callback=self.parse_wheel_details, meta={'page_num': page_num})

        # Move pagination logic here instead of in parse_wheel_details
        if page_num < 693:
            next_page_num = page_num + 1
            next_page = f"https://wheelsamerica.com/shop/page/{next_page_num}/"
            yield scrapy.Request(url=next_page, callback=self.parse, meta={'page_num': next_page_num})

    def parse_wheel_details(self, response):
        page_num = response.meta.get('page_num', 'unknown')
        self.logger.info(f"Parsing wheel detail from page {page_num}")
        
        item = WheelsamericaItem()
        title = response.css('h1.product-title.product_title.entry-title::text').get()
        main_title = title.strip()
        inventory = response.css('p.stock.in-stock::text').get()
        if inventory:
            num_inventory = inventory.split(' ')[0] 
        else:
            num_inventory = None  
                 
        condition = response.css('div.wheel-specs p:nth-child(1) strong::text').get()
        if condition:
            fin_condition = condition.split(' ')[-1]
        else:
            fin_condition = None

        int_vari = response.css('div.wheel-specs p:nth-child(2) strong::text').get()
        if int_vari:
            interchange = int_vari.split('||')[0].split(':')[-1].strip()
            variations = int_vari.split('||')[-1].split(':')[-1].strip()
        else:
            interchange = None
            variations = None

        table = response.css('table.wheel-spec-table tbody tr')
        for row in table:
            td = row.css('td')
            size = td[0].css('::text').get()
            width = td[1].css('::text').get()
            lugs = td[2].css('::text').get()
            spokes = td[3].css('::text').get()
            bolt_circle = td[4].css('::text').get()
            finish = td[5].css('::text').get()
        price = "".join(response.css('span.woocommerce-Price-amount.amount bdi ::text').getall()).strip()
        desc2 = response.css('div.panel.entry-content p:nth-of-type(2)::text').get()
        Int2 = response.css('div.panel.entry-content h5::text').get()
        Int2_final = Int2.split(':')[-1].strip()
        vehicles = response.css('div.panel.entry-content p:nth-of-type(4) i::text').getall()
        partnumbers = response.css('div.panel.entry-content p:nth-of-type(5) i::text').getall()
        idents = response.css('div.panel.entry-content p:nth-of-type(6) i::text').getall()

        item['title'] = main_title
        item['inventory'] = num_inventory
        item['condition'] = fin_condition
        item['interchange'] = interchange
        item['variations'] = variations
        item['sizes'] = size
        item['width'] = width
        item['lugs'] = lugs
        item['spokes'] = spokes
        item['bolt_circle'] = bolt_circle
        item['finish'] = finish
        item['price'] = price
        item['desc2'] = desc2
        item['Int2'] = Int2_final
        item['vehicles'] = vehicles
        item['partnumbers'] = partnumbers
        item['indents'] = idents
        yield item