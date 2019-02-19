import gc  # Usuwanie
import glob
import os
import pandas as pd
import re
import time
from tqdm import tqdm


def wczytaj_main(input_path, typ_pliku, kolumny, pomin_fora=None, part_len=30):
    """
    Funkcja zwraca pandasową ramkę, która zawiera wybrane kolumny z podanego typu plików (np. Comments).
    Pliki to csvki, które powinny być w jednym folderze, którego ścieżkę podajemy jako input_path.
    Dodatkowo możemy podać po ile forów ma zczytywać i doklejać do wynikowej ramki na raz (30 jest całkiem spoko).
    """
    def chunks(l, n):
        """ Yield successive n-sized chunks from l. """
        for i in range(0, len(l), n):
            yield l[i:i + n]
            
    # Komunikat powitalny :P
    start = time.process_time()
    print("Zaczynamy!", flush=True) 
    
    # Wynikowa ramka
    wynik = pd.DataFrame(columns=kolumny)
    
    # Odczytanie listy csv-ek do zmielenia
    lista_plikow = glob.glob(os.path.join(input_path, "*_%s.csv" % typ_pliku))
    
    # Licznik do garbage collectora
    counter = 0
    
    # Główna akcja, dla podziału na listy (part_len)-elementowe dopisujemy ten kawałek do wyniku
    for lista in chunks(lista_plikow, part_len):
        wynik = wynik.append(wczytaj_csv(lista, kolumny, pomin_fora), sort=False)
        
        # Zbieranie śmieci
        counter += 1
        if counter % 10 == 0:
            gc.collect()
    
    # Komunikat końcowy -- ile to wszystki zajęło
    end = time.process_time()
    print("Gotowe! Zajęło nam to: %ss" % round(end-start, 1))
    
    # Zwrócenie pięknej ramencji
    return wynik


def wczytaj_csv(lista_plikow, kolumny, pomin_fora):
    """
    Wczytuje kolumny z csv z listy do jednej ramki.
    """
    
    ramka = pd.DataFrame(columns=kolumny)
    
    # Przetwarzamy każdy plik podany w liście
    for file_path in tqdm(lista_plikow):
        
        # Odczytyujemy dane ze ścieżki
        nazwa_pliku = re.search("[^/]*$", file_path).group()
        nazwa_forum = re.search("[^_]*", nazwa_pliku).group()
        
        # Pominięcie zaznaczonych forów
        if pomin_fora is not None and nazwa_forum in pomin_fora:
            continue
        
        # Dodanie nowego forum
        ramka = ramka.append(
            pd.read_csv(
                file_path,              # ścieżka csv
                usecols=kolumny,        # kolumny, które odczytamy
                keep_default_na=False,  # nie uwzględniamy domyślnych wartości rzutowanych na NA
                na_values=[""]          # mówimy, że NA to jedynie puste wartości
            ).assign(
                Forum=nazwa_forum       # przyda się do matchowania
            ),
            sort=False                  # nie mieszamy kolejności kolumn
        )
        
    return ramka