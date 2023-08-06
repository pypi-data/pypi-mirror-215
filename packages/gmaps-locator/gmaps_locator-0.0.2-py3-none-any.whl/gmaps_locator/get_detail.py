"""
This module using request-html to search through google maps and return coordinate from specific address.

Author: Akbar Tolandy
Linkedin: https://www.linkedin.com/in/akbar-tolandy-32a949a4/
"""

__author__ = "Akbar Tolandy, NeuralNine"
__email__ = "akbartolandy@gmail.com"
__status__ = "Beta"

from requests_html import HTMLSession

class GetCoord:
    def __init__(self):         
        self.session = HTMLSession()

    def get_latlon(self, address):
        url_map = f"http://www.google.com/maps/search/{address}"
        
        try:
            req_map = self.session.get(url_map, allow_redirects=True)
            location = req_map.html.find('meta[property="og:image"]', first=True).attrs['content']            
        except:
            print('location not found')
            location = ''

        try:
            lat_lon = location.split('&markers=')[1].split('%7C')[0].split('%2C')
            lat, lon = lat_lon[0], lat_lon[1]
        except:
            try:
                lat_lon = location.split('center=')[1].split('&zoom')[0].split('%2C')
                lat, lon = lat_lon[0], lat_lon[1]
            except:
                print("Coordinate not found!!! recheck your address")
                lat, lon = '', ''

        coord = {'lat':lat, 'lon':lon}
        return coord            
