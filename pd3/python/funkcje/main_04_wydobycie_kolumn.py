from config import co_przerobic, co_wykluczyc, co_wydobyc
from metody.skrypt import do_csv
import os
import sys
import multiprocessing
import re
from tqdm import tqdm


nadpisuj = False 

# Funkcja obrabiajaca forum
def wypisz_wymaluj_forum(nazwa_forum):
    
    for nazwa_pliku in co_wydobyc.keys():
        if os.path.isfile(os.path.join(output_path, "%s_%s.csv" % (nazwa_forum, nazwa_pliku))) and not nadpisuj:
            #print("Pomijam %s_%s" % (nazwa_forum, nazwa_pliku))
            continue
        print("Przetwarzam %s_%s.csv" % (nazwa_forum, nazwa_pliku))
        do_csv(
            z_czego=os.path.join(input_path, nazwa_forum, nazwa_pliku),
            co_wydobyc=co_wydobyc[nazwa_pliku],
            plik_wynikowy=os.path.join(output_path, "%s_%s" % (nazwa_forum, nazwa_pliku))
        )
        if delete:
            try:
                os.remove(os.path.join(input_path, nazwa_forum, nazwa_pliku+".xml"))
            except OSError as err:
                print ("Error: %s - %s." % (err.filename, err.strerror))
        
    # Usunięcie folderu na koniec
    if delete:
        try:
            os.rmdir(os.path.join(input_path, nazwa_forum))
        except OSError as err:
            print ("Error: %s - %s." % (err.filename, err.strerror))

if len(sys.argv) != 4:
    raise Exception("Zla liczba argumentow! Potrzebujemy folderu z podfolderami forow (kazdy z xml'ami), folderu do ktorego wypiszemy wynik i info czy usuwac('Tak'/ cokolwiek innego)")

# Odczytanie podanych ścieżek
input_path = sys.argv[1]
output_path = sys.argv[2]
delete = True if sys.argv[3] == "Tak" else False

# Stworzenie wynikowego katalogu, jeśli nie istnieje
if not os.path.isdir(output_path):
    os.makedirs(output_path)
    
# Odczytanie nazw forów z katalogu z uwzględnieniem wykluczeń
if len(co_przerobic) == 0:
    forum_names = ([nazwa
                   for nazwa in next(os.walk(input_path))[1]
                   if nazwa not in co_wykluczyc])
else:
    forum_names = co_przerobic

# Rozdzielenie forów na podzadania
pool = multiprocessing.Pool()

# Właściwa rzecz jest w tqdm, żeby pokazywał się postęp względem liczby forów
for _ in tqdm(pool.imap_unordered(wypisz_wymaluj_forum, forum_names), total=len(forum_names)):
    pass
        
pool.close()
