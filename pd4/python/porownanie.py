from sklearn.metrics.cluster import fowlkes_mallows_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import adjusted_rand_score
from scipy.cluster.hierarchy import linkage
from scipy import cluster
import genieclust
#3 inne algorytmy z sklearn : 
from sklearn.cluster import MeanShift, AgglomerativeClustering, KMeans
from spectral import spectral_clustering

import glob
import os
import numpy as np
import pandas as pd

method = ["single",'complete','average','weighted','centroid','median','ward']

def Porownaj_algorytmy(data, klasy, labels, method, baza):
    """
    Oblicza indeksy AM, AR i FM dla wszystkich algorytmów, aprócz napisanego przeze mnie.
    """

    wektor =[]
    test =[0]*len(method)
    i=0
    #algorytmy linkage
    for name in method:
        Z = linkage(data, name)
        test[i] = cluster.hierarchy.cut_tree(Z,klasy)
        test[i] = [y for x in test[i] for y in x]
        wektor.append([fowlkes_mallows_score(labels,test[i]), adjusted_mutual_info_score(labels, test[i]),adjusted_rand_score(labels,test[i]),baza ])
        i+=1
    # algorytm genieclust
    wynikMG = genieclust.genie.Genie(n_clusters=klasy).fit_predict(data)
    wektor.append([fowlkes_mallows_score(labels,wynikMG), adjusted_mutual_info_score(labels, wynikMG),adjusted_rand_score(labels,wynikMG),baza ])
    
    #MeanShift
    wynikCL = MeanShift(bandwidth=klasy).fit(data).labels_
    wektor.append([fowlkes_mallows_score(labels,wynikCL), adjusted_mutual_info_score(labels, wynikCL),adjusted_rand_score(labels,wynikCL),baza ])
    
    #AgglomerativeClustering
    wynikFA = AgglomerativeClustering(n_clusters=klasy).fit(data).labels_
    wektor.append([fowlkes_mallows_score(labels,wynikFA), adjusted_mutual_info_score(labels, wynikFA),adjusted_rand_score(labels,wynikFA),baza ])
    
    #KMeans
    wynikKM = KMeans(n_clusters=klasy, random_state=123).fit(data).labels_
    wektor.append([fowlkes_mallows_score(labels,wynikKM), adjusted_mutual_info_score(labels, wynikKM),adjusted_rand_score(labels,wynikKM) ,baza])
    
    
    index = ["single",'complete','average','weighted','centroid','median','ward', "genieclust","AgglomerativeClustering","KMeans","MeanShift"]
    
    return pd.DataFrame(wektor, index = index, columns = ["FM","AM","AR", "Dane"])
katalog = ["fcps","graves","other","sipu","wut"]
def wczytaj_dane(katalog):
    """
    zaladowanie danych od MG
    """
    data = []
    label = []
    lista_plikow = []
    labels=[]
    lista_baz = []

    
    for i in katalog:
        lista_plikow.append(glob.glob(os.path.join(i, "*.data.gz")))
        label.append(glob.glob(os.path.join(i, "*.labels0.gz")))

    for i in range(len(lista_plikow)):
        for nazwa in sorted(lista_plikow[i]):
            data.append(np.loadtxt(nazwa, ndmin=2))
            lista_baz.append(nazwa[:-8])
        for labe in sorted(label[i]):
            labels.append(np.loadtxt(labe, dtype=np.int))
    return data, lista_baz, labels


def wczytaj_dane2():
    """
    zaladowanie zbiorkow zrobionych przeze mnie
    """
    lista_baz = ["zbiorek1","zbiorek2","zbiorek3"]
    data = [0]*3
    labels = [0]*3
    for i in range(len(lista_baz)):
        data[i] = np.array(pd.read_csv("moje/"+lista_baz[i]+".data").iloc[:,[1,2]])
        labels[i] = np.array(pd.read_csv("moje/"+lista_baz[i] + ".labels0").iloc[:,[1]])
        labels[i] = [y+1 for x in labels[i] for y in x]
    return data, lista_baz, labels


def generuj_wyniki(data, labels, method, lista_baz):
    """
    wypluwa ramkę danych i zapisuje ją do csv na wszystkich zbiorach od MG
    """
    ramka = Porownaj_algorytmy(data[0], max(labels[0]), labels[0], method, baza = lista_baz[0])

    for i in range(1,len(data)):
        ramka = ramka.append(Porownaj_algorytmy(data[i], max(labels[i]), labels[i], method, baza = lista_baz[i]))
        print("Jestem na bazie: ", lista_baz[i])

    ramka.to_csv("danebench")

