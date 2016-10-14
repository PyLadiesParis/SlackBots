# Se Loger Slackbot Documentation

The main file is "immobot.py"

Once the Config file is set, t works in three steps :
1. it reads and imports an existing dictionary of listings ("DictFile.txt")
2. it updates the list of listings and broadcast the new listings (and the old listings with a new price)
3. it saves the updated listings in the dictionary DictFile.txt for later use

The functions for step 1 and 3, to read/save the external dictionary, are stored in the **dictFunction Module**
The function for step 2, called **"dictAnnonceUpdater"**, works like this

##dictAnnonceUpdater
* function : Get the new annonces, delete the old ones, Score them and broadcast them (print)
* input : Dictionnary of listings (dictAnnonce)
* output : none
* effect : Broadcast of listings and their relative value compared to all available listings

1. it lists all the available listing (in Annonce Class form, available in immobilier.py) on the Se Loger WS
2. Compare the list with de dictionnary of existing listings (DictAnnonce)
3. if the listing is new or has changed price, add it to annoncesToAnalyse and update the dictionnary
4. Delete listings that are in the dictionnary but not available anymore
5. Score the listings in annoncesToAnalyse and brodcasts the results


### Step 1, we use **xmlGenerator.ListingsPresentGeneratorSL()** cf doc de xmlGenerator

### getNewListings(listingsPresent) (Step 2)
*this function finds the new listings and generates Annonces, and the listings that changed price.
*This function updates the dictAnnonce with the new info
*Input : List of Annonce present on the XML
*output : list Annonces to analyze

### deleteOldListings(listingsPresent) (Step 3)
    # Check if some listings are not on available anymore, delete them from the Dict
    # Input : List of the listing's ID in the XML, the dictionnary with the known annonces
    # Output : None
    # Effect : Delete in the Dictionnary, the Annonce that do not corresponds to an existing listing

### medianBroadcaster(annoncesToAnalyse) (Step 4)
    # Calculates the median score of all existing Annonce and compare the score of the new annonces. Broadcasts the resultes
    # Input : list of the listings that need to be analyzed
    # Output : None
    # Effect : Prints the score of each interesting listing, updates the dictionnary
    --> the scoring function are in the howToScore Module

## xmlGenerator
xmlGenerator contais all the functions that use Se Loger specific information to run

## Config

## CalltoGraphhopperAPI

## howToScore
## dictFunctions
## immobilier

## TXT Files

### dictfile.txt
### DictMetroStations

## Directories

## Heuristiques :
- Une annonce est corompue quand elle n'a pas d'ID unique, dans ce cas là, elle est eliminée (xml generator, listofpresent)
- le prix entre cc et non cc, est calculé avec une moyenne


# todo :
* differencier le scoring charges comprise ou non
* finish the documentation
* optimize scoringFunc(annonce)
* Question : Utilile de garder un dict ? pourquoi pas une liste ID et prix ?)

# Sources
* https://www.dataquest.io/blog/apartment-finding-slackbot/
