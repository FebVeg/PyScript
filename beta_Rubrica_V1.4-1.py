# Rubrica del Rifugio
# Versione 1.4-1 
# changelog
# Chiusura automatica dopo aver creato una nuova sotto cartella
# Aggiunta modifica Contatto + Aggiunta funzione per inserire documenti nel contatto
# Modificato il metodo di inserimento del contatto - possibililià di scrivere un nuovo contatto anche se esso è già esistente

# --------------------------------------------------------------------------------------------------------------
# Importo le librerie
import os
import subprocess
import sys
import shutil
import time
import glob
import pathlib
# --------------------------------------------------------------------------------------------------------------
# importo le libreria per lavorare con la parte grafica
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
# --------------------------------------------------------------------------------------------------------------
# Creo la funzione che genererà un file di log per ulteriori debug
def logCapture(log):
    fileLog = "log_Rubrica.log"
    f = open(fileLog, "a")
    f.write("{0} -- {1}\n".format(data, log))
    f.close()
# --------------------------------------------------------------------------------------------------------------
# Variabili 
try:
    subdirs = ["Rubrica/_Documenti", "Rubrica/Coniglio", "Rubrica/Criceto", "Rubrica/Degu", "Rubrica/Gatto", "Rubrica/Cane", "Rubrica/Cincillà", "Rubrica/Volatile", "Rubrica/Ratto", "Rubrica/Topo", "Rubrica/Serpente", "Rubrica/Tartaruga"]
    get_usr = os.getlogin() # username del PC (windows)
    global data # Globalizzo la variabile DATA (per impostare un'orario)
    data = (time.strftime("%d/%m/%Y %H:%M")) # Data e orario
    programPath = pathlib.Path(__file__).parent.absolute() # cartella assoluta del programma della Rubrica

    if os.path.isdir("Rubrica") == 1: # Controllo se la Cartella RUBRICA esiste
        print("Cartella RUBRICA trovata, controllo il database..")
    else: 
        os.mkdir("Rubrica") # Creo la Rubrica
        print("Rubrica creata")

    for c in subdirs: # Controllo che il database esista
        if(os.path.isdir(c)) == 1: 
            print("Sottocartella: " + c + " trovata")
        else:
            for i in subdirs:
                if(os.path.isdir(i)) == 0: # Controllo se le sottocartella esistano
                    os.mkdir(i) # Creo le sottocartelle
                    print("Cartella " + i + " creata")
except Exception as log:
    logCapture(log)
