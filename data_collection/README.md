 # TRIPADVISOR SCRAPY CRAWLER
 ## CONTENTS
 
 ### Spiders
 In the folder spider insdie the crawler, three scrapy spiders are acessible:
 - geoRestaurant
 - reviewsRestaurant
 - Restaurants
 
 ### Others
 The file *getAllReviews*
 
 ## Usage
 ###  Main csvs
 First step is to obtain initial csvs. Use for this the *geoRestaurant* spider to crawl an entire list of restaurant from a geographic page of tripadvisor (or similar) about restaurants such this one: 
 
 ...to have your csv you need to go in the root folderof the crawler ad run from terminal: 
 
```bash

scrapy crawl geoRestaurant -a url="http://www.tripadvisor.com/yourpageurl.html" -O "your/output/file.csv"

```
### Reviews
Once you have your csv, you can scrape all reviews of all the restaurants collected in your cvs.
The file `getAllReviews.py` can be runned by command line. You need to specify as argument the name of the csv fiel you want to iterate.

  
```bash

pytyon getAllReviews.py -a csv="your/csvfile.csv"

```
 Across all the link on the csv the spider named `reviewsRestaurant` will collect all review for that restaurant and wirting those in json file inside a folder calles as the initial csv.
 It will take a long time probably, accordingly to the csv size and the number of reviews of each restaurant.
 
 **N.B** Can be very useful modifying `getAllReviews.py` basing on what you need.
 
 ### Enrichment
 To scrape more information from the main page of each restaurant, another spider is needed. So use `Restaurants` to iterate once over a specific csv , obtaining a complementary version for this csv with information not present on the first list explored. So csv is completeed with information such as: specialDiets, covidMeasure(*boolean*), geographical coordinates, and more geographical information useful to complete and correct the ones alredy owned.
 
 ```bash

scrapy crawl Restaurants -a csv="your/originalfile.csv" -O "your/newfile.csv"

```
 
