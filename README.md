# pyruter - A module to get information about the next departure from a stop.

#### Notes
This has been tested with python 3.6  
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
ur = UptimeRobot()

#Get deperture information:
result = ur.getMonitors(apikey)

#Print the result:
print(result)
```