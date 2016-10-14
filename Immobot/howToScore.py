import config
import CalltoGraphhopperAPI
import dictFunctions
import logging

#this function tells you if the gps location (coords) belong in a geographical box (box)
#input : gps coodinates as tuple and a box as a list of 2 tuples : top right annd bottom left
#output : bolean
def in_box(coords, box):
    logging.info("in_box(coords, box) - Starting")
    if box[0][0] > coords[0] > box[1][0] and box[0][1] > coords[1] > box[1][1]:
        logging.info("in_box(coords, box) - Ending")
        return True
    logging.info("in_box(coords, box) - Ending")
    return False

#this function returns False is annonce should be vetoed based on config
def AnnonceTobeVetoed(annonce) :
    logging.info("AnnonceTobeVetoed(annonce) - Starting")
    # Take out the VETO elements qui mont la qualité de veto
    if annonce.prix > config.priceMaxGoal or annonce.prix < config.priceMinGoal:
        logging.warning("AnnonceTobeVetoed(annonce) - Ending with veto on Price" + str(annonce))
        return False
    if annonce.surface < config.sizeMinGoal or annonce.surface > config.sizeMaxGoal:
        logging.warning("AnnonceTobeVetoed(annonce) - Ending with veto on Surface" + str(annonce))
        return False
    if annonce.codePostal not in config.codePostalGoal:
        logging.warning("AnnonceTobeVetoed(annonce) - Ending with veto on Zip Code" + str(annonce))
        return False
    else :
        return True

#this function calculates how far away from a metro station a listing is
def distanceFromMetro(dictMetro, annonce):
    logging.info("scoringFunc(annonce) - Get the DictMetro")
    dictMetro = dictFunctions.dictInitialization('dictMetroStation.txt')
    # def Distancedumetro
    for station in dictMetro:
        # if the annonce is in the vicinity of a metro station
        if in_box(annonce.geotag, dictMetro[station]['bbox']) == True:
            # get the name of the station
            thisStation = dictMetro[station]['name']
            # Get the distance between the metro station
            howFarHowLong = CalltoGraphhopperAPI.graphhoppercall(annonce.geotag, dictMetro[station]['geotag'])
            #if you cannot connect to Graphhopper
            if howFarHowLong == "NO INTERNET":
                annonce.stations.append([thisStation, None, None])
                logging.info("scoringFunc(annonce) - Ending w/ error")
                return False
            else:
                howFar = howFarHowLong[0]
                howLong = howFarHowLong[1]
                annonce.stations.append([thisStation, howFar, howLong])

    logging.info("scoringFunc(annonce) - Ending w/ error")
    annonce.stations = sorted(annonce.stations, key=lambda x: x[1])
    return True

def scoring(annonce) :
    logging.info("scoringFunc(annonce) - Starting")

    prixMetreCarreOriginal = annonce.prix / annonce.surface

    # Nice to Have

    prixPondere = annonce.prix
    if annonce.nbPiece == config.nbPiece[0]:
        prixPondere -= config.nbPiece[1]
    if annonce.nbChambre == config.nbChambre[0]:
        prixPondere -= config.nbChambre[1]
    if annonce.bilanConsoEnergie == config.bilanConsoEnergie[0]:
        prixPondere -= config.bilanConsoEnergie[1]
    if annonce.typologie == config.typologie[0]:
        prixPondere -= config.typologie[1]

    # test si le quartier correspond aux demande
    for box in config.MapGoal:
        if in_box(annonce.geotag, config.MapGoal[box]) == True:
            annonce.quartier = str(box)
            prixPondere -= config.mapGoalReward
            break
    else:
        annonce.quartier = "Meh"

    # detecter la présence de mots tel que cave ou parking dans l'annonce

    for i in config.descriptifGoal:
        if i[0] in annonce.descriptif:
            annonce.pointsForts.append(i[0])
            prixPondere -= i[1]

    # distance depuis le metro

    #if there is a list of close stations :
    try:
        # if the graphhopper limit was reached when this listing was scored
        if annonce.stations[0][1] == None:
            # try to score it again
            check = distanceFromMetro(annonce)
            # if it doen't work, returs the scoring as is
            if check == False:
                prixMetreCarrePondere = prixPondere / annonce.surface
                logging.info("scoringFunc(annonce) - Ending w/o close station scoring")
                return (prixMetreCarreOriginal, prixMetreCarrePondere)
            #if it worked, test if it is close enough
            else :
                if annonce.stations[0][1] < config.minuteMetroGoal[0]:
                    annonce.stationProche = True
                    prixPondere -= config.minuteMetroGoal[1]
                    prixMetreCarrePondere = prixPondere / annonce.surface
                    prixMetreCarrePondere = prixPondere / annonce.surface
                    return (prixMetreCarreOriginal, prixMetreCarrePondere)
                else :
                    prixMetreCarrePondere = prixPondere / annonce.surface
                    return (prixMetreCarreOriginal, prixMetreCarrePondere)

        # if we have the info and the distance in in line with config file
        elif annonce.stations[0][1] < config.minuteMetroGoal[0]:
            annonce.stationProche = True
            prixPondere -= config.minuteMetroGoal[1]
            prixMetreCarrePondere = prixPondere / annonce.surface
            return (prixMetreCarreOriginal, prixMetreCarrePondere)
        else :
            prixMetreCarrePondere = prixPondere / annonce.surface
            return (prixMetreCarreOriginal, prixMetreCarrePondere)

    except IndexError:
        prixMetreCarrePondere = prixPondere / annonce.surface
        logging.warning("scoringFunc(annonce) - No stations for this listing")
        return (prixMetreCarreOriginal, prixMetreCarrePondere)


