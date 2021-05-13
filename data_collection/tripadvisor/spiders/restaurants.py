import scrapy
import urllib
import pandas as pd
import pybase64

class RestaurantsSpider(scrapy.Spider):
    name = "Restaurants"
    
    def __init__(self, csv=None, *args, **kwargs):
        super(RestaurantsSpider, self).__init__(*args, **kwargs)
        self.df = pd.read_csv(csv)
        self.i = 0
        self.start_urls =  ['https://www.tripadvisor.com/'+self.df.loc[self.i,'link']] 
     
                               
    def parse(self, response):
         
        pageurl = self.df.loc[self.i,'link']
        
        if response.css('img._1_zmoVbU').get() != None: covidMeasure = True
        else: covidMeasure = False
        if response.css('span._9ZPAmdk6').get() != None: travellersChoice = True
        else: travellersChoice  = False  
        if response.css("span.ui_icon.verified-checkmark._2QiauFRP").get() != None : claimed = True 
        else: claimed = False
            
        try:
            positionlink = response.css("div.xAOpeG9l * a._2wKz--mA._27M8V6YV::attr(data-encoded-url)").get()
        except: positionlink = None
        
        if positionlink !=None:
            try:
                positionlink = pybase64.b64decode(positionlink).decode('UTF-8')
                coordinates = positionlink.split('@')[1].split('_')[0].split(',')      
                #positionlink[positionlink.find('@')+1:positionlink.find('_',-5,-1)].split(',')
                latitude = float(coordinates[0])
                longitude = float(coordinates[1])
            except: 
                coordinates = None
                latitude = None
                longitude = None
        else:
            coordinates = None
            latitude = None
            longitude = None

        try: geolist = [item.extract() for item in response.css('ul.breadcrumbs > li.breadcrumb *::text')]
        except: geolist = [None for i in range(15)]
        province = geolist[9]
        city = geolist[12]
        name = geolist[-1]
        
        
        cuisines = None
        meals = None
        specialDiets = None
        
        try :
            sections= response.css("div._14zKtJkz::text").getall()
            contents = response.css("div._1XLfiSsv::text").getall()
            
            for i, section in enumerate(sections):
                if section.lower() == 'cuisines': cuisines = contents[i]
                elif section.lower() == 'meals' : meals = contents[i]
                elif section.lower() == 'special diets': specialDiets = contents[i]
                
        except: pass
            
            
        yield {'Name':name, 'Link' : pageurl, 'Province': province, 'City':city, 'claimed': claimed, 'covidMeasure': covidMeasure, 'travellersChoice':travellersChoice, 'latitude': latitude, 'longitude': longitude, 'cuisines':cuisines, 'meals':meals,'specialDiets':specialDiets, 'coordinates':coordinates,'positionlink':positionlink}
                    
        self.i += 1
        try: next_page = 'https://www.tripadvisor.com/'+self.df.loc[self.i,'link']
        except: next_page = None
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
           
        