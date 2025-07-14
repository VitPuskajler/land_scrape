import requests
from bs4 import BeautifulSoup
import re
import datetime
import time # Don't overwhelm websites and wait for a couple of seconds before doing another request

class SearchEngine():
    def __init__(self):
        # Save data from bazos
        self.name = "Reality - land for a house (SK)"
        self.website = "Reality"
        self.url_base = "https://www.reality.sk"

    # Return links for all 
    def lands_for_last_day(self, url)->dict:
        self.scrape_next_page = False
        self.ads = []
        self.next_page = 2

        if url:
            self.r = requests.get(url)
            self.r.raise_for_status()
            self.soup = BeautifulSoup(self.r.content, "html.parser")
            # Each ad is in inzeraty flex box so it is simple to search through it
            self.content = self.soup.find_all("div", class_="offer no-gutters")
            # Today's date -> so I am scraping only today's ads
            self.today = datetime.datetime.now()
            self.reality_format_date = self.today.strftime("%d.%m.%Y") # D.M.Y 

            # Add do self.ads all today's 
            for ad in self.content:
                date = ad.find('span', class_="offer-date")
                href = ad.find("a", href=True)
                if date:
                    strip_date = date.contents[-1].strip('Publikované: ')
                    if str(strip_date) == str(self.reality_format_date):
                        full_link_format = f"{self.url_base}{href.get("href")}"
                        self.ads.append(full_link_format)


            # If last value of ad has today's date -> scrapre next page
            if strip_date == self.reality_format_date:
                while self.scrape_next_page != True:
                    self.request_url = str(f"{url}&page={self.next_page}")
                    self.r = requests.get(self.request_url)
                    self.r.raise_for_status()
                    self.soup = BeautifulSoup(self.r.content, "html.parser")
                    self.content = self.soup.find_all("div", class_="offer no-gutters")

                    for ad in self.content:
                        date = ad.find('span', class_="offer-date")
                        href = ad.find("a", href=True)
                        if date:
                            strip_date = date.contents[-1].strip('Publikované: ')
                            if str(strip_date) == str(self.reality_format_date):
                                full_link_format = f"https://www.reality.sk{href.get("href")}"
                                self.ads.append(full_link_format)

                    if strip_date == self.reality_format_date:
                        self.next_page += 1
                    else:
                        self.scrape_next_page = True
                    
                    time.sleep(2) # Let's not kill the website with our requests -> and I don't like to be banned either

        return self.ads

    # Scrape each ad and return data in disctionary which can be later stored in database
    def each_ad_scrape(self, links:list)->list[dict]:
        self.output = []
        if links:
            for i, link in enumerate(links):
                self.data = {"Title": None, "Photo": None, "Description": None, "Price":None, "Source": None}
                self.r = requests.get(link)
                self.r.raise_for_status()
                self.soup = BeautifulSoup(self.r.content, "html.parser")

                # Extract: Photo links, Title, Description, Price
                self.photo = (self.soup.find("img", class_="js-lazy mx-auto d-block img-fluid")).get("data-lazy-src")

                # Title
                self.title = self.soup.find("h1", class_="detail-title pt-4 pb-2").get_text()
                # Description
                self.description = self.soup.find("span", class_="content-preview").get_text()
                # Price
                self.price = f"{self.soup.find("h3", class_="contact-title big").get_text().split("€")[0]}€" # Find all tags because other options is not working thanks to <br>

                link = f"{self.url_base}{link}"

                self.data["Title"]=self.title
                self.data["Photo"]=self.photo
                self.data["Description"]=self.description
                self.data["Price"]=self.price
                self.data["Source"]=link

                self.output.append(self.data)
        
        return self.output