# --------------------------------------------------------------------------------------------------------------
def nuovoContatto():
    try:
        # Contenuto delle textbox
        contenuto = "Nominativo: %s\nIndirizzo: %s\nCellulare: %s\nAnimale: %s\nTipologia: %s\nNote: %s\nData: %s" % (nominativo.get(), indirizzo.get(), cellulare.get(), animale.get(), tipologia.get(), note.get("1.0","end-1c"), data)
        global noPdf # Globalizzo la variabile noPdf
        noPdf = var.get() # Prendo in considerazione che il pulsante è stato premuto in variabile noPdf

        # Verifico che ALMENO la entry nominativo.get() sia stata scritta
        if len(nominativo.get()) == 0: # Controllo se la entry nominativo sia a 0 
            messagebox.showwarning("Avviso", "Il contatto ha bisogno di un Nominativo per essere aggiunto al Database") # AlertMessageBox: No user was declared
            log = "Funzione nuovoContatto() --> Il contatto ha bisogno di un Nominativo per aggiungerlo al Database"
            logCapture(log)
            print() # WorkAround per il problema che quando aggiungi un pdf o non lo dichiari e aggiungi il contatto ti restituisce il contenuto 
        else: 
            if os.path.isdir("Rubrica/" + animale.get()) == 0: # Verifico che la sottocartella esista
                messagebox.showerror("Errore", "Sottocartella non trovata. Riprova usando la sintassi corretta. Esempio: 'Gatto Cane' e non 'gatto cane'.") # Syntax log
                log = "Funzione nuovoContatto() --> Sottocartella non trovata. Riprova usando la sintassi corretta. Esempio: 'Gatto Cane' e non 'gatto cane'."
                logCapture(log)
                print() # WorkAround per il problema che quando aggiungi un pdf o non lo dichiari e aggiungi il contatto ti restituisce il contenuto 
            else:
                try: ######################################################
                    os.mkdir("Rubrica/" + animale.get() + "/" + nominativo.get()) # Creo la cartella del Contatto
                    fileContatto = open("Rubrica/" + animale.get() + "/" + nominativo.get() + "/" + nominativo.get() + ".txt", "a") # Creo il file txt
                    fileContatto.write(str(contenuto)) # inserisco nel txt i dati ottenuti
                    fileContatto.close() # Chiudo il file txt
                except Exception as log:
                    logCapture(log)
                    messagebox.showerror("Errore", "Contatto già presente in rubrica")
            if noPdf == 0:
                if os.path.exists(pathOfPdf) == 1: # Controllo se il pdf esiste e lo sposto nella cartella del contatto
                    shutil.copy(pathOfPdf, "Rubrica/%s/%s" % (animale.get(), nominativo.get()))
                    os.rename(("Rubrica/%s/%s/" + pdf) % (animale.get(), nominativo.get()), "Rubrica/" + animale.get() + "/" + nominativo.get() + "/" + nominativo.get() + ".pdf")

            contactSavedMessage = "Contatto salvato nella sottocartella: " + animale.get() + " > " + nominativo.get()
            messagebox.showinfo("Info", contactSavedMessage) # Se il contatto è stato salvato, riferisco dove
        messagebox.showinfo("Info", contenuto) # Mostro il contenuto dopo l'aggiunta del contatto
        ResetTextBox() # Pulisco l'interfaccia
    except Exception as log:
        logCapture(log)
# --------------------------------------------------------------------------------------------------------------
# Funzione che cerca il pdf
def caricaFile():
    try:
        name = askopenfilename(initialdir="C:/Users/" + get_usr + "/", # Apro il file manager
                            filetypes =(("File PDF", "*.pdf"),("All Files", "*.*")), # Imposto la ricerca in base all'estensione scritta
                            title = "Scegli il File" # Titolo del file manager
                            )
        # Rendo globali le due variabili affinchè tutto il programma faccia fede a loro
        global pathOfPdf
        global pdf
        global pdfClear

        pathOfPdf = str(name) # Tengo a mente l'output in stringa del nome del pdf
        pdf = os.path.basename(pathOfPdf) # Converto la full path con il solo nome del file preso da pathOfPdf
        pdfClear = Label(root, text=pdf, font=("Verdana", 11))
        pdfClear.grid(row=8, column=1, padx=20, sticky=E+N+S)
    except Exception as log:
        logCapture(log)
# --------------------------------------------------------------------------------------------------------------
def addNewDocument(): # Funzione che aggiunge un documento di ogni tipo alla sottocartella del contatto
    try:
        cercaDocumento = askopenfilename(initialdir = programPath,
            filetypes = (("file PDF", "*.pdf*"),("All files","*.*")),
            title = "Aggiungi cun File al Contatto"
            ) # Apro la finestra per la ricerca del file

        global documento # globalizzo la viariabile documento
        documento = str(cercaDocumento) # assegno in stringa il valore di cercaDocumento, ovvero il nome del file che si vuole

        if os.path.isfile(documento) == True: # verifico che il file esista
            try:
                shutil.copy(documento, pathlib.Path(contatto).parent.absolute()) # Copio il file nella sottocartela del contatto
                messagebox.showinfo("Avviso", "Documento: %s inserito nella sottocartella > %s" % (os.path.basename(cercaDocumento), pathlib.Path(contatto).parent.absolute()))
            except Exception as log:
                messagebox.showerror("Errore", "Errore imprevisto durante la copia del file: %s" % (documento))
                logCapture(log)             
    except Exception as log: # se ci fosse un eccezione, stampo l'errore nel file di log
        logCapture(log)
