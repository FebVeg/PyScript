import base64
import sys
import os

# Intro
print("\nPython - Convert python script to Base64\nCoded by FebVeg\n")


# Variabili
currentPath = os.path.dirname(os.path.abspath(__file__)) + "\\" # Workink directory
text_payload = "encoded_script.txt"

# Input dell'utente
file_to_enc = input("File: ")
python_payload = input("Type the final name of payload (es. shell.py or pincopalle.py): ")

data = open(file_to_enc).read() # Apro il file in readmode dentro ad una variabile

encodedBytes = base64.b64encode(data.encode("utf-8")) # Codifico il file
encodedStr = str(encodedBytes, "utf-8") # creo una variabile con le stringhe codificate

# verifico se non esiste la directory di output
if not os.path.isdir(currentPath + "output"):
    os.mkdir(currentPath + "output")

def creating_encoded_payload():
    try:
        print("\n[INFO] If you need to use pyinstaller after encoding the payload, you need to add a library!!!")
        libs = input("[+] Add a library? like (es. ',pynput,win32gui,win32clipboard') or just press ENTER for none: ")
        if libs == "":
            libs = ""
        # scrivo il pyload codificato
        build = "import base64,sys%s;exec(base64.b64decode({2:str,3:lambda b:bytes(b,'UTF-8')}[sys.version_info[0]]('%s')))" % (libs, encodedStr)
        py_enc = open(currentPath + "output\\" + python_payload, "w")
        py_enc.write(build)
        py_enc.close()
        print("\nFile [output/%s] Saved" % (python_payload))
    except Exception as error:
        print(error)

def save_txt():
    try:
        # salvo il codice codificato
        py_enc = open(currentPath + "output\\" + text_payload, "w")
        py_enc.write(encodedStr)
        py_enc.close()

        print("\nFile [output/%s] Saved" % (text_payload))
    except Exception as error:
        print(error)

while True:
    print("-"*30)
    print("1. Print the encoded strings")
    print("2. Just build the payload")
    print("3. Save encoded stings into a txt file")
    print("0. Exit")
    show = input("> ")

    if show == "1":
        print("-"*50)
        print(encodedStr) # Stampo le stringhe codificate
        print("-"*50)
    elif show == "2":
        creating_encoded_payload()
    elif show == "3":
        save_txt()
    elif show == "0":
        print("\nBye")
        sys.exit()
    else:
        print("Wrong decision")
