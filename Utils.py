import os
from tqdm import tqdm
import requests

def downloadFile(url, filename, chunk_size):
    """
    Downloads a file from a given url and saves it to the given filename
    The filename should include the file extension

    :param url: The url to download the file from
    :param filename: The filename to save the file to
    :param chunk_size: The chunk size to use when downloading the file
    """

    print("Downloading file from " + url + " to " + filename)

    # get the file extension from filename
    file_extension = os.path.splitext(filename)[1]

    # if there is no file extension, warn the user
    if file_extension == '':
        print('Warning: No file extension found in filename')

    r = requests.get(url, stream=True)

    if r.status_code != 200:
        print("Error downloading file: " + str(r.status_code))
        return

    with open('/tmp/metadata' + file_extension, 'wb') as fd:
        for chunk in tqdm(r.iter_content(chunk_size)):
            fd.write(chunk)

    os.rename('/tmp/metadata' + file_extension, filename)

    print("Download complete")