# --------------------------------------------------------------------------------------------------------------
def editContatto(): # Funzione che apre il documento TXT per un eventuale modifica
    try:
        os.startfile(contatto)
    except Exception as log:
        logCapture(log)
# --------------------------------------------------------------------------------------------------------------
# Funzione che apre il documento nella funzione di cercaContatto
def apriPdf(): # Apro il file PDF
    try:
        a = os.path.splitext(contatto)[0] # Grabbo il nome del contatto senza estensione 
        # Verico che il pdf o documento esista
        if os.path.exists(a + ".pdf") == 1:
            os.startfile(a + ".pdf") # Apro il pdf
        else:
            messagebox.showerror("Errore", "Documento non trovato")
            log = "Funzione apriPdf() --> Documento non trovato"
            logCapture(log)
    except Exception as log:
        logCapture(log)
# --------------------------------------------------------------------------------------------------------------
# Funzione che apre la sottocartella del contatto in cercaContatto()
def openContactDir():
    try:
        os.startfile(pathlib.Path(contatto).parent.absolute())
    except Exception as log:
        messagebox.showerror("Errore", log)
# --------------------------------------------------------------------------------------------------------------
# Funzione che cerca un contatto
def cercaContatto():
    try:
        global cercaNome
        cercaNome = askopenfilename(initialdir = programPath, # Apro il file manager
                        filetypes = (("file TXT", "*.txt"),("All Files","*.*")), # Imposto la ricerca in base all'estensione scritta
                        title = "Cerca Contatto" # Titolo del file manager
                        )

        global contatto # Globalizzo la variabile
        contatto = str(cercaNome) # Converto in Stringa la fullpath del contatto, il file txt

        if os.path.exists(contatto) == 1:
            secondRoot = Tk() # Creo la finestra
            secondRoot.title("Contatto della Rubrica") # Titolo della finestra
            secondRoot.resizable(True, True) # Blocco il resize

            fileContatto = open(cercaNome).read() # Apro il file in modalità lettura dentro una variabile
            Label(secondRoot, text=fileContatto, font=("Verdana", 12)).grid(row=0, column=0, columnspan=4, padx=20, pady=20, sticky=W+E+N+S) # Faccio apparire quello che c'è dentro al file del Contatto
            
            Button(secondRoot, text="Apri PDF", command=apriPdf).grid(row=1, column=0, padx=20, pady=20, sticky=W+N+S) # Pulsante per aprire il PDF
            Button(secondRoot, text="Apri Cartella", command=openContactDir).grid(row=1, column=1, padx=20, pady=20, sticky=W+N+S) # Pulsante per aprire il PDF
            Button(secondRoot, text="Aggiungi File", command=addNewDocument).grid(row=1, column=2, padx=20, pady=20, sticky=W+N+S)
            Button(secondRoot, text="Modifica", command=editContatto).grid(row=1, column=3, padx=20, pady=20, sticky=W+N+S)
            Button(secondRoot, text="Chiudi", command=secondRoot.destroy).grid(row=1, column=4, padx=20, pady=20, sticky=E) # Chiudo la finestra
        else:
            messagebox.showerror("Errore", "Contatto non trovato.")
            log = "Funzione cercaContatto() --> Contatto non trovato."
            logCapture(log)
    except Exception as log:
        logCapture(log)
