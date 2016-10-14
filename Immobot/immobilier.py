import datetime
#Each listing is an instance of the class Annonce
class Annonce:
    def __init__(self,idAnnonce, dtcreation, prix, prixUnite, surface, nbPiece, nbChambre, descriptif, codePostal, permalien, geotag, bilanConsoEnergie, nbPhotos, nomAgence, rcsSirenAgence, photo, typologie):
        self.id = idAnnonce
        self.url = permalien
        self.dtcreation = dtcreation
        self.prix = prix
        self.prixUnite = prixUnite
        self.surface = surface
        self.nbPiece = nbPiece
        self.nbChambre = nbChambre
        self.descriptif = descriptif
        self.codePostal = codePostal
        self.geotag = geotag
        self.bilanConsoEnergie = bilanConsoEnergie
        self.nbPhotos = nbPhotos
        self.nomAgence = nomAgence
        self.rcsSirenAgence = rcsSirenAgence
        self.photo = photo
        self.typologie = typologie
        self.quartier = None
        self.score = None
        self.pointsForts = []
        self.stations = []
        self.stationProche = False

    def __str__(self):
        # this function tells you how old the posting is un a tuple (publicationDate, HowLongAgo)
        def DateFormating(dateFromatInput):
            # Input = date as it appears in the XML
            # output = tuple of date in datetime format and how long ago it was
            year = int(dateFromatInput[0:4])
            month = int(dateFromatInput[5:7])
            day = int(dateFromatInput[8:10])
            hour = int(dateFromatInput[11:13])
            minute = int(dateFromatInput[14:16])
            second = int(dateFromatInput[17:19])
            # print(year, month, day, hour, minute, second)
            pubDate = datetime.datetime(year, month, day, hour, minute, second)

            todayDate = datetime.datetime.now()

            pubAge = todayDate - pubDate
            if pubAge.days > 0:
                pubAgePrint = pubAge.days
                ago = (str(pubAgePrint) + " days ago")
            elif pubAge.seconds > 3600:
                pubAgePrint = int(pubAge.seconds / 3600)
                ago = (str(pubAgePrint) + " hours ago")
            else:
                pubAgePrint = int(pubAge.seconds / 60)
                ago = (str(pubAgePrint) + " minutes ago")
            # print(pubDate, ago)
            return (pubDate, ago)

        dateItem = DateFormating(self.dtcreation)

        return  str(self.id) + "///" + str(dateItem[1]) + " /// " + str(self.prix)+"€ " + " /// " + str(self.surface) + " m2" +  "////" + " Metro : " + str(self.stations)+ "//////" + " Points forts : " + str(self.pointsForts)+ "//////" + " RCS : " + str(self.rcsSirenAgence) + "//////" + " photo : " + str(self.photo)
