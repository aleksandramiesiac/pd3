from xml.etree.ElementTree import iterparse
import copy
import csv
from tqdm import tqdm

def do_csv(z_czego,co_wydobyc,  plik_wynikowy):
    """ 
        z_czego = nawa pliku bez rozszerzenia .xml
        co_wydobyc = lista nazw kolumn których potrzebujemy.
        plik_wynikowy = nazwa pliku wynikowego
     """
    #tree = et.parse(z_czego+".xml") 
    #root = tree.getroot()
    #print("Pobieram źródło")
    # open a file for writing
    #print("tworze plik wynikowy")
    if len(co_wydobyc)==0: return
    plik_data = open(plik_wynikowy+'.csv', 'w', encoding='utf-8')

    # create the csv writer object
    #print("Tworzy csv objekt")
    csvwriter = csv.writer(plik_data)
    #print("Nazywa wiersze")
    csvwriter.writerow(co_wydobyc)
    zmienna = co_wydobyc.copy()
    #print("dla kazego wiersza pisze")
    for event, member in iterparse(z_czego+".xml"):#tqdm(iterparse(z_czego+".xml")): 
        if event == 'end' and member.tag == 'row':
            data = []
            for i in range(len(co_wydobyc)): 
                zmienna[i] = member.get(co_wydobyc[i])
                data.append(zmienna[i])
            csvwriter.writerow(data)
        member.clear()
    plik_data.close()
