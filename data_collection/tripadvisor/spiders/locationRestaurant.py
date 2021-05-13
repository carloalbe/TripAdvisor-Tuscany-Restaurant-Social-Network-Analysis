import scrapy
import pandas as pd
import numpy as np


class geoRestaurantsSpider(scrapy.Spider):
    name = "geoRestaurant"
    
    def __init__(self, url=None, *args, **kwargs):
        super(geoRestaurantsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'{url}']
    
    def parse(self, response):
        for div in response.css('div._1llCuDZj'):
            if div.css('::attr(data-test)').get() != 'SL_list_item':
                href = div.css('a._15_ydu6b::attr(href)').get()
                #CovidMeasures = False
                menu = False 
                txts = div.css('::text').getall()
                position = txts[0]
                name = txts[2]
                price = None
                for i, txt in enumerate(txts[3:]):
                    if txt == 'Menu': menu = True
                    #if txt == 'Taking safety measures': CovidMeasures = True
                    if txt.find(r'$') >= 0 : price = txt
                try:    score = float(div.css('svg.zWXXYhVR::attr(title)').get()[:3])
                except: score = None
                try : city = div.css('div.HhAnTQDq > div:nth-child(2)::text').get()
                except: city = None
                try: reviews = int(div.css("span.w726Ki5B::text").get().replace(',',''))
                except: reviews = 0
                
                yield {'position':int(position),'name':name, 'city':city, 'menu':menu,'link':href,'score':score,'N_reviews':reviews, 'price':price}
           
                    
        next_page = response.css('a.nav.next.rndBtn.ui_button.primary.taLnk').attrib['href']
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
            
            
            
            
            
