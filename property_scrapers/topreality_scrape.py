import requests
from bs4 import BeautifulSoup
import datetime
import time # Don't overwhelm websites and wait for a couple of seconds before doing another request

class SearchEngine():
    def __init__(self):
        # Save data from bazos
        self.name = "TOP Reality - land for a house (SK)"
        self.website = "TOP Reality"
        self.url_base = "https://www.topreality.sk/"

    # Return links for all 
    def lands_for_last_day(self, url, url_p_one, url_p_two, url_p_three)->dict:
        self.scrape_next_page = False
        self.ads = []
        if url:
            self.request_url = f"{url}"
            self.r = requests.get(self.request_url)
            self.r.raise_for_status()
            self.soup = BeautifulSoup(self.r.content, "html.parser")
            # Each ad is in inzeraty flex box so it is simple to search through it
            self.content = self.soup.find_all("div", class_="card-info card-info-left align-self-sm-center w-100")
            # Today's date -> so I am scraping only today's ads
            self.today = datetime.datetime.now()
            self.topreality_format_date = self.today.strftime("%#d.%#m.%Y") # D.M.Y 

            # Add do self.ads all today's 
            for ad in self.content:
                date = ad.find('li', class_="date")
                href = ad.find("a", href=True)
                if date:
                    strip_date = date.get_text(strip=True)
                    if str(strip_date) == str(self.topreality_format_date):
                        self.ads.append(href.get("href"))


            # If last value of ad has today's date -> scrapre next page
            if strip_date == self.topreality_format_date:
                while self.scrape_next_page != True:
                    self.request_url = str(f"{url_p_one}{url_p_two}{url_p_three}")
                    self.r = requests.get(self.request_url)
                    self.r.raise_for_status()
                    self.soup = BeautifulSoup(self.r.content, "html.parser")
                    self.content = self.soup.find_all("div", class_="card-info card-info-left align-self-sm-center w-100")

                    validator = 0
                    for ad in self.content:
                        date = ad.find('li', class_="date")
                        href = ad.find("a", href=True)
                        if date:
                            strip_date = date.get_text(strip=True)
                            if str(strip_date) == str(self.topreality_format_date):
                                self.ads.append(href.get("href"))
                        validator += 1

                    if strip_date == self.topreality_format_date and validator > 2:
                        url_p_two += 1
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
                self.price = None

                # Extract: Photo links, Title, Description, Price
                """ self.photo_all = self.soup.find("img", id="galleryImageHero").get("src")[-1]
                self.photo_link = f"{self.url_base}{self.photo_all}"
                self.photo = []
                self.photo.append(self.photo_link) """
                # BS4 is unable to wait for JS and I don't want to import SELENIUM just for this -> I will be fine with custom image 
                self.photo = []
                self.photo.append("https://arbtech.co.uk/wp-content/uploads/2021/10/land-for-sale-rural-landscape.jpg.webp")
                 
                # Title
                self.title = self.soup.find("h1", class_="h2 pt-2").get_text(strip=True)
                # Description
                self.description = self.soup.find("div", class_="description").get_text(strip=True)
                # Price
                self.price_container = self.soup.find("li", class_="priceContainer")

                if self.price_container:
                    self.price_tag = self.price_container.find("strong", class_="price")
                    if self.price_tag:
                        self.price = self.price_tag.get_text(strip=True)

                self.data["Title"]=self.title
                self.data["Photo"]=self.photo
                self.data["Description"]=self.description
                self.data["Price"]=self.price
                self.data["Source"]=link

                self.output.append(self.data)
        
        return self.output