import scrapy
import urllib

class reviewsRestaurantsSpider(scrapy.Spider):
    name = "reviewsRestaurant"
    
    def __init__(self, url=None, *args, **kwargs):
        params = {'filterLang':'ALL'}
        super(reviewsRestaurantsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'{url}?{urllib.parse.urlencode(params)}']
        
                               
    def parse(self, response):
        for div in response.css('div.review-container'):
            username = div.css('div.info_text.pointer_cursor > div::text').get()
            if username.find(' ')>0:
                username += ' ' + div.css('img.basicImg::attr(data-mediaid)').get()
            
            date = div.css('span.ratingDate::attr(title)').get()
            visit = div.css('div.prw_rup.prw_reviews_stay_date_hsx::text').get()
            try: likes = int(div.css('span.numHelp::text').get().split(' ')[0])
            except: likes = 0
            viaMobile = False
            if div.css('span.viaMobile').get() != None: viaMobile = True
            try: no_reviews = int(div.css('span.badgeText::text').get().split(' ')[0])
            except: no_reviews = 1
            try: vote = int(div.css('span.ui_bubble_rating::attr(class)').get().split(' ')[1][-2:])
            except: vote = None
              
            yield {'username':username, 'date': date, 'vote': vote, 'viaMobile': viaMobile, 'likes': likes, 'N_reviews': no_reviews}
                    
        next_page = response.css('a.nav.next.ui_button.primary')
        if next_page is not None:
            yield response.follow(next_page.attrib['href'],callback=self.parse)
           
        
     