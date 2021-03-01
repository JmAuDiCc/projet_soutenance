import pandas as pd
import numpy as np
from datetime import datetime,date,timedelta 
import scrap_titres as st
from os import path
import socket
import time



#permet de vérifier si l'on est bien connecté afin d'effectuer le scrap
def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 80))
        return True
    except OSError:
        pass
    return False

###########################################################################
#créations des listes qui permetront de récupérer les données
def crea_listes(x,y,taille):
    return [x]*taille,[y]*taille


liste_titres = []
liste_journaux = []
liste_dates = []

def insert_nom_et_dates(nomJournal, day, titres_scrap):
    global liste_titres
    global liste_journaux
    global liste_dates
    
    liste_titres = liste_titres + titres_scrap
    li = crea_listes(nomJournal,day,len(titres_scrap))
    liste_journaux = liste_journaux + li[0]
    liste_dates = liste_dates + li[1]

##############################################################################


# tant que l'on est pas connecté, attendre 20 secondes
try: 
    while not is_connected():
        time.sleep(20)
    



    ########################
    #récupération du dernier de récupération des données
    f = open("dernier_jour.txt", encoding="utf-8")
    day = [date.strip() for date in f][-1]
    day = (pd.to_datetime(day , format="%d-%m-%Y").date())
    f.close()

    #############################
    #listes spéciales pour charlie, non opti ( récupération du thème également ==> petit model sur le thème?)
    liste_ch = () 
    liste_titre_charlie = []
    liste_th_charlie = []
    liste_date_charlie = []

    #listes des journaux associés à leur fonction permetant le scrap des titres ( non opti ==> dictionnaire dans st?)
    noms_journaux = ['Libération','Le Monde','Nord Presse','Science et Avenir','Closer','Gorafi','La Point','Public','Figaro']
    noms_function = ['scrap_libe','scrap_monde','scrap_nord_presse','scrap_sience_avenir','scrap_closer','scrap_gorafi','scrap_le_point','scrap_public','scrap_figaro']

    hier = date.today() - timedelta(days=1)
    
    #input("apres 4...")

    while day!= hier:

        liste_e = []

        liste_titres = []
        liste_journaux = []
        liste_dates = []

        #input("avt st.charlie ..")

        day = day + timedelta(days=1)
        #récupération titres charlie
        if not liste_ch:
           liste_ch = st.recup_listes_charlie(day)
            
        #input("apres st.charlie ..")

        #pour récup theme et model en fonction => à voir en plus
        res=st.scrap_charlie(day,liste_ch) #retourne tuple titre,theme du jour
        liste_titre_charlie = liste_titre_charlie + res[0]
        liste_th_charlie = liste_th_charlie + res[1]
        liste_date_charlie = liste_date_charlie + [day]*len(res[0])
        
        #input("apres st.charlie 2..")

        #charlie pour insertion BD 
        liste_titres = liste_titres + res[0]
        li = crea_listes('Charlie Hebdo',day,len(res[0]))
        liste_journaux = liste_journaux + li[0]
        liste_dates = liste_dates + li[1]

        #input("test pour autres journ..")

        for nom_j,nom_fun in zip (noms_journaux,noms_function):
            l = []   
            try:
                l = getattr(st, nom_fun)(day)
                insert_nom_et_dates(nom_j, day, l)
                print(day, nom_j, len(l))
            except Exception as e:
                if type(e).__name__ == "HTTPError":
                    print(type(e).__name__ , e.code , nom_j , len(l) ,e.url, e.name)
                    liste_e.append(str(datetime.now())+" | "+str(type(e).__name__)+" | "+str(e.code)+" | "+nom_j+" | "+str(e.url))
                else:
                    print(type(e).__name__)
                    print(e)
                    print(type(e))
                    liste_e.append(str(datetime.now()+" | "+str(type(e).__name__) ))

        if liste_titres:            
            df = pd.DataFrame()
            df['titre'] = liste_titres
            df['journal'] = liste_journaux
            df['date'] = liste_dates
            csv_path_name = "data_titres/titres_presse/titres_" + str(day) + ".csv"         
            df.to_csv(index=False ,path_or_buf=csv_path_name,encoding = 'utf-8')  

        if liste_e:
            path_name = "data_titres/logs/log_error"+str(day)+".log"
            f=open(path_name,'w')
            for er in liste_e:
                f.write(er+'\n')

            f.close()



    df_charlie = pd.DataFrame()
    df_charlie['titre'] = liste_titre_charlie
    df_charlie['theme'] = liste_th_charlie
    df_charlie['date'] = liste_date_charlie


    if not path.exists('data_titres/charlie_hebdo/charlie.csv'):
        df_charlie.to_csv(index=False ,path_or_buf='data_titres/charlie_hebdo/charlie.csv',encoding = 'utf-8')
    else:
        df_charlie.to_csv(index=False ,path_or_buf='data_titres/charlie_hebdo/charlie.csv',mode='a',encoding = 'utf-8',header=False)


    f = open('dernier_jour.txt','a')
    f.write('\n' + day.strftime('%d-%m-%Y'))
    f.close()  
    
except Exception as e:
    #liste_e.append(str(datetime.now()+" | "+str(type(e).__name__)+" | "+"FATAL" ))
    input("Fatal Error...")
    
    
    