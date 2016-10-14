import config
import xml.etree.ElementTree as ET
import urllib.request
from immobilier import Annonce
from urllib.error import URLError
from xml.etree.ElementTree import ParseError
import logging

#this function generates an Annonce object from a listing on the Se Loger web service
def annonceGenerator(element) :

    #get the following

    idAnnonce = element.find('idAnnonce').text
    if idAnnonce == None :
        print("annonceGenerator(element) - NoID")
        return "NO ID"
    dtCreation = element.find('dtCreation').text
    price = float(element.find('prix').text)
    priceUnite = element.find('prixUnite').text
    try :
        surface = float(element.find('surface').text)
    except AttributeError:
        surface = 1
    nbPiece = int(element.find('nbPiece').text)
    try:
        nbChambre =  int(element.find('nbChambre').text)
    except AttributeError:
        nbChambre = None

    descriptif = element.find('descriptif').text
    codePostal = int(element.find('cp').text)
    permaLien = element.find('permaLien').text
    geotag =(float(element.find('latitude').text), float(element.find('longitude').text))
    try :
        bilanConsoEnergie = element.find('bilanConsoEnergie').text
    except AttributeError :
        bilanConsoEnergie = None
    typologie = element.find('siLotNeuf').text
    try:
        nbPhotos = int(element.find('nbPhotos').text)
    except TypeError :
        nbPhotos = 0
    #trouver l'élément contact
    contact = element.find('contact')
    #itérer l'élément contact
    for child in range(len(contact) - 1):
        #Si le tag rcs existe
        if contact[child].tag == 'rcsSiren':
            #le text devient une des carac de l'annonce
            rcsSirenAgence = contact[child].text
        else:
            #sinon, la carac est None
            rcsSirenAgence = None
        # Si le tag Nom existe
        if contact[child].tag == 'nom':
            # le text devient une des carac de l'annonce
            nomAgence = contact[child].text
        else:
            nomAgence = None
    #s'il y a des photos
    if nbPhotos > 0:
        #initialiser une liste
        photo = []
        #dans la liste des photos
        photosList = element.find('photos')
        #pour item
        for item in range(len(photosList) - 1):
            #si c'est une photo
            if photosList[item].tag == 'photo':
                photoItem = photosList[item]
                #trouver la standard URL et l'ajouter à la liste
                for carac in range(len(photoItem) - 1):
                    if photoItem[carac].tag == 'stdUrl':
                        photoUrl = photoItem[carac].text
                        photo.append(photoUrl)
    else:
        photo = None
    #and create an Annonce object with all these elements
    nodeAnnonce = Annonce(idAnnonce, dtCreation, price, priceUnite, surface, nbPiece, nbChambre, descriptif, codePostal, permaLien, geotag, bilanConsoEnergie, nbPhotos, nomAgence, rcsSirenAgence, photo, typologie)

    return nodeAnnonce

#this function constructs the URL to query the webservice
#Input : config file
#output : URL as a string
def url_immo() :

    return "url to get the listings (through config)"

#this function requests the xml that is behing the Seloger URL
#output : XML string
def xml_immo(url) :
    logging.info("xml_immo(url) - Starting")
    try:
        xml = urllib.request.urlopen(url).read()
        logging.info("xml_immo(url) - Ending")
        return xml
    except URLError:
        logging.error("xml_immo(url) - No internet")
        logging.info("xml_immo(url) - Ending w/ error")
        return "NO INTERNET"


def ListingsPresentGeneratorSL():
    logging.info("ListingsPresentGeneratorSL() - Starting")
    #create the fist page XML
    url = url_immo()
    xml = xml_immo(url)

    if xml == "NO INTERNET" :
        logging.error("ListingsPresentGeneratorSL - No internet")
        logging.info("ListingsPresentGeneratorSL() - Ending w/ error")
        return "NO INTERNET"
    listOfPresent = []


    # parse the XML
    try :
        root = ET.fromstring(xml)

    except ParseError :
        logging.error("ListingsPresentGenerator - XML cannot be parsed")
        logging.info("ListingsPresentGeneratorSL() - Ending w/ error")
        return "NO LISTING"
    for element in root.iter("annonce"):
        # create an annonce
        annonce = annonceGenerator(element)
        #if annonce does not have a unique ID
        if annonce == "NO ID":
            pass
        else :
            listOfPresent.append(annonce)
    #get the max page of listings

    pageMax = 0
    for element in root.iter("pageMax") :
        pageMax = int(element.text)
    #if there is more than 1
    if pageMax > 1 :
        for i in range(pageMax -1 ) :
            url = "url search schema"
            xml = xml_immo(url)
            root = ET.fromstring(xml)
            for element in root.iter("annonce"):
                # create an annonce
                annonce = annonceGenerator(element)
                if annonce == "NO ID" :
                    pass
                else :
                    listOfPresent.append(annonce)
    #if the list is empty
    if len(listOfPresent) == 0:
        logging.error('ListingsPresentGenerator - No listings')
        logging.info("ListingsPresentGeneratorSL() - Ending w/ error")
        return "NO LISTING"
    logging.info("ListingsPresentGeneratorSL() - Ending")
    return listOfPresent
