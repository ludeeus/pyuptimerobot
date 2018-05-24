"""
A python module to monitor Uptime Robot monitors.
This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import requests

class UptimeRobot:
    """This class is used to get information from Uptime Robot."""
    BASE_URL = 'https://api.uptimerobot.com/v2/'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def __init__(self):
        """Initialize"""
    def getMonitors(self, apikey):
        """Get departure info from stopid."""
        data= 'api_key=' + apikey + '&format=json'
        fetchUrl = self.BASE_URL
        fetchUrl += 'getMonitors'
        monitors = requests.post(fetchUrl,
            headers=self.headers, data=data).json()
        return monitors