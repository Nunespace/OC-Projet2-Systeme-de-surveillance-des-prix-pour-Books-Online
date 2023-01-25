import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

from livre import *
from categorie import *

url_site= "http://books.toscrape.com"

def recuperation_code_page(url):
    reponse = requests.get(url)
    # transforme (parse) le HTML en objet BeautifulSoup. test est ajouté pour avoir le texte et non le code 200
    soup = BeautifulSoup(reponse.text, "html.parser")
    if reponse.ok:  # cad si requests.get renvoie le code 200
        return soup
    
def recuperation_liste_url_categories (url, soup):
    a_liens=soup.findAll('a') #class_="side_categories")
    liste_liens=[]
    for lien in a_liens:
        liste_liens.append (url_site+"/"+lien['href'])
    liste_liens_categories=liste_liens[3:53]
    return liste_liens_categories
     
 
soup=recuperation_code_page(url_site)
liste_liens_categories=recuperation_liste_url_categories (url_site, soup)

dico_liens_livres=recuperation_infos_livre (url_product)

"""
liste_all_livres=[]
for lien_categorie in liste_liens_categories :
    url_categorie=lien_categorie
    soup_categorie=recuperation_code_page(url_categorie)
    liste_url_livres=recuperation_liste_url_livres (soup_categorie)
    liste_all_livres.append(liste_url_livres)
print (liste_all_livres)
"""
liste_all_livres=[]
for lien_categorie in liste_liens_categories :
    url_categorie=lien_categorie
    soup_categorie=recuperation_code_page(url_categorie)
    liste_url_livres=recuperation_liste_url_livres (soup_categorie)
    for liste_livres in liste_url_livres:
        url_product=liste_livres
        dico_livres=recuperation_infos_livre (url_product)
        liste_all_livres.append(dico_livres)
print (liste_all_livres)

    
    
    


