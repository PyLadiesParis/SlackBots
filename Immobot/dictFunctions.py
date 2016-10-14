
import pickle
import os
import logging
#re-creates a Python Dictionnary from a TXT file where the dictionnary was saved
#input : TXT file
#output : python dictionnary


def dictInitialization (dictFile) :
    logging.info("dictInitialization (dictFile) - Starting")
    #if the file is empy : create an empy dictionnary
    if os.stat(dictFile).st_size == 0 :
        dictDefault = {}
    else :
        #otherwise, read the file
        output = open(dictFile, 'rb')
        #make a dictionnary from that file
        dictDefault = pickle.load(output)    # 'obj_dict' is a dict object
        #close the file
        output.close()
    logging.info("dictInitialization (dictFile) - Ending")
    return dictDefault


#Erases everything in the dictfile, writes the complete Dictionnary in Dict File
def dictFileUpdater(dictionnary, dictFile) :
    logging.info("dictFileUpdater(dictionnary, dictFile) - Starting")
    output = open(dictFile, 'w')
    output.close()
    output = open(dictFile, 'ab+')
    pickle.dump(dictionnary, output)
    output.close()
    logging.info("dictFileUpdater(dictionnary, dictFile) - file updated")
    logging.info("dictFileUpdater(dictionnary, dictFile) - Ending")