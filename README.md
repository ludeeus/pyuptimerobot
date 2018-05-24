# pyuptimerobot - A python module to monitor Uptime Robot monitors.

#### Notes
This has been tested with python 3.6  
This module require an API key from Uptime Robot.
This module uses these external libararies:
- requests

#### Install
```bash
pip install pyuptimerobot
```

#### Usage:
```python
from pyuptimerobot import UptimeRobot

apikey = 'u432898-d2507e493b31217e6c64fd35'
monitor = '1527172614' #optional
ur = UptimeRobot()

#Get monitor information:
result = ur.getMonitors(apikey, monitor)

#Print the result:
print(result)
```