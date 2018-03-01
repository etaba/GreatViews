# GreatViews
Airbnb web crawler which finds rooms with great views! GreatViews takes in a prepared airbnb url and searches through all the room results' reviews for keywords indicating if that room has a good view. Start by preparing your search on Airbnb. Enter all your filters (you can omit price range if you wish to set that from the command line). When airbnb brings up your search results, use that url as the input to the crawler. 

# Usage
`python greatViews.py <quick | thorough> <minPrice> <maxPrice> "<url>"`
Example:
`python greatView.py quick 565 750 "https://www.airbnb.com/s/Tokyo--Japan/homes?query=Tokyo%20Homes&refinement_paths%5B%5D=%2Fhomes&allow_override%5B%5D=&room_types%5B%5D=Entire%20home%2Fapt&adults=4&checkin=2018-04-28&checkout=2018-05-01&s_tag=GkLTftGD"`

## <quick | thorough>
`quick` will crawl airbnb using regular requests, and will be much faster than the `thorough` alternative. The caveat is that without javascript support, only the first page of reviews, and only the first few sentences of each review can be crawled. This might limit the number of hits found. 
`thorough` uses selenium chrome webdriver. To use this mode you will need to download the chrome webdriver and place it in your $PATH. See the 'Drivers' section of the selenium installation guide for more info on how to accomplish that: http://selenium-python.readthedocs.io/installation.html. With `thorough` mode, the first two pages of reviews of each room will be scanned in their entirety, usually resulting in more hits.
The code has commented-out sections which provide multithreaded crawling. While this greatly increases the speed of the program, for me this resulted in my IP being blacklisted from airbnb after about 100 scraped pages. Uncomment with caution.

## Modifying the search
If you'd like to use this crawler to search for other airbnb aspects, simply modify the `KEYWORDS` list to include the keywords you believe indicate a room has what you need.

## Example output:
![Alt text](/greatViewsScreenshot.jpg?raw=true "Example Output")
