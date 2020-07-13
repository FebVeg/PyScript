import os
os.system("cls")

print("\n\t- Capture all stored wifi on Windows 10 -")
print("\t- Coded by FebVeg -\n")

new_dir = "C:\\Users\\%s\\Save_Wifi\\" % (os.getlogin())

try:
    print("[+] Creating a new directory: " + new_dir)
    os.mkdir(new_dir)

    print("[+] Saving profiles in %s" % (new_dir))
    os.system("netsh wlan export profile folder=%s key=clear > Nul" % (new_dir))
except Exception as error:
    print("[!] ERROR DURING PROCESS: " + str(error))

try:
    print("\n[i] Elaboring all file for getting: SSIDs + Passwors")
    print("="*50)
    for dirName, subdirName, files in os.walk(new_dir):
        for f in files:
            elab = open(new_dir+f).readlines()
            for line in elab:
                line = line.strip()
                if line.startswith("<name>"):
                    ssid = line.replace("<name>", "")
                    ssid = ssid.replace("</name>", "")
                if line.startswith("<keyMaterial>"):
                    password = line.replace("<keyMaterial>", "")
                    password = password.replace("</keyMaterial>", "") 
                    print(ssid + ": " + password)
    print("="*50)
    print("\n[+] Removing all xml files")
    for x in os.listdir(new_dir):
        os.remove(new_dir+x)
    print("[+] Removing dir: " + new_dir)
    os.removedirs(new_dir)
    print("[-] Done")
except Exception as error:
    print(error)
