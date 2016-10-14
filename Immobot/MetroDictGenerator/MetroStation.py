#this transform the XML of station into a dict file
# get the distance to the metro https://www.data.gouv.fr/fr/datasets/stations-et-gares-de-metro-rer-et-tramway-de-la-region-ile-de-france/

#opens a dictMetroStation file
#copies the file into it

import xml.etree.ElementTree as ET
import pickle

distance = 0.005

#output dictMetro[name] = {"name": name, "geotag": [latitude, longitude], "bbox":
def GenerateDictMetro(distance) :
    #index error
    urlMetro = "metrogps.xml"
    treeMetro = ET.parse(urlMetro)
    rootMetro = treeMetro.getroot()

    #create Dict
    dictMetro = {}

    #for each metro station node
    for element in rootMetro.iter("node") :
        # get the name of the metro station
        for line in element:
            if line.attrib['k'] == "name":
                name = line.attrib['v']
        # The lagitude and longitude
        latitude = float(element.attrib["lat"])
        longitude = float(element.attrib["lon"])
        # create dictionary entry with Borderbox top right and bottom left
        #bbox are boxes of O.O3 around GPS to appoximate 300m
        # coordinate distance calculator http://boulter.com/gps/distance/?from=48.82%2C+2.36&to=48.8225%2C2.36&units=k
        ## Long : 300m == +/- 0.0025 -- https://en.wikipedia.org/wiki/Decimal_degrees
        ## Lat : 300m == +/- 0.0025
        dictMetro[name] = {"name": name, "geotag": [latitude, longitude], "bbox": [[latitude + distance, longitude + distance], [latitude - distance, longitude - distance]]}

    return dictMetro
def dictFileUpdater(dict, File) :
    output = open(File, 'w')
    output.close()
    output = open(File, 'ab+')
    pickle.dump(dict, output)
    output.close()
    print ("file updated")


dictMetro = GenerateDictMetro(distance)
dictFileUpdater(dictMetro, 'dictMetroStation.txt')