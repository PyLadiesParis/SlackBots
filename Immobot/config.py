
SLEEP_INTERVAL = 20 * 60
#location ou achat
location = True
achat = False

#type de biens
typebien = {"Appartement": True,
                  "MaisonVilla": 200,
                  "ParkingBox": False,
                  "Terrain": False,
                  "Boutique": False,
                  "LocalCommercial": False,
                  "Bureaux": False,
                  "LoftAtelierSurface": 200,
                  "Immeuble": False,
                  "Batiment": False,
                  "Chateau": False,
                  "Hotelparticulier": 200,
                  "Programme": False
                  }
#price & size
sizeMinGoal = 50
sizeMaxGoal = 70
priceMinGoal = 1000
priceMaxGoal = 2000

#descriptif (element, prix associé)
nbPiece = (3, 100)

nbChambre = (2, 10)
bilanConsoEnergie = ("A", 50)
typologie = ("true", 50)

descriptifGoal = [("cave", 100), ("parking", 100), ("bain", 200)]


#Obligatoires
codePostalGoal = [75013]

#mieux si
MapGoal = {
    "bibliotheque_francois_mitterand": [
        [48.836889, 2.3869513],
        [48.827049, 2.366719]
    ],
    "carreaux_du_temple": [
        #top right
        [48.865384, 2.374603],
        # bottomLeft
        [48.8618975, 2.3516863]
    ]}
mapGoalReward = 100

minuteMetroGoal = (5,100)