#this function scores a listing depending on the caracteristics described in the config file
#input : Annonce object
#output : False if one of the veto element is triggered, otherwise, a tuple with the original price per m2, and the score
def scoringFunc(annonce) :
    logging.info("scoringFunc(annonce) - Starting")
    logging.info("scoringFunc(annonce) - Get the DictMetro")
    dictMetro = dictFunctions.dictInitialization('dictMetroStation.txt')

    #Take out the VETO elements qui mont la qualité de veto
    if annonce.prix > config.priceMaxGoal or annonce.prix < config.priceMinGoal :
        logging.info("scoringFunc(annonce) - Ending")
        return False
    if annonce.surface < config.sizeMinGoal or annonce.surface > config.sizeMaxGoal :
        logging.info("scoringFunc(annonce) - Ending")
        return False
    if annonce.codePostal not in config.codePostalGoal :
        logging.info("scoringFunc(annonce) - Ending")
        return False
    if annonce.prixUnite != "€cc*" :
        print("charges non comprises")
        return False

    prixMetreCarreOriginal = annonce.prix/annonce.surface

    #Nice to Have

    prixPondere = annonce.prix
    if annonce.nbPiece == config.nbPiece[0] :
        prixPondere -= config.nbPiece[1]
    if annonce.nbChambre == config.nbChambre[0]:
        prixPondere -= config.nbChambre[1]
    if annonce.bilanConsoEnergie == config.bilanConsoEnergie[0]:
        prixPondere -= config.bilanConsoEnergie[1]
    if annonce.typologie == config.typologie[0]:
        prixPondere -= config.typologie[1]

    #test si le quartier correspond aux demande
    # modif de l'annonce pour contenir le quartier
    #modif du scoring

    for box in config.MapGoal:
        if in_box(annonce.geotag, config.MapGoal[box]) == True:
            annonce.quartier = str(box)
            prixPondere -= config.mapGoalReward
            break
    else:
        annonce.quartier = "Meh"

    #detecter la présence de mots tel que cave ou parking dans l'annonce

    for i in config.descriptifGoal :
        if i[0] in annonce.descriptif :
            annonce.pointsForts.append(i[0])
            prixPondere -= i[1]

    # distance depuis le metro
    #def Distancedumetro
    for station in dictMetro :
        #if the annonce is in the vicinity of a metro station
        if in_box(annonce.geotag, dictMetro[station]['bbox']) == True:
            #get the name of the station
            thisStation = dictMetro[station]['name']
            #Get the distance between the metro station
            howFarHowLong = CalltoGraphhopperAPI.graphhoppercall(annonce.geotag, dictMetro[station]['geotag'])
            if howFarHowLong == "NO INTERNET" :
                annonce.stations.append([thisStation, None, None])
                prixMetreCarrePondere = prixPondere / annonce.surface
                logging.info("scoringFunc(annonce) - Ending w/ error")
                return (prixMetreCarreOriginal, prixMetreCarrePondere)
            else:
                howFar = howFarHowLong[0]
                howLong = howFarHowLong[1]
                annonce.stations.append([thisStation, howFar, howLong])

    annonce.stations = sorted(annonce.stations, key= lambda x :x[1])
    try :
        if annonce.stations[0][1] < config.minuteMetroGoal[0] :
            annonce.stationProche = True
            prixPondere -= config.minuteMetroGoal[1]
    except IndexError :
        logging.warning("scoringFunc(annonce) - No stations for this listing")
    #calcule le nouveau scoring
    prixMetreCarrePondere = prixPondere/annonce.surface
    logging.info("scoringFunc(annonce) - Ending")
    return(prixMetreCarreOriginal, prixMetreCarrePondere)

#this function calcultates the first, second and third quartile of a list
def medianPosition(lst):
    logging.info("medianPosition(lst) - Starting")
    #calculates the median
    def medianOrigin(lst):
        lst = sorted(lst)
        if len(lst) < 1:
            return None
        if len(lst) % 2 == 1:

            return lst[int(((len(lst) + 1) / 2)) - 1]
        else:

            return float(sum(lst[int((len(lst) / 2)) - 1:int((len(lst) / 2)) + 1])) / 2.0

    #step 1 : sort the list
    lst = sorted(lst)
    #step 2 : calculate the median of the whole list
    median = medianOrigin(lst)
    #step 3 : determine the middle of the list
    position = int(len(lst) / 2)

    if median != None :
        # if the list is uneven
        if len(lst) %2 == 1:
            premQuartile = medianOrigin(lst[0:position])
            thirdQuartile = medianOrigin(lst[position+1:])
            logging.info("medianPosition(lst) - Ending")
            return(premQuartile, median, thirdQuartile)
        else:
            # if the list is even
            #print(lst[0:position])
            premQuartile = medianOrigin(lst[0:position])
            thirdQuartile = medianOrigin(lst[position:])
            logging.info("medianPosition(lst) - Ending")
            return(premQuartile, median, thirdQuartile)
    else :
        logging.info("medianPosition(lst) - Ending")
        return None

#testing :
# a = [1,3,12,18,23]
# print(medianPosition(a))
#
# b = [1,2]
# print(medianPosition(b))
#
# c = [3, 7, 8, 5, 12, 14, 21, 15, 18, 14]
# print(medianPosition(c))