import json
import urllib.request
from urllib.error import URLError
import logging
import private

def graphhoppercall(geotag, station) :
    logging.info("graphhoppercall(geotag, station) - Starting")
    try :
        APICall = urllib.request.urlopen('https://graphhopper.com/api/1/route?point=' + str(geotag[0])+'%2C' + str(geotag[1])+'&point='+ str(station[0])+'%2C' + str(station[1])+ '&vehicle=foot&locale=en&key=' + str(private.graphhopper_key))
    except URLError:
        logging.warning("graphhoppercall(geotag, station) - No internet or too many api call")
        logging.info("graphhoppercall(geotag, station) - Ending w/ error")
        return "NO INTERNET"


    text = APICall.read().decode("utf-8")
    decoded = json.loads(text)

    distance = int(decoded["paths"][0]["distance"])
    time = int(decoded["paths"][0]["time"]/1000)/60

    logging.info("graphhoppercall(geotag, station) - Ending")
    return(distance,time)

#graphhoppercall([48.8864837, 2.3447296], [48.865384, 2.374603])
#https://graphhopper.com/dashboard/#/overview