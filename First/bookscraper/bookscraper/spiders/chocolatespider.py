import scrapy
import re

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.css('product-item')
        for currProduct in products:
            # Extracting the raw price string
            raw_price_str = currProduct.css('span.price::text').getall()
            # Joining list elements into a single string and using regex to find price patterns
            price_str = ''.join(raw_price_str)
            price_match = re.search(r'£\d+\.?\d*', price_str)
            price = price_match.group(0) if price_match else 'Price Not Found'
            yield{
                'name': currProduct.css('a.product-item-meta__title::text').get(),
                'real_price': price,
                'price': price,
                'url': currProduct.css('div.product-item-meta a').attrib['href'],
        }

            next_page = response.css('[rel="next"] ::attr(href)').get()
            
            if next_page is not None:
                next_page_url = 'https://www.chocolate.co.uk' + next_page
                yield response.follow(next_page_url, callback=self.parse)
                