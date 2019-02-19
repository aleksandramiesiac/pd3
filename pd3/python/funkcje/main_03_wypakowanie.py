from metody.przetwarzanie_plikow import extract_7z, remove_file
import os
import sys
import glob

if len(sys.argv) != 2:
    raise Exception("Zla liczba argumentow! Potrzebujemy pliku z folderami: forum/7z")

# Odczytanie podanych ścieżek
input_path = sys.argv[1]

for forum_name in next(os.walk(input_path))[1]:
    
    # Zmontowanie biezacej sciezki
    forum_path = os.path.join(input_path, forum_name)
    
    for zfile in glob.glob(os.path.join(forum_path, "*.7z")):
        print(forum_path)
        print(zfile)
        # Wypakowanie pliku
        extract_7z(zfile, forum_path)
    
        # Usunięcie .7z
        # remove_file(zfile)
