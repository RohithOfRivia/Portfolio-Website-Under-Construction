import requests
from bs4 import BeautifulSoup
import re
import time
import pymongo
import crawlerMethods
from dotenv import load_dotenv
import os

load_dotenv()

client = pymongo.MongoClient(f"mongodb+srv://{os.getenv('MONGO_KEY')}@projects.1qkvd5p.mongodb.net/test")
db = client.KijijiCrawler
houses = db['House Listings']

repeats = 0
startingLink = "https://www.kijiji.ca/b-house-for-sale/gta-greater-toronto-area/page-50/c35l1700272"
Stopper = 0

def startScrape(startingLink, interrupted):


    counter = 0

    while (counter <= 2):

        if Stopper == True:
            return

        if interrupted:
            return

        repeats = 0
        for listing in (crawlerMethods.crawler(startingLink)):


            try:

                row = {}
                row["_id"] = listing['url']
                row["price"] = listing['price']
                row["desc"] = listing['desc']
                row["address"] = listing['address']
                row["bedRooms"] = listing['attrDict']['bedRooms']
                row["bathRooms"] = listing['attrDict']['bathRooms']
                row["size"] = listing['attrDict']['size']

                newLink = listing['newLink']

                insert = houses.insert_one(row)
                print("Insert Success!", row)

            except pymongo.errors.DuplicateKeyError:
                counter += 1
                if counter > 2:
                    break
                print("\nDuplicate Insertion, moving to next listing")
                repeats += 1

                # if (repeats > 3):
                #     print("""Probably scraped everything in this page. Moving to:
                #     """ + newLink)
                #     repeats = 2
                #
                #     crawlerMethods.crawler(newLink)

                continue

            except Exception:
                print("\n\nRequest attempts likely exceeded, waiting for a minute...\n")
                time.sleep(60)


        for i in (crawlerMethods.crawler("https://www.kijiji.ca/b-house-for-sale/gta-greater-toronto-area/c35l1700272")):
            print(i)
            counter += 1
            if counter > 2:
                break

# startScrape("https://www.kijiji.ca/b-house-for-sale/gta-greater-toronto-area/page-50/c35l1700272", False)

