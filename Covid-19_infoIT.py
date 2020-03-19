import requests
from bs4 import BeautifulSoup
import os
import time
import urllib
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

while True:
    try:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        URL = 'https://www.worldometers.info/coronavirus/country/italy/'
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'} # User Agent
        #proxy = "https://user:pass@proxy:porta"
        #os.environ['https_proxy'] = proxy

        ultimo_controllo = (time.strftime("%H:%M:%S")) # Data e orario
        print("\nRiepilogo CORONAVIRUS in Italia \nPer chiudere il programma premi CTRL+C") # titolo
        print("Ultimo Controllo: " + bcolors.WARNING + ultimo_controllo + bcolors.ENDC) 
        print("Link: " + URL + "\n")

        page = requests.get(URL, headers=headers, verify=True) # normale richiesta al sito
        soup = BeautifulSoup(page.content, 'html.parser') # Elaborazione del Contenuto della pagina
        lastupdate = soup.find('body').find('div', {'style': 'font-size:13px; color:#999; text-align:center'}) # Casi totali
        coronavirus_data = soup.findAll(id='maincounter-wrap') # Dettagli

        currently_infected_activeCases = soup.find('body').find('div', {'class': 'number-table-main'})

        mild_activeCases = soup.find('body').find('div', {'style': 'float:left; text-align:center'}).find('span')
        serious_activeCases = soup.find('body').find('div', {'style': 'float:right; text-align:center'}).find('span')

        # Titolo 
        if lastupdate:
            print(bcolors.UNDERLINE + lastupdate.text + bcolors.ENDC + "\n")
        else:
            print("Error to extracting 'Last update' data from: " + URL)
        
        # principali dettagli
        if coronavirus_data:
            for x in coronavirus_data:
                print(x.text.strip().replace("\n", " "))
        else:
            print("Error to extract data")

        # totale infettati in italia
        if currently_infected_activeCases:
            print("Currently Infected Patiens: " + currently_infected_activeCases.text.strip())
        else:
            print("Error to extract $currently_infected_activeCases")

        # Totale infettati in buone condizioni
        if mild_activeCases:
            print("In Mild Conditions: " + mild_activeCases.text)
        else:
            print("Error to extract data $mild_activeCases")

        # Totale infettati GRAVI
        if serious_activeCases:
            print("Serious and Critical: " + serious_activeCases.text)
        else:
            print("Error to extract data $serious_activeCases")

        break # per ora lo blocco per fare i test
        #time.sleep(300)

    except Exception as e:
        print(e)
        break
    
    except KeyboardInterrupt:
        print("\nChiudo il programma")
        sys.exit(0)


