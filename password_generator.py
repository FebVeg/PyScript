# Random Password Utility - FebVeg

import os
import sys
import string
import time
import random 
from random import *
from password_strength import *
import hashlib


def cleaner():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=2,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)

global space
space = " "*30

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def go_back():
    option_to_back = input("\nPremi [ENTER] per tornare al menu")
    if option_to_back == "":
        home()
    else:
        sys.exit(0)


def generator():
    cleaner()
    
    wordlist = input("Import your clean wordlist (es. not dark-wordlist): ")

    while True:
        word = choice(open(wordlist).read().split()).strip()
        simbols = "!$%&/*.-" + string.digits + string.ascii_uppercase
        random_chars = "".join(choice(simbols) for x in range(randint(4, 8))) # Randomizzo i caratteri della variabile simbols da 2 a 8
        password = "".join(word) + random_chars # Genero la password finale
        stats = PasswordStats(password)

        try:
            print(bcolors.HEADER + "Checking policies.. " + bcolors.ENDC + password, space, end="\r")
            time.sleep(0.10)
            if not policy.test(password):
                print(bcolors.WARNING + "Security testing.. " + bcolors.ENDC + password, space, end="\r")
                time.sleep(0.10)
                if stats.strength() > 0.700:
                    print("\rPassword generata secondo le policy e alla sicurezza impostata nel programma.")
                    print("Password:", bcolors.OKGREEN + password + bcolors.ENDC)
                    print("Livello di sicurezza:", stats.strength())
                    break
                else:
                    print( bcolors.FAIL+ "Bad Password: " + bcolors.ENDC + password, space, end="\r")
                    time.sleep(0.10)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            sys.exit(0)

    option_to_back = input("\nPremi [ENTER] per generare un'altra password\nPremi 'back' per tornare al menu\n> ")
    if option_to_back == "":
        generator()
    elif option_to_back == "back":
        home()
    else:
        sys.exit(0)

def test_password_user(password):
    print("-"*50)
    stats = PasswordStats(password) # creo una statistica in base all'entrofia della password

    if policy.test(password):
        print("Policy ignorate:", policy.test(password)) # Testo la password in base alle policy di sicurezza
    else:
        print("Policy rispettate.")

    # Verifico se in baso alla robustezza la password è valida
    if stats.strength() < 0.300:
        print("Password Vulnerabile")
        print("Livello di sicurezza:", stats.strength())
    elif stats.strength() < 0.500:
        print("Password Debole")
        print("Livello di sicurezza:", stats.strength())        
    elif stats.strength() > 0.700:
        print("Password Sicura")
        print("Livello di sicurezza:", stats.strength())
    else:
        print("Password valida")
        print("Livello di sicurezza:", stats.strength())


def bruteforce():
    cleaner()
    password_to_test = input("Type the password hashed: ")
    wordlist = input("Enter the full path of wordlist: ")

    print("\nHASH >", password_to_test)

    if os.path.exists(wordlist):
        print("Wordlist >", wordlist)
    else:
        print("Error to import the wordlist..")
        go_back()
    
    for x in open(wordlist).read().split():
        string = hashlib.md5(x.encode())
        string_hashed = string.hexdigest()

        print("Testing: " + x, space, end="\r")

        if password_to_test == string_hashed:
            print("\n\nPassword found: " + x)
            break


def hasher():
    string_to_hash = input("\nType the string you want to convert into MD5 hash: ")
    string_hashed = hashlib.md5(string_to_hash.encode())
    print("\nHash MD5 of: " + string_to_hash + " | " + string_hashed.hexdigest())    
    

def home():
    while True:
        cleaner()

        print("Password Tool - FebVeg")
        print("1. Test your password")
        print("2. Password generator tool")
        print("3. Break an MD5 password! (dictionary attack)")
        print("4. Convert a string to MD5 hash!")
        print("0. Exit")

        home_options = input("\nChoose betwen 1, 2, 3, 4, 0 > ")

        if home_options == "0":
            sys.exit(0)

        elif home_options == "1":
            password = input("\nType the password: ")
            test_password_user(password)
            go_back()
        
        elif home_options == "2":
            generator()
        
        elif home_options == "3":
            bruteforce()
            go_back()

        elif home_options == "4":
            hasher()
            go_back()

        else: 
            home()


home()
