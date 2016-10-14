#This Program creates a dictionnary af all posting that corresponds to a configuration (in the config file)
# Any new posting is scored (according to the config)
# Any new posting is compared to the median scoring of all available postings
#then it is saved in the dictionnary
import xmlGenerator
import howToScore
import dictFunctions
import logging
import broadcaster


###PREP###

#Get the new annonces, delete the old ones, Score them and broadcast them (log)
#input :saved listings (dictAnnonce)
#output : none
#effect : Broadcast of listings and their relative value compared to all available listings
def dictAnnonceUpdater(dictAnnonce) :
    logging.info("dictAnnonceUpdater(dictAnnonce) - Starting")
    ### PREP ####

    #this function finds the new listings and generates Annonces, and the listings that changed price.
    #This function updates the dictAnnonce with the new info
    #Input : List of Annonce present on the XML
    #output : list Annonces to analyze
    def getNewListings (listingsPresent):
        logging.info("getNewListings (listingsPresent) - Starting")
        annoncesToAnalyse = []

        for item in listingsPresent :

            annonceID = item.id
            annoncePrix = item.prix

            # if the listing is new
            if annonceID not in dictAnnonce :
                # score the new annonce
                scoreTemp = howToScore.scoringFunc(item)
                if scoreTemp == "NO INTERNET" :
                    logging.error("dictAnnonceUpdater - No internet")
                    logging.info("getNewListings (listingsPresent) - Ending w/ error")
                    return "NO INTERNET"
                if scoreTemp != False:
                    # Save the score of the new annonce
                    item.score = scoreTemp
                    # add new annonce to the Dictionnary of annonces
                    dictAnnonce[annonceID] = item
                    # add the ID to the list of new ids
                    annoncesToAnalyse.append(item)
                else :
                    continue
            #if the listing is not new but the price changed
            elif  annoncePrix != dictAnnonce[annonceID].prix:
                logging.info("new Price!!! " + annonceID)
                dictAnnonce[annonceID].prix = annoncePrix
                # score the new annonce
                scoreTemp = howToScore.scoringFunc(dictAnnonce[annonceID])
                if scoreTemp == "NO INTERNET":
                    logging.error("dictAnnonceUpdater - No internet")
                    return "NO INTERNET"
                # if there is no veto
                if scoreTemp != False:
                    # Save the score of the new annonce
                    dictAnnonce[annonceID].score = scoreTemp
                    # add the ID to the list of new ids
                    annoncesToAnalyse.append(dictAnnonce[annonceID])

            # If the listing is known and the price has not changed
            else :
                logging.info("old news")
                continue

        logging.info("getNewListings (listingsPresent) - Ending")
        return annoncesToAnalyse


    # Check if some listings are not on available anymore, delete them from the Dict
    # Input : List of the listing's ID in the XML, the dictionnary with the known annonces
    # Output : None
    # Effect : Delete in the Dictionnary, the Annonce that do not corresponds to an existing listing
    def deleteOldListings(listingsPresent) :
        logging.info("deleteOldListings(listingsPresent) - Starting")
        listofID =[]
        for j in listingsPresent :
            listofID.append(j.id)
        itemsToDel = []
        for i in dictAnnonce:
            if i not in listofID:
                logging.info("bye bye " + str(i))
                itemsToDel.append(i)
        for i in itemsToDel:
            del dictAnnonce[i]
        logging.info("deleteOldListings(listingsPresent) - Ending")

    # Calculates the median score of all existing Annonce and compare the score of the new annonces. Broadcasts the resultes
    # Input : list of the Annonce that need to be analyzed
    # Output : None
    # Effect : logs the score of each interesting listing
    def medianBroadcaster (annoncesToAnalyse):
        logging.info("medianBroadcaster (annoncesToAnalyse) - Starting")
        ### PREP ###

        medianList = []

        for i in dictAnnonce:
            medianList.append(dictAnnonce[i].score[1])

        lenMedianList = len(medianList)

        ### COOKING ###

        if lenMedianList > 2:
                # calc la médiane et les quartiles
                reperes = howToScore.medianPosition(medianList)

                for item in annoncesToAnalyse :

                    score = item.score[1]
                    if score < reperes[0]:
                        logging.info("Bellow 1st Quartile " + str(item))
                        #broadcaster.slackBroadcast("Bellow 1st Quartile ", item.surface, item.prix, item.stations[0], item.stations[1], item.url)
                    elif score < reperes[1]:
                        logging.info("Bellow the median : " + str(item))
                        #broadcaster.slackBroadcast("Bellow the median : ", item.surface, item.prix, item.stations[0],item.stations[1], item.url)
                    elif score < reperes[2]:
                        logging.info("Above the median : " + str(item))
                        #broadcaster.slackBroadcast("Above the median : ", item.surface, item.prix, item.stations[0],item.stations[1], item.url)
                    else:
                        logging.info("Above 1st Quartile : " + str(item))
                        try :
                            broadcaster.slackBroadcast("Above 1st Quartile : ", item.surface, item.prix, item.stations[0][0], item.stations[0][2],item.url)
                        except IndexError :
                            broadcaster.slackBroadcast("Above 1st Quartile : ", item.surface, item.prix, item.stations, item.codePostal, item.url)

        elif lenMedianList > 1 :
            logging.info("Only one listing available : " + str(annoncesToAnalyse[0]))
        else :
            logging.info("There are no Annonce in the Dictionnary")

        logging.info("medianBroadcaster (annoncesToAnalyse) - Ending")



    ### COOKING ###

    #Analyse the XML
    listingsPresent = xmlGenerator.ListingsPresentGeneratorSL()
    if listingsPresent == "NO INTERNET" :
        logging.error("dictAnnonceUpdater(dictAnnonce) - No internet")
        return "NO INTERNET"
    if listingsPresent == "NO LISTING" :
        logging.error('ListingsPresentGenerator - No listings')
        return "NO LISTING"

    annoncesToAnalyse = getNewListings(listingsPresent)
    #Clean up the DictAnnonce
    deleteOldListings(listingsPresent)
    #Calculates median and broadcast results
    medianBroadcaster(annoncesToAnalyse)

###COOKING###

def scrape_immo() :
    logging.basicConfig(filename='ImmoBot.log',format='%(levelname)s : %(asctime)s /// %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)
    logging.info('Started')
    #Creates a python Dictionnary out of the saved TXT file
    dictAnnonce = dictFunctions.dictInitialization('dictFile.txt')
    logging.info("On part avec " + str(len(dictAnnonce)) + " annonces")
    #Get the new annonces, delete the old ones, Score them and broadcast them (log)
    update = dictAnnonceUpdater(dictAnnonce)
    if update == "NO INTERNET" :
        logging.error("Se Loger BOT - No internet")
    if update == "NO LISTING":
        logging.error('Se Loger BOT - No listings')

    #Updates the saved TXT dictionnary file
    dictFunctions.dictFileUpdater(dictAnnonce, 'dictFile.txt')
    logging.info("On finit avec " + str(len(dictAnnonce)) + " annonces")


