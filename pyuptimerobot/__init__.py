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

    def getMonitors(self, apikey, monitors='none'):
        """Get departure info from stopid."""
        data= 'api_key=' + apikey + '&format=json'
        if monitors != 'none':
            data += '&monitors=' + monitors
        fetchUrl = self.BASE_URL
        fetchUrl += 'getMonitors'
        try:
            monitors = requests.post(fetchUrl,
                headers=self.headers, data=data, timeout=3)
        except:
            return False
        else:
            if monitors:
                return monitors.json()
            else:
                return False