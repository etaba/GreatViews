import requests,sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
#from multiprocessing.dummy import Pool as ThreadPool


CLASS_READ_MORE = "_b82bweu"
CLASS_REVIEW = "_m7iebup"
CLASS_PAGE = "_1bdke5s"

KEYWORDS = ["scenic"," view "," view."," view!"," views","rooftop"]

def getReview(keyword,text):
    occ = text.find(keyword)
    end = text[occ:].find("<") + occ
    start = occ - text[occ::-1].find(">") + 1
    return text[start:end]

def thoroughReviewAnalysis(url,driver=None):
    print "Scraping ",url
    #uncomment if multithreading (don't though):
    #driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5)
    driver.get(url)
    reviews = []
    for i in range(2):
        try:
            #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'reviews')))
            readMoreXPath = "//div[@id='reviews']//div[@class='"+CLASS_REVIEW+"']/button[@class='"+CLASS_READ_MORE+"']"
            readMoreBtns = driver.find_elements_by_xpath(readMoreXPath)

            for btn in readMoreBtns:
                driver.execute_script("arguments[0].click();", btn)
            reviewXPath = "//div[@id='reviews']//div[@class='"+CLASS_REVIEW+"']"
            reviewDivs = driver.find_elements_by_xpath(reviewXPath)
            for reviewDiv in reviewDivs:
                reviews.append(reviewDiv.text)

            nextPageLink = driver.find_element_by_xpath('//li[@class="next next_page"]/a[1]')
            driver.execute_script("arguments[0].click();", nextPageLink)
        except Exception as e:
            break
    urlIsGood = False
    for review in reviews:
        for kw in KEYWORDS:
            count = review.count(kw)
            if count > 0:
                print "Found positive reviews for ", url
                print review
                urlIsGood = True
    #uncomment if multithreading:
    #driver.close()
    return url if urlIsGood else None

def quickReviewAnalysis(url):
    print "Scraping ",url
    urlIsGood = False
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    reviewHtml = soup.select('div#reviews')
    if len(reviewHtml)>0:
        reviewHtml = str(reviewHtml[0])
        for kw in KEYWORDS:
            count = reviewHtml.count(kw)
            if count > 0:
                print "Found positive reviews for ", url
                print getReview(kw,reviewHtml)
                urlIsGood = True
    return url if urlIsGood else None

def greatViews(url,mode,minPrice,maxPrice,keywords):
    baseUrl = url + "&price_min=" + str(minPrice) + "&price_max=" + str(maxPrice)
    #selenium code to get exact number of pages of results:
    '''d = webdriver.Chrome()
    d.get(baseUrl)
    pageBtns = d.find_elements_by_xpath("(//div[@class='"+CLASS_PAGE+"'])[last()]")
    if len(pageBtns) == 0:
        lastPageNum = 1
    else:
       lastPageNum = int(pageBtns[0].text)
    d.close()'''
    goodUrls = []
    totalRooms = 0
    i = 0
    while True:
        url = baseUrl + "&section_offset="+str(i)
        print "Checking page ",str(i+1)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        roomIds = set()
        for anchor in soup.find_all('a'):
            if "rooms" in anchor['href']:
                idEnd = anchor['href'].find("?")
                roomId = anchor['href'][7:idEnd]
                int(roomId)
                roomIds.update([roomId])
        if len(roomIds) == 0:
            break
        totalRooms+=len(roomIds)
        roomUrls = ["https://www.airbnb.com/rooms/"+x for x in roomIds]

        #Multithreaded way: Do not use this, will get your IP added to airbnb's temporary blacklist :(
        #if you do want to use this, move the selenium driver instantiation and garbage collection within the thoroughReviewAnalysis method 
        '''pool = ThreadPool(5)
        if mode == "quick":
            results = pool.map(quickReviewAnalysis,roomUrls)
        else:
            results = pool.map(thoroughReviewAnalysis,roomUrls)
        pool.close() 
        pool.join()'''
        
        #Single threaded alternative:
        if mode == "quick":
            results = [quickReviewAnalysis(url) for url in roomUrls]
        else:
            driver = webdriver.Chrome()
            results = [thoroughReviewAnalysis(url,driver) for url in roomUrls]
            driver.close()

        goodUrls += [url for url in results if url != None]
        i += 1
    print "Total rooms scanned: ",str(totalRooms) 
    return goodUrls

# ./greatViews.py <quick | thorough> <minPrice> <maxPrice> <url>
if __name__ == "__main__":
    mode = "thorough" if sys.argv[1] == "thorough" else "quick"
    [minPrice,maxPrice,url] = sys.argv[2:5]
    goodUrls = greatViews(url,mode,minPrice,maxPrice,KEYWORDS)
    print "Results:"
    for url in goodUrls:
        print url

