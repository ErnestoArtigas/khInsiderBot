"""
Code written by Ernesto Artigas.
Licence GNU General Public Licence v3.0.
"""

import colorama
import os
import requests
from tqdm import tqdm
from urllib.parse import unquote

def getRequestFromLink(link):
	request = requests.get(link)
	if request.status_code != 200:
		request.raise_for_status()
	return request



def extractDecodeFileName(url):
	return unquote(url.split("/")[-1])



def createDirectory(directoryName):
	path = os.path.join(os.getcwd(), directoryName)
	try:
		os.mkdir(path)
	except OSError as error:
		raise error



def downloadFile(path, link):
	request = getRequestFromLink(link)
	fileName = extractDecodeFileName(link)
	totalSize = int(request.headers.get("content-length"))
	try:
		with open(f"{path}\{fileName}", 'wb') as file:
			with tqdm(total=totalSize, unit="B", unit_scale=True, desc=fileName, initial=0, ascii=False, colour="green") as progressBar:
				for chunk in request.iter_content(chunk_size=1024):
					if chunk:
						file.write(chunk)
						progressBar.update(len(chunk))
	except Exception as error:
		raise (error)



def downloadFiles(directoryName, linkArray):
	try:
		createDirectory(directoryName)
		for element in linkArray:
			downloadFile(f"{os.getcwd()}\{directoryName}", element)
		print(colorama.Fore.GREEN + "Finished downloading all files.")
	except Exception as error:
		print(colorama.Fore.RED)
		print(error)
