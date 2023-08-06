import os, sys

if os.path.isfile("Package_Installer/Logs/Log_Installed.log"):
    print("[  DEBUG  ] : Looks Like This is not first time run. Going to Start Page...")
    exit
else: 
    print("[  DEBUG  ] : Looks Like This is first time you launch Cmon-AI. Installing Packages you downloaded with package...")

class Installer:
    def __init__():
        print("[  DEBUG  ] : Initializing OS...")
        os.system("bash Package_Installer/GOV/install_all.sh [DEBUG]")
        print("[  DEBUG  ] : Successfully Installed all of packages!. Note: May be python3 default replaced with old version but is not very important because with any update for Cmon-AI packages replaced with lastest version.")
        return 0

if __name__=="__main__":
    Installer()
    
    exit