# --------------------------------------------------------------------------------------------------------------
def aggiuntiSottocartella(): # Aggiungo la funzione che crea una nuova sottocartella da aggiungere al database
    def aggiungiCartella(): # Funzione che crea la sottocartella
        try:
            if len(nomeSottocartella.get()) == 0:
                messagebox.showwarning("Avviso", "Per aggiungere una nuova sottocartella al database devi scrivere il nome")
                log = "Funzione aggiungiCartella() --> Avviso, Per aggiungere una nuova sottocartella al database devi scrivere il nome"
                logCapture(log)
            else:            
                if os.path.isdir("Rubrica/" + nomeSottocartella.get()): # Verifico se la Sottocartella esiste già
                    messagebox.showerror("Errore", "Sottocartella già presente nel database")
                    log = "Funzione aggiungiCartella() --> Sottocartella già presente nel database"
                    logCapture(log)
                else: 
                    os.mkdir("Rubrica/" + nomeSottocartella.get()) # Creo la sottocartella
                    cartellaCreata = "Sottocartella " + nomeSottocartella.get() + " creata"
                    messagebox.showinfo("Info", cartellaCreata)
                    nomeSottocartella.delete(0, END)
                    fourthRoot.destroy()
        except Exception as log:
            logCapture(log)
    try: 
        fourthRoot = Tk() # Creo la finestra
        fourthRoot.title("Aggiungi nuova Sottocartella al DataBase") # Titolo della finestra
        fourthRoot.resizable(False, False) # Blocco il resize della finestra
        fourthRoot.grid_columnconfigure(1, weight=1) # Espando la colonna 1

        Label(fourthRoot, text="Nome: ", font=("Verdana", 12)).grid(row=0, column=0, sticky="W", padx=10, pady=10)
        nomeSottocartella = Entry(fourthRoot, font=("Verdana", 11))
        nomeSottocartella.grid(row=0, column=1, sticky=W+E+N+S, padx=10, pady=10)
        Button(fourthRoot, text='Aggiungi', command=aggiungiCartella).grid(row=1, column=0, sticky=W, padx=10, pady=20) # Pulsante Aggiungi Sottocartella al DB
        Button(fourthRoot, text='Chiudi', command = fourthRoot.destroy).grid(row=1, column=1, sticky=E, padx=10, pady=20) # Pulsante chiudi
    except Exception as log:
        logCapture(log)
# --------------------------------------------------------------------------------------------------------------
# Funziona che pulisce le textbox
def ResetTextBox():
    try:
        nominativo.delete(0, END)
        indirizzo.delete(0, END)
        cellulare.delete(0, END)
        animale.delete(0, END)
        tipologia.delete(0, END)
        note.delete("1.0", END)
        var.set(0)
        pdfClear.destroy()
    except Exception as log:
        logCapture(log)
# --------------------------------------------------------------------------------------------------------------
def BackUpRubrica(): # Funzione che esegue un backup della Rubrica
    try:
        fifthRoot = Tk()
        fifthRoot.title("BackUp Rubrica")
        
        Button(fifthRoot, text="Percorso della Rubrica").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        # creare una label che spawna ilpercorso della rubrica
        # creare funzione che zippa le cartelle e sottocartelle
        # bottone che sceglie dove backuppare lo zip e creare una label che spawna il percorso finale
    except Exception as log:
        logCapture(log)
# --------------------------------------------------------------------------------------------------------------
# Funzione che apre il filemanager nel DB delle sottocartelle
def openDB(): 
    try:
        databasePath = os.path.dirname(__file__) # assegno alla variabile la absolute path del programma in stringa
        os.startfile(databasePath + "\\Rubrica\\") # avvio il file manager sotto la cartella Rubrica
    except Exception as log:
        logCapture(str(position) + log)
# --------------------------------------------------------------------------------------------------------------
def openLogFile(): # Creo una funzione per aiutarmi a debuggare il programma
    try:
        fileForDebug = "log_Rubrica.log" # file di log
        if os.path.exists(fileForDebug) == 0: # Controllo se il file non esiste
            messagebox.showerror("Errore", "File di LOG non trovato")
        else:
            os.startfile(fileForDebug) # Apro il file di log
    except Exception as log:
        logCapture(log)
# --------------------------------------------------------------------------------------------------------------

