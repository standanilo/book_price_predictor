import scrapy


class BookSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['https://www.knjizare-vulkan.rs/domace-knjige/page-' + str(i) for i in range(0, 1031)]
    
    def parse(self, response):
        for booklink in response.css('a.product-link::attr(href)').getall():
            yield response.follow(booklink, self.parse_book)
            
    def parse_book(self, response):
        yield {
            'title': self.get_title(response),
            'author': self.get_author(response),
            'category': self.get_category(response),
            'publisher': self.get_publisher(response),
            'year': self.get_year(response),
            'pages': self.get_pages(response),
            'binding': self.get_binding(response),
            'format': self.get_format(response),
            'description': self.get_description(response),
            'price': self.get_price(response),
            'weight': self.get_weight(response),
        }
        
    def get_title(self, response):
        try:
            return response.css('h1 span::text').get()
        except:
            return ""
    
    def get_author(self, response):
        try:
            fields = response.css('td').getall()
            for field in range(0, len(fields)):
                if response.css('td')[field].css('::text').get().lower().strip() == "autor":
                    return response.css('td')[field+1].css('a::text').get().strip()
            return ""
        except:
            return ""
    
    def get_category(self, response):
        try:
            fields = response.css('td').getall()
            for field in range(0, len(fields)):
                if response.css('td')[field].css('::text').get().lower().strip() == "kategorija":
                    return response.css('td')[field+1].css('a::text').get().strip()
            return ""
        except:
            return ""
    
    def get_publisher(self, response):
        try:
            fields = response.css('td').getall()
            for field in range(0, len(fields)):
                if response.css('td')[field].css('::text').get().lower().strip() == "izdavač":
                    return response.css('td')[field+1].css('a::text').get().strip()
            return ""
        except:
            return ""
    
    def get_year(self, response):
        try:
            fields = response.css('td').getall()
            for field in range(0, len(fields)):
                if response.css('td')[field].css('::text').get().lower().strip() == "godina":
                    return response.css('td')[field+1].css('::text').get().strip()
            return ""
        except:
            return ""
    
    def get_pages(self, response):
        try:
            fields = response.css('td').getall()
            for field in range(0, len(fields)):
                if response.css('td')[field].css('::text').get().lower().strip() == "strana":
                    return response.css('td')[field+1].css('::text').get().strip()
            return ""
        except:
            return ""
    
    def get_binding(self, response):
        try:
            fields = response.css('td').getall()
            for field in range(0, len(fields)):
                if response.css('td')[field].css('::text').get().lower().strip() == "povez":
                    return response.css('td')[field+1].css('::text').get().strip()
            return ""
        except:
            return ""
    
    def get_format(self, response):
        try:
            fields = response.css('td').getall()
            for field in range(0, len(fields)):
                if response.css('td')[field].css('::text').get().lower().strip() == "format":
                    return response.css('td')[field+1].css('::text').get().strip()
            return ""
        except:
            return ""
    
    def get_description(self, response):
        try:
            descriptions = response.css('div#tab_product_description::text').getall()
            return "".join(descriptions).strip()
        except:
            return ""
    
    def get_price(self, response):
        try:
            return "".join(response.css('div span.product-price-value.value::text').getall()).strip()
        except:
            return ""
    
    def get_weight(self, response):
        try:
            fields = response.css('td').getall()
            for field in range(0, len(fields)):
                if response.css('td')[field].css('::text').get().lower().strip() == "težina specifikacija":
                    return response.css('td')[field+1].css('::text').get().strip()
            return ""
        except:
            return ""