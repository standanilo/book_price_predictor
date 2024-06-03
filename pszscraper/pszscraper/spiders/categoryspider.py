import scrapy

c = {}

class CategoriesSpider(scrapy.Spider):
    name = 'categories'
    start_urls = ['https://www.knjizare-vulkan.rs/domace-knjige/']

    category_urls = []
    category_visited = []
    
    def parse(self, response):
        category_urls = response.css('div#nb_f-kategorije').css('::attr(href)').getall()
        CategoriesSpider.category_urls += [url for url in category_urls]

        while True:
            times = 0
            for category_url in CategoriesSpider.category_urls:
                if category_url in CategoriesSpider.category_visited:
                    continue
                times +=1
                yield response.follow(category_url, self.parse_category)
            if times == 0:
                break
            
        
    def parse_category(self, response):
        CategoriesSpider.category_visited.append(response.url)
        CategoriesSpider.category_urls += [res for res in response.css('div#nb_f-kategorije').css('::attr(href)').getall()]
        main_category = self.get_main_category(response)
        subcategory = self.get_subcategory(response)
        if main_category == "" or subcategory == "" :
            return
        else:
            yield {
                'main_category': main_category,
                'subcategory': subcategory,
            }
    
    def get_main_category(self, response):
        try:
            return response.css('div.breadcrumbs div.container a')[3].attrib['title']
        except:
            return ""

    def get_subcategory(self, response):
        try:
            return response.css('div.breadcrumbs div.container li.active::text').get()
        except:
            return ""


            