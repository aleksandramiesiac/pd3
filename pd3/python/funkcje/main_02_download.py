from metody.przetwarzanie_plikow import get_filename, get_forumname, download_file
import os
import sys

if len(sys.argv) != 3:
    raise Exception("Zla liczba argumentow! Potrzebujemyu pliku z linkami i folderu do ktorego pobierzemy")

# Odczytanie podanej ścieżki
input_file = sys.argv[1]
output_path = sys.argv[2]

# Stworzenie katalogu, jeśli nie istnieje
if not os.path.isdir(output_path):
    os.makedirs(output_path)
    
# Stworzenie loga
with open("log.txt", "w") as log:
    print("url", "file_name", "forum_name", "status", sep=",", file=log)

with open(input_file, "r") as links_file:
    for line in links_file.readlines():

        # Odczytanie linku z pliku
        url = line.strip()

        # Odczytanie nazwy pliku i forum z linku
        file_name = get_filename(url)
        forum_name = get_forumname(file_name)

        # Stworzenie katalogu dla tego forum, jeśli nie istnieje
        forum_path = os.path.join(output_path, forum_name)
        if not os.path.isdir(forum_path):
            os.makedirs(forum_path)
        
        with open("log.txt", "a") as log:
            # Pobranie pliku .7z do katalogu forum
            if not download_file(url, file_name, path=forum_path):   # funkcja zwraca false, jeśli się wykrzaczy
                # przejście do następnego linku, jeśli coś poszło nie tak, czyli
                # albo rozmiar pobranego pliku nie zgadza się, albo gdy 10 razy będzie przekroczony czas połączenia
                print(url, file_name, forum_name, 0, sep=",", file=log)
                continue
            else:
                print(url, file_name, forum_name, 1, sep=",", file=log)
