"""
Helsinki Weather Widget
Written by Arto Vuori
License: Public Domain
"""

import urllib2
from xml.dom import minidom

class Weather:
    DATA_SRC = "http://weather.yahooapis.com/forecastrss?w=565346&u=c"

    def __init__(self, condition, wind, image, astronomy):
        self.condition = condition
        self.wind = wind
        self.image = image
        self.astronomy = astronomy

    def get_temperature(self):
        return self.condition[1]

    def get_wind_chill(self):
        return self.wind[0]

    def get_wind_speed(self):
        return "%.2f" % float(float(self.wind[1])*1000/3600)

    def get_description(self):
        return self.condition[0]

    def get_timestamp(self):
        return self.condition[2]

    def get_time(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M")

    def get_image(self):
        return self.image

    def get_sunrise(self):
        return self.astronomy[0]

    def get_sunset(self):
        return self.astronomy[1]

    def render_html(self):
        return """<html>
<head>
<meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8" />
<meta http-equiv="refresh" content="900" />
<title>Weather Helsinki Now</title>
<link href="style.css" rel="stylesheet" type="text/css">
</head>
<body>
<img src="%s" alt="%s" />
<em>%s.</em><br />
<b>%s</b> &deg;C.<br />
Wind speed is %s m/s, chill is %s &deg;C.<br />
Sunrise at %s.<br />
Sunset at %s.<br /><br />
Updated at %s.
</body>
</html>
        """ % (self.get_image(),
               self.get_description(),
               self.get_description(),
               self.get_temperature(),
               self.get_wind_speed(),
               self.get_wind_chill(),
               self.get_sunrise(),
               self.get_sunset(),
               self.get_time())
    
def fetch():
    return urllib2.urlopen(Weather.DATA_SRC).read()


def parse(s):
    return minidom.parseString(s)


def make_weather_object(document):
    
    yweather_ns_uri = "http://xml.weather.yahoo.com/ns/rss/1.0"

    def get_el_ns(ns, el_name, nth=0):
        return document.getElementsByTagNameNS(ns, el_name)[nth]
    
    def get_el(el_name, nth=0):
        return document.getElementsByTagName(el_name)[nth]

    def get_condition():
        el = get_el_ns(yweather_ns_uri, "condition")    
        return el.getAttribute("text"),\
               el.getAttribute("temp"),\
               el.getAttribute("date")

    def get_wind():
        el = get_el_ns(yweather_ns_uri, "wind")    
        return el.getAttribute("chill"),\
               el.getAttribute("speed")

    def get_image():
        import re
        d = get_el("description", 1)
        m = re.search('<img src="([^"]+)"', d.firstChild.nodeValue)
        return m.group(1)

    def get_astronomy():
        el = get_el_ns(yweather_ns_uri, "astronomy")
        return el.getAttribute("sunrise"),\
               el.getAttribute("sunset")

    return Weather(get_condition(),
                   get_wind(),
                   get_image(),
                   get_astronomy())



if __name__ == "__main__":
    w = make_weather_object(parse(fetch()))
    print w.render_html()
    
