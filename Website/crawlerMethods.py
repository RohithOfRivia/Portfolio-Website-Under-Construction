import requests
from bs4 import BeautifulSoup
import re
import time


def attributeFinder(soup):
    attrs = []
    attrDict = {}
    attrDict['bedRooms'] = 'NA'
    attrDict['bathRooms'] = 'NA'
    attrDict['size'] = 'NA'

    # target_details = soup.find(id="mainPageContent")

    # size_rooms = soup.find(id="vip-body")
    # size_rooms = soup.find(id="AttributeList")

    size_rooms = soup.find_all("dd")
    size_rooms = list(size_rooms)

    for attribute in size_rooms:
        #         print(str(attribute))
        attrs.append(re.findall('">(.*?)</', str(attribute)))

    if len(attrs) > 0:

        attrs = [item for sublist in attrs for item in sublist]

        i = 0
        for feature in attrs:

            if feature == '':
                continue

            if i == 0:
                attrDict['bedRooms'] = attrs[0]
                i += 1

            elif i == 1:
                attrDict['bathRooms'] = attrs[1]
                i += 1

            elif i == 2:
                attrDict['size'] = attrs[2]
                i += 1

        #         print(attrDict)
        return attrDict

    else:
        return 'NO'


def priceFinder(soup):
    priceSearch = soup.find_all("span")
    price = []

    for item in priceSearch:
        price = re.findall('\$(.*?)</', str(priceSearch))

    if len(price) > 0:
        price = price[0]
        print(f"Fetched price: {price}")
        return (price)

    else:
        # print("No Price Listed")
        return 0


def addressFinder(soup):
    addressSearch = str(soup.find(id="ViewItemPage"))
    address = re.findall('itemprop="address"(.*?)</sp', str(addressSearch))
    if len(address) > 0:
        address = address[0].strip()
        address = address.split(">")[1]

        #         print(address)
        return address

    else:
        return 'NA'


def descFinder(soup):
    desc = soup.find("p").string
#     print(desc)
    return desc


def crawler(startingLink):
    page = requests.get(startingLink)
    soup = BeautifulSoup(page.content, 'html.parser')

    nextPage = ''
    print("starting at " + startingLink)

    while True:


        # nextPage = True
        movePage = soup.find('a', {'title': "Next"}).get("href")[:-11]
        newLink = "https://www.kijiji.ca" + movePage


        if nextPage != '':

            print(f"Finished current page. Currently trying to navigate to: {newLink}\n")
            movePage = requests.get(newLink)
            soup = BeautifulSoup(movePage.content, 'html.parser')
            print("NEXT PAGE SUCCESS\n")

        links = soup.find_all("a")
        listings = []

        for link in links:
            if 'class="title"' in str(link):
                #         print(str(link))
                hit = re.findall('href="(.*?)"', str(link))
                listings.append(hit)

        listings = [item for sublist in listings for item in sublist]

        for listing in listings:
            listingDetails = {}

            print("Scraping through : ")

            url = "http://kijiji.ca" + listing
            print(url)

            currentPage = requests.get("http://kijiji.ca" + listing)

            print("request success")

            Currentsoup = BeautifulSoup(currentPage.content, 'html.parser')

            listingDetails['url'] = url

            listingDetails['attrDict'] = attributeFinder(Currentsoup)

            listingDetails['price'] = priceFinder(Currentsoup)

            listingDetails['address'] = addressFinder(Currentsoup)

            listingDetails['desc'] = descFinder(Currentsoup)

            listingDetails['newLink'] = newLink

            nextPage = True

            yield listingDetails

            print("\nLOADING NEXT LISTING...\n")

            time.sleep(6)