# Inizio della GUI 
# y = verticale 
# x = orizzontale
try: 
    root = Tk()
    root.title("Rubrica - Version: 1.4-1")
    root.resizable(True, True)
    root.geometry("500x375")
    root.grid_columnconfigure(1, weight=1)
    var = IntVar() # dichiaro che Var è un intero (0-1)
    var.set(0) # Setto di default su 0 il radiobutton

    # Barra del Menù
    menu = Menu(root)
    root.config(menu=menu)
    opzioni = Menu(menu)
    menu.add_cascade(label = 'File', font=("Verdana", 13), menu = opzioni) # Pulsante a cascata: File
    opzioni.add_command(label = 'Cerca Contatto', command = cercaContatto)
    opzioni.add_command(label = 'Aggiungi Sottocartella', command = aggiuntiSottocartella)
    opzioni.add_command(label = 'Apri Database', command = openDB)
    opzioni.add_command(label = 'Debug', command = openLogFile)
    opzioni.add_command(label = 'Esci', command = root.destroy) # Pulsante Exit

    # Mostro la scritta che precede le textbox
    Label(root, text="Nominativo: ", font=("Verdana", 12)).grid(row=1, column=0, sticky="W", padx=20) # Nominativo
    Label(root, text="Indirizzo: ", font=("Verdana", 12)).grid(row=2, column=0, sticky="W", padx=20) # Indirizzo
    Label(root, text="Cellulare: ", font=("Verdana", 12)).grid(row=3, column=0, sticky="W", padx=20) # Cellulare
    Label(root, text="Animale: ", font=("Verdana", 12)).grid(row=4, column=0, sticky="W", padx=20) # Animale
    Label(root, text="Tipologia: ", font=("Verdana", 12)).grid(row=5, column=0, sticky="W", padx=20) # Tipologia
    Label(root, text="Note: ", font=("Verdana", 12)).grid(row=6, column=0, sticky="W", padx=20) # Note
    # --------------------------------------------------------------------------------------------------------------
    Label(root, text="").grid(row=7, column=0, sticky="W", padx=20) # Separatore
    ttk.Separator(root, orient='horizontal').grid(row=7, columnspan=2, sticky=W+E) # Separatore
    # --------------------------------------------------------------------------------------------------------------
    Button(root, text='Carica File', command=caricaFile).grid(row=8, column=0, sticky=W, padx=20, pady=5) # Pulsante Carica File
    Radiobutton(root, text = "Non allegare documento", variable=var, value=1).grid(row=8, column=1, sticky=W) # Pulsante Radio per dichiarare la mancanza di un documento (bypass pdf variable log)
    # --------------------------------------------------------------------------------------------------------------
    Label(root, text="").grid(row=9, column=0, sticky="W", padx=20) # Separatore
    ttk.Separator(root, orient='horizontal').grid(row=9, columnspan=2, sticky=W+E) # Separatore

    # Creo le Entry per il contenutto delle textbox
    nominativo = Entry(root, font=("Verdana", 11))
    indirizzo = Entry(root, font=("Verdana", 11))
    cellulare = Entry(root, font=("Verdana", 11))
    animale = Entry(root, font=("Verdana", 11))
    tipologia = Entry(root, font=("Verdana", 11))
    note = Text(root, width=20, height=3)
    note.grid(row=6, column=1, sticky=W+E+N+S, pady=5, padx=20)

    #Textbox
    nominativo.grid(row=1, column=1, pady=5, padx=20, sticky=W+E+N+S)
    indirizzo.grid(row=2, column=1, pady=5, padx=20, sticky=W+E+N+S)
    cellulare.grid(row=3, column=1, pady=5, padx=20, sticky=W+E+N+S)
    animale.grid(row=4, column=1, pady=5, padx=20, sticky=W+E+N+S)
    tipologia.grid(row=5, column=1, pady=5, padx=20, sticky=W+E+N+S)

    # Mostro i pulsanti 
    Button(root, text= 'Reset', command=ResetTextBox).grid(row=10, column=0, sticky=W+S, padx=20, pady=20) # Pulsante Pulisci
    Button(root, text='Aggiungi', command=nuovoContatto).grid(row=10, column=1, sticky=E+S, padx=20, pady=20) # Pulsante Agiungi alla rubrica

    root.mainloop()
except Exception as log:
    logCapture(log)