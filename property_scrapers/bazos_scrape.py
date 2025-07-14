import requests
from bs4 import BeautifulSoup
import datetime
import time  # Don't overwhelm websites and wait for a couple of seconds before doing another request


class SearchEngine:
    def __init__(self):
        # Save data from bazos
        self.name = "Bazos - land for a house (SK)"
        self.website = "Bazos"
        self.link_prefix = "https://reality.bazos.sk"

    # Return links for all
    def lands_for_last_day(
        self, url, url_part_one, url_part_two, url_part_three
    ) -> dict:
        self.scrape_next_page = False
        self.ads = []
        self.request_url = f"{url}"
        self.r = requests.get(self.request_url)
        self.r.raise_for_status()
        self.soup = BeautifulSoup(self.r.content, "html.parser")
        # Each ad is in inzeraty flex box so it is simple to search through it
        self.content = self.soup.find_all("div", class_="inzeraty inzeratyflex")
        # Today's date -> so I am scraping only today's ads
        self.today = datetime.datetime.now()
        self.bazos_format_date = self.today.strftime("%#d.%#m. %Y")  # D.M.Y

        # Add do self.ads all today's
        for ad in self.content:
            date = ad.find("span", class_="velikost10")
            href = ad.find("a", href=True)
            if date:
                strip_date = date.contents[-1].strip("- []")
                if str(strip_date) == str(self.bazos_format_date):
                    full_link_format = f"{self.link_prefix}{href.get("href")}"
                    self.ads.append(full_link_format)

        # If last value of ad has today's date -> scrapre next page
        if strip_date == self.bazos_format_date:
            while self.scrape_next_page != True:
                self.next_page_url = f"{url_part_one}{url_part_two}{url_part_three}"
                self.request_url = f"{self.next_page_url}"
                self.r = requests.get(self.request_url)
                self.r.raise_for_status()
                self.soup = BeautifulSoup(self.r.content, "html.parser")
                self.content = self.soup.find_all("div", class_="inzeraty inzeratyflex")

                for ad in self.content:
                    date = ad.find("span", class_="velikost10")
                    href = ad.find("a", href=True)
                    if date:
                        strip_date = date.contents[-1].strip("- []")
                        if str(strip_date) == str(self.bazos_format_date):
                            full_link_format = f"{self.link_prefix}{href.get("href")}"
                            self.ads.append(full_link_format)

                if strip_date == self.bazos_format_date:
                    url_part_two += 10
                else:
                    self.scrape_next_page = True

                time.sleep(
                    2
                )  # Let's not kill the website with our requests -> and I don't like to be banned either

        return self.ads

    # Scrape each ad and return data in disctionary which can be later stored in database
    def each_ad_scrape(self, links: list) -> list[dict]:
        self.output = []
        if links:
            for i, link in enumerate(links):
                self.data = {
                    "Title": None,
                    "Photo": None,
                    "Description": None,
                    "Price": None,
                    "Source": None,
                }
                self.r = requests.get(link)
                self.r.raise_for_status()
                self.soup = BeautifulSoup(self.r.content, "html.parser")

                # Extract: Photo links, Title, Description, Price
                self.photo_all = self.soup.find_all("img")
                self.photo = []
                for p in self.photo_all:
                    if "src" in p.attrs:
                        self.photo.append(p["src"])

                # Title
                self.title = self.soup.find("h1", class_="nadpisdetail").get_text()
                # Description
                self.description = self.soup.find(
                    "div", class_="popisdetail"
                ).get_text()
                # Price
                self.price_rel_tags = self.soup.find_all(
                    "td"
                )  # Find all tags because other options is not working thanks to <br>
                self.price_spec_tag = None
                self.price = None

                for td in self.price_rel_tags:
                    if "Cena:" in td:
                        self.price_spec_tag = td
                        break

                if self.price_spec_tag:
                    price_value_tag = self.price_spec_tag.find_next_sibling("td")
                    if price_value_tag:
                        self.price = price_value_tag.get_text(strip=True)

                self.data["Title"] = self.title
                self.data["Photo"] = self.photo
                self.data["Description"] = self.description
                self.data["Price"] = self.price
                self.data["Source"] = link

                self.output.append(self.data)

        return self.output