def generuj_wyniki_stand(data, labels, method, lista_baz):
    """
    wypluwa ramkę danych i zapisuje ją do csv na wszystkich zbiorach od MG standaryzowanych
    """
    przyklad = (data[0].transpose() - np.mean(data[0].transpose()))/np.std(data[0].transpose(), ddof =1)
    ramka = Porownaj_algorytmy(przyklad.transpose(), max(labels[0]), labels[0], method, baza = lista_baz[0])

    for i in range(1,len(data)):
        przyklad1 = (data[i].transpose() - np.mean(data[i].transpose()))/np.std(data[i].transpose(), ddof =1)
        ramka = ramka.append(Porownaj_algorytmy(przyklad1.transpose(), max(labels[i]), labels[i], method, baza = lista_baz[i]))
        print("Jestem na bazie: ", lista_baz[i])

    ramka.to_csv("danebenchstd")


def Porownaj_algorytmy2(data, klasy, labels, baza):
    """
    Oblicza indeksy AM, AR i FM dla algorytmu napisanego przeze mnie.
    """
    wektor =[]
    
    #moj algorytm
    wynikM = spectral_clustering(data, k=klasy, M=5)
    wektor.append([fowlkes_mallows_score(labels,wynikM), adjusted_mutual_info_score(labels, wynikM),adjusted_rand_score(labels,wynikM),baza ])
    
    index=["Moj"]
    
    return pd.DataFrame(wektor, index = index, columns = ["FM","AM","AR", "Dane"])



def generuj_wyniki2(data, labels, lista_baz):
    """
    wypluwa ramkę danych i zapisuje ją do csv na wszystkich zbiorach od MG 
    algorytm napisany przez mnie.
    """
    
    wyniki = Porownaj_algorytmy2(data[0], max(labels[0]), labels[0], baza = lista_baz[0])
    for i in range(1,len(data)):
        wyniki = wyniki.append(Porownaj_algorytmy2(data[i], max(labels[i]), labels[i], baza = lista_baz[i]))
        print("Jestem na bazie: ", lista_baz[i])
    wyniki.to_csv("NapisanyAlgorytm")


def generuj_wyniki2_stand(data, labels, lista_baz):
    """
    wypluwa ramkę danych i zapisuje ją do csv na wszystkich zbiorach od MG standaryzowanych
    algorytm napisany przez mnie.
    """
    przyklad = (data[0].transpose() - np.mean(data[0].transpose()))/np.std(data[0].transpose(), ddof =1)
    wyniki = Porownaj_algorytmy2(przyklad.transpose(), max(labels[0]), labels[0], baza = lista_baz[0])
    for i in range(1,len(data)):
        przyklad1 = (data[i].transpose() - np.mean(data[i].transpose()))/np.std(data[i].transpose(), ddof =1)
        wyniki = wyniki.append(Porownaj_algorytmy2(przyklad1.transpose(), max(labels[i]), labels[i], baza = lista_baz[i]))
        print("Jestem na bazie: ", lista_baz[i])
    wyniki.to_csv("NapisanyAlgorytmMojeSTD")

def ypredstd(data1, labels, lista_baz):
    """
    zapisuje w pliku txt w miejscu gdzie sa dane  podzial na klasy obliczony algorytmem:
    1. genieclust
    2. MeanShift
    3. hierarchiczny 'single'
    dla danych standaryzowanych
    """
    y_pred=[]
    i=0
    for data in data1:
        data = (data.transpose() -np.mean(data.transpose()))/np.std(data.transpose(), ddof=1)
        data = data.transpose()
        klasy = max(labels[i])
        wynikMG = genieclust.genie.Genie(n_clusters=klasy).fit_predict(data)
        wynikCL = MeanShift(bandwidth=klasy).fit(data).labels_
        Z = linkage(data, 'single')
        wynikSI = cluster.hierarchy.cut_tree(Z,klasy)
        wynikSI = [y for x in wynikSI for y in x]
        y_pred.append([wynikMG, wynikCL, wynikSI])
        i+=1
    for i in range(len(y_pred)):
        np.savetxt(lista_baz[i]+"y_predstd", y_pred[i], fmt = "%d")

def ypred(data1, labels, lista_baz):
    """
    zapisuje w pliku txt w miejscu gdzie sa dane  podzial na klasy obliczony algorytmem:
    1. genieclust
    2. MeanShift
    3. hierarchiczny 'single'
    """
    y_pred=[]
    i=0
    for data in data1:
        klasy = max(labels[i])
        wynikMG = genieclust.genie.Genie(n_clusters=klasy).fit_predict(data)
        wynikCL = MeanShift(bandwidth=klasy).fit(data).labels_
        Z = linkage(data, 'single')
        wynikSI = cluster.hierarchy.cut_tree(Z,klasy)
        wynikSI = [y for x in wynikSI for y in x]
        y_pred.append([wynikMG, wynikCL, wynikSI])
        i+=1
    for i in range(len(y_pred)):
        np.savetxt(lista_baz[i]+"y_pred", y_pred[i], fmt = "%d")
