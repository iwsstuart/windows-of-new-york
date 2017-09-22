import json
import requests
import googlemaps
import settings
import string
from bs4 import BeautifulSoup

class Scraper:

    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)

    def scrape(self):
        windows = []
        request = requests.get('http://www.windowsofnewyork.com/')
        html = request.text
        soup = BeautifulSoup(html)
        windows_markup = soup.findAll('div', { "class" : "window" })
        for idx, window_html in enumerate(windows_markup[:5]):
            window_soup = BeautifulSoup(str(window_html), "html.parser")
            image_url = window_soup.find("img")
            if image_url:
                image_url = "http://windowsofnewyork.com/" + image_url['src']
            address = window_soup.find("div", {'class': 'address'})
            if address:
                address = address.getText()
                address = filter(lambda x: x in string.printable, address).strip()
            neighborhood = window_soup.find("div", {'class': 'neighborhood'})
            if neighborhood:
                neighborhood = neighborhood.getText()
            geocode_result = self.gmaps.geocode("%s %s new york city" % (address, neighborhood)) # search for "{{ address }} {{ neighborhood }} new york city"
            print geocode_result
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            formatted_address = geocode_result[0]['formatted_address']
            if image_url and address and neighborhood and lat and lng and formatted_address:
                window = json.dumps({'image_url': image_url, 'address': address, 'neighborhood': neighborhood, 'lat': lat, 'lng': lng, 'formatted_address': formatted_address})
                windows.append(window)
            print '%s of %s complete' % (idx, len(windows_markup) - 1)
        with open('windows.json', 'w') as f:
            json.dump(windows, f)
        # return windows

Scraper().scrape()
