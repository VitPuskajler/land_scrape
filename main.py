import os
from dotenv import load_dotenv
from property_scrapers.bazos_scrape import SearchEngine as bazos
from property_scrapers.reality_scrape import SearchEngine as reality
from property_scrapers.topreality_scrape import SearchEngine as topreality
from email_sender.email_sender import EmailSender as sender

load_dotenv(r".\credentials\mail.env")

EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")

bazos_search = bazos()
reality_search = reality()
topreality_search = topreality()

s = sender()

# All these URLs are with applied filter, it is simple as it looks. Filter out what you like in the website andcopy the link.

bazos_url = "https://reality.bazos.sk/predam/pozemok/?hledat=&rubriky=reality&hlokalita=97401&humkreis=10&cenaod=&cenado=&Submit=H%C4%BEada%C5%A5&order=&crp=&kitx=ano"
# Important is part two, this one can be incremented +10 and ti will act as clicking on "nex page"
bazos_next_page_part_one = "https://reality.bazos.sk/predam/pozemok/"
bazos_next_page_part_two = 20
bazos_next_page_part_three = "/?hledat=&rubriky=reality&hlokalita=97401&humkreis=10&cenaod=&cenado=&Submit=H%C4%BEada%C5%A5&order=&crp=&kitx=ano"

reality_url = "https://www.reality.sk/pozemky/banska-bystrica/predaj/?price_to=100000&order=created_date-newest"
topreality_url = "https://www.topreality.sk/vyhladavanie-nehnutelnosti.html?form=1&type%5B%5D=802&obec=1997&searchType=string&distance=&q=&cena_od=&cena_do=100000&vymera_od=0&vymera_do=0&n_search=search&page=estate&gpsPolygon="
topreality_nexpage_part_one = "https://www.topreality.sk/vyhladavanie-nehnutelnosti-"
topreality_nexpage_part_two = 2
topreality_nexpage_part_three = ".html?type%5B0%5D=802&form=1&obec=1997&cena_do=100000&n_search=search&gpsPolygon=&searchType=string"

def bazos_scrape():
    bazos_ads = bazos_search.lands_for_last_day(bazos_url, bazos_next_page_part_one,bazos_next_page_part_two,bazos_next_page_part_three)
    return bazos_search.each_ad_scrape(bazos_ads)

def reality_scrape():
    reality_ads = reality_search.lands_for_last_day(reality_url)
    return reality_search.each_ad_scrape(reality_ads)

def topreality_scrape():
    topreality_ads = topreality_search.lands_for_last_day(topreality_url, topreality_nexpage_part_one, topreality_nexpage_part_two, topreality_nexpage_part_three)
    return topreality_search.each_ad_scrape(topreality_ads)

bazos_data = bazos_scrape()
reality_data = reality_scrape()
topreality_data = topreality_scrape()

mail_body = s.table_create(bazos_data, reality_data, topreality_data)
s.send_email(mail_body, EMAIL, PASS)