import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

#from livre import *

url_categorie= "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

def recuperation_code_page(url):
    reponse = requests.get(url)
    # transforme (parse) le HTML en objet BeautifulSoup. test est ajouté pour avoir le texte et non le code 200
    soup = BeautifulSoup(reponse.text, "html.parser")
    if reponse.ok:  # cad si requests.get renvoie le code 200
        return soup
    
def recuperation_liste_url_livres (soup_categorie):
    soup_categorie=recuperation_code_page(url_categorie)
    article=soup_categorie.findAll('article', class_="product_pod")
    liste_liens=[]
    for a_href in article :
        a=a_href.find('a')
        lien= a['href']
        fin_lien=len(lien)
        liste_liens.append("http://books.toscrape.com/catalogue/"+lien[9:fin_lien])
    return liste_liens
    


    

    



"""
def sauvegarder(filename, l_donnees, sep=','):
    with open(filename, 'w', encoding='utf-8') as file_out:
        l_entetes = [str(e) for e in l_donnees[0]] # la liste des titres des entêtes correspondent aux clés du dictionnaire
        entetes = sep.join(l_entetes)
        file_out.write(entetes + '\n')
        for donnees in l_donnees:
            ligne = sep.join([str(donnees[cle]) for cle in l_entetes])
            file_out.write(ligne + '\n')

dico2=[recuperation_infos_livre (url_produit), {'product_page_url':url_produit, 'universal_product_code(upc)':'essai', 'title' :'ouf', 'price_excluding_tax' : '', 'price_including_tax': '', 'number_available':'', 'product_description' : '', 'category':'', 'review_rating' : '', 'image_url':''}]


sauvegarder("infos_livre.csv", dico2, sep=',')
data_frame=pd.read_csv("infos_livre.csv")
"""


