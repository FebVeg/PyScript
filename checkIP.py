# controllo stato di un device collegato in rete
# FebVeg 

import os 
import socket
import time
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

def logger(log): # funzione che salva i log qual'ora il programma si interrompesse e il terminale crashasse
    namefile = address + ".log"
    logFile = open(namefile, "a")
    logFile.write("{}\n".format(log))
    logFile.close()

os.system("cls")
print("-"*55)
print("Automatic IP Checker - Fabrizio CAGNINI")
print("-"*55)
print("Printers port > 9100\nWebsites port > 80\nMicrosoft SMB > 445")
print("\nMore ports are here: https://it.wikipedia.org/wiki/Lista_di_porte_standard")
print("-"*75)

try:
    address = input("Target: ")
    int_port = int(input("Port: "))
    int_seconds = int(input("Retry Seconds: "))
    time.sleep(1)
    print("Log file: " + address + ".log")
    print("-"*85)
except Exception as e:
    print(e)

while True:
    try: 
        s =  socket.socket() # creo il socket di connessione
        result = s.connect_ex((address, int_port)) # risultato di connessione
        s.close() # chiudo il socket
        data = (time.strftime("%d/%m/%Y %H:%M:%S")) # Data e orario
    except socket.error as log:
        print(log)
        logger(log)

    try:
        if result:
            try:  
                log = data + " | " + address + ":" + str(int_port) + " > OFFLINE" # Variabile di log
                print(data + " | " + address + ":" + str(int_port) + bcolors.FAIL + " OFFLINE" + bcolors.ENDC)
                time.sleep(int_seconds)
            except KeyboardInterrupt:
                sys.exit(0)
        else:
            try:
                log = data + " | " + address + " > ONLINE" + " | Hostname > " + socket.gethostbyname(address) + ":" + str(int_port) # Variabile di log
                print(data + " | " + address + " | Hostname = " + socket.gethostbyname(address) + ":" + str(int_port) + bcolors.OKGREEN + " ONLINE" + bcolors.ENDC)            
                time.sleep(int_seconds)
            except KeyboardInterrupt:
                sys.exit(0)
        # Salvo i log di test
        logger(log)
    # eccezione durante la richiesta socket - problema generale di connessione
    except socket.error as log:
        logger(log)
        time.sleep(1)
        print(log) 
