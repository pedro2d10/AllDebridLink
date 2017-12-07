import argparse
import json
import urllib2
import requests
import sys, getpass
import getopt
from os.path import expanduser
import os.path

SoftName="ppitest"
Token=""
tryprotect=False


def temp():
        reponse=requests.get(UrlLogin)
        data=reponse.json()

        if data["success"]:
                if data["user"]["isPremium"]:
                        print "Utilisateur authentifie et premium"
                        Token=data["token"]
                else:
                        print "l utilisateur n'est pas premium"
                        sys.exit(1)
        else:
                print "Erreur d'authentification"
                sys.exit()

        #reponse=requests.get("https://api.alldebrid.com/link/redirector?agent="+SoftName+"&token="+Token+"&link=https://www.liens-telechargement.com/123455600123$
        data=reponse.json()

        print data

def init(Tokenfile):
        Login = raw_input("Enter your Alldebrid login: \n")
        Password = getpass.getpass("Enter your password: \n")
        try:

                urllogin= "https://api.alldebrid.com/user/login?agent="+SoftName+"&username="+Login+"&password="+Password
                reponse = requests.get(urllogin)
#               print urllogin
                data = reponse.json()
#               print data
                if data["success"]:
                        if data["user"]["isPremium"]:
                                print "Utilisateur authentifie et premium"
                                Token=data["token"]
#                               print Token
                                f = open(Tokenfile, 'w')
                                f.write(str(Token))
                                f.close()
                        else:
                                print "l utilisateur n'est pas premium"
                                sys.exit(1)
        except:
                        print "Unexpected error:", sys.exc_info()

def debridlink(link):
        Token = getTokenFile()
        global tryprotect
        if Token == None:
            print "Non initialise, utiliser l option -i pour generer le Token"
        else:
            try:
                print link
                print tryprotect
                #urlwithlink="https://api.alldebrid.com/link/redirector?agent="+SoftName+"&token="+Token+"&link="+link[0]
                urlwithlink="https://api.alldebrid.com/link/infos?agent="+SoftName+"&token="+Token+"&link="+link[0]
                
                reponse=requests.get(urlwithlink)
                data = reponse.json()
                print data
                if data["success"]:
                    keylist = data["infos"].keys()
                    if keylist[0] == "errorCode" and tryprotect == False:
                        tryprotect=True
                        print "host not supported, trying to bypass protect link"
                        urlwithlinkprotected="https://api.alldebrid.com/link/redirector?agent="+SoftName+"&token="+Token+"&link="+link[0]
                        reponse=requests.get(urlwithlinkprotected)
                        data = reponse.json()
                        debridlink(data["links"])
                    else:
                        print "Create link for file:" + data["infos"]["filename"]
                        urllinkdebrided = "https://api.alldebrid.com/link/unlock?agent="+SoftName+"&token="+Token+"&link="+data["infos"]["link"]
                        reponse=requests.get(urllinkdebrided)
                        data = reponse.json()
                        print data["infos"]["link"]
            except:
                print "Unexpected error:", sys.exc_info()
            #https://api.alldebrid.com/link/redirector?agent=mySoft&token=TOKEN&link=LINK
            

def getTokenFile():
        TockenFile =  (expanduser("~") + "/.alldebrid")
        if os.path.isfile(TockenFile):
                f = open(TockenFile, 'r')
                tocken = f.readline()
#               print tocken
                return tocken
        else:
                print "nok"

def main():
        tryprotect = False
        parser = argparse.ArgumentParser(prog='AllDebrid', description = "Permet de debrider des lien via l API AllDebrid")
        parser.add_argument('-i', '--init', help="init for the first connexion with %(prog)s", action="store_true")
        parser.add_argument('-u', help="Login Premium Alldebrid")
        parser.add_argument('-l' '--link', dest='link', nargs=1, help="url to debrid")
        args = parser.parse_args()

        initfile = expanduser("~") + "/.alldebrid"
        if args.init :
                init(initfile)
                sys.exit()

        if args.link != None:
                debridlink(args.link)

#       print initfile
#       init(initfile)

if __name__ == "__main__":
    main()