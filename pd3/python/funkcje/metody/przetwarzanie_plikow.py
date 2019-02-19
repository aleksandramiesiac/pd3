from tqdm import tqdm
import requests
import os
import re
import time
import codecs


def get_filename(url):
    """
    Extracts stackexchange's archive from the URL.
    """
    return re.search(r"[^/]*$", url).group(0)


def get_forumname(filename):
    """
    Extracts the forum name from the file name
    """
    return re.search(r"^[^\.]*(\.meta)?", filename).group(0)


def download_file(url, filename, path="./temp"):
    """
    Saves file from provided URL under a specified name.
    """
    # Creating the temp folder
    if not os.path.isdir(path):
        os.mkdir(path)
    
    # Reading the url
    for i in range(10):
        try:
            resp = requests.get(url, stream=True)
        except requests.exceptions.Timeout:
            # Retry connecting after 15 seconds
            time.sleep(15)
            continue
        except requests.exceptions.RequestException as err:
            with codecs.open("log.txt", "a", "utf-8") as err_log:
                print(f"File: {filename}\nURL: {url}\n", err, file=err_log)
            return False
        break
    total_size = int(resp.headers.get('content-length', 0))
    
    # Setting needed variables
    block_size = 1024
    saved = 0
    
    # Saving the file
    with open(os.path.join(path, filename), "wb") as f:
        for data in tqdm(resp.iter_content(block_size), total=total_size//block_size, unit="KB", unit_scale=True, desc=filename):
            saved += len(data)
            f.write(data)
    
    # Download completeness check
    if total_size != 0 and saved != total_size:
        with codecs.open("log.txt", "a", "utf-8") as err_log:
            print(f"File: {filename}\nURL: {url}\n", "Plik nie został pobrany w całości", file=err_log)
        return False

    # Successful download!
    return True


def extract_7z(archive_path, output_path):
    """
    File extracts the .7z archive contents using the 7z program.
    """
    os.system(f"7z x {archive_path} -o{output_path} && rm {archive_path}")


def remove_file(file_path):
    """
    Deletes the .7z archive and the usual .xml files from temp directory.
    """
    # Removing provided file (usually .7z archive)
    os.remove(file_path)
