# Covid scraper ita, coded by FebVeg
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

def computer_os():
    # Controllo sistema operativo
    if os.name == "nt": # NT è windows
        os.system("cls") # pulisco il CMD / PS
    else:
        os.system("clear") # Pulisco la bash shell

def worldSituation():
    try:
        URL = 'https://www.worldometers.info/coronavirus/'
        #proxy = "https://user:pass@proxy:porta"
        #os.environ['https_proxy'] = proxy

        page = requests.get(URL, verify=True) # normale richiesta al sito
        soup = BeautifulSoup(page.content, 'html.parser') # Elaborazione del Contenuto della pagina

        # Dati 
        lastupdate = soup.find('body').find('div', {'style': 'font-size:13px; color:#999; margin-top:5px; text-align:center'}) # Ultimo Aggiornamento
        coronavirus_data = soup.findAll(id='maincounter-wrap') # Dettagli
        currently_infected_activeCases = soup.find('body').find('div', {'class': 'number-table-main'}) # casi attualmente positivi
        mild_activeCases = soup.find('body').find('div', {'style': 'float:left; text-align:center'}).find('span') # totali in buone condizioni
        serious_activeCases = soup.find('body').find('div', {'style': 'float:right; text-align:center'}).find('span') # totali gravi
        
        print(bcolors.OKGREEN + soup.title.text + bcolors.ENDC)

        # Titolo 
        if lastupdate:
            print(lastupdate.text + "\n")
        else:
            print("Error to extracting 'Last update' data from: " + URL)
        
        # principali dettagli
        if coronavirus_data:
            for x in coronavirus_data:
                print(bcolors.BOLD + x.text.strip().replace("\n", " ") + bcolors.ENDC)
        else:
            print("Error to extract data")

        # totale infettati in italia
        if currently_infected_activeCases:
            print()
            print(bcolors.WARNING + "Currently Infected Patiens: " + bcolors.ENDC + currently_infected_activeCases.text.strip())
        else:
            print("Error to extract $currently_infected_activeCases")

        # Totale infettati in buone condizioni
        if mild_activeCases:
            print(bcolors.HEADER + "In Mild Conditions: " + bcolors.ENDC + mild_activeCases.text)
        else:
            print("Error to extract data $mild_activeCases")

        # Totale infettati GRAVI
        if serious_activeCases:
            print(bcolors.FAIL + "Serious and Critical: " + bcolors.ENDC + serious_activeCases.text)
        else:
            print("Error to extract data $serious_activeCases")

    except Exception as e:
        print(e)

def italySituation():
    try:
        URL = 'http://www.salute.gov.it/portale/nuovocoronavirus/dettaglioContenutiNuovoCoronavirus.jsp?lingua=italiano&id=5351&area=nuovoCoronavirus&menu=vuoto' 
        page = requests.get(URL, verify=True) # normale richiesta al sito
        soup = BeautifulSoup(page.content, 'html.parser') # Elaborazione del Contenuto della pagina

        print(bcolors.OKGREEN + soup.title.text + bcolors.ENDC) # Titolo

        # test
        dati = soup.findAll('div', {'id': 'intestazioneContenuto'}) 
        for temp in dati:
            testo = temp.findChildren()[12]
            div1 = temp.findChildren()[30]
            div2 = temp.findChildren()[31]
            div3 = temp.findChildren()[33]
            div4 = temp.findChildren()[34]
            div5 = temp.findChildren()[35]
        for x in testo:
            print(x.strip())
        for divs1 in div1:
            print("\n" + bcolors.WARNING + divs1.strip() + bcolors.ENDC + "\n")
        for divs2 in div2:
            print(bcolors.BOLD + divs2.strip() + bcolors.ENDC)
        for divs3 in div3:
            print("     " + divs3.strip())
        for divs4 in div4:
            print("     " + divs4.strip())
        for divs5 in div5:
            print("     " + divs5.strip())
        
    except Exception as e:
        print(e)

try:
    while True:
        computer_os()
        ultimo_controllo = (time.strftime("%H:%M:%S")) # Data e orario
        print("\nRiepilogo CORONAVIRUS \nPer chiudere il programma premi CTRL+C") # titolo
        print("Ultimo Controllo: " + bcolors.WARNING + ultimo_controllo + bcolors.ENDC) 
        print("\nCaricamento dati..", end="\r")
        worldSituation()
        print("\nCaricamento dati..", end="\r")
        italySituation()
        time.sleep(600)
except KeyboardInterrupt:
    print("\nChiusura del programma\n")
