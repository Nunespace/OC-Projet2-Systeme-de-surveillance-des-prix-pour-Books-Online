import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


url_site= "http://books.toscrape.com"

url_product = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html" # lien de la page du produit à scrapper


def recuperation_code_page(url):
    reponse = requests.get(url)
    # transforme (parse) le HTML en objet BeautifulSoup. test est ajouté pour avoir le texte et non le code 200
    soup = BeautifulSoup(reponse.text, "html.parser")
    if reponse.ok:  # cad si requests.get renvoie le code 200
        return soup

def recuperation_infos_livre (url):

    def recup_titre_livre(soup_product):
        div_titre=soup_product.find('div', class_='col-sm-6 product_main')
        for h1 in div_titre:
            titre=soup_product.find('h1').text
        return titre

    def recuperation_url_image(url_site, soup):
        div_image=soup.find('div', class_='item active')
        lien_image=div_image.find('img')
        source=lien_image['src']
        return url_site + source

    def recuperation_description_produit (soup_product):
        description=soup_product.findAll('p')
        return description[3].text

    def recuperation_categorie (soup_product):
        categorie1=soup_product.findAll('li')
        categorie1=str(categorie1[2].text)
        categorie=categorie1.strip() #supprime les blancs au début et à la fin de la catégorie
        return categorie
     
    def review_rating_extraction(soup_product):#Returns review_rating from soup_product
        review_rating_string_int_correspondance = {
        "One" : 1,
        "Two" : 2,
        "Three" : 3,
        "Four" : 4,
        "Five": 5
        }
        paragraphs_attributes = []
        paragraphs = soup_product.findAll('p')
        for paragraph in paragraphs:
            paragraphs_attributes.append(paragraph.attrs)
        for paragraphs_attribute in paragraphs_attributes:
            for key in paragraphs_attribute:
                if key == "class":
                    if paragraphs_attribute[key][0] == "star-rating":
                        review_rating_string = paragraphs_attribute[key][1]
        review_rating = review_rating_string_int_correspondance[review_rating_string]
        return review_rating  
       

    def recuperation_info_livre (dico, liste_info):
        number_available=liste_info[5]#récupération uniquement du nombre dans "number available"
        number_available="".join([i for i in number_available if not i.isalpha() and i.isalnum()])
        liste_info[5]=int(number_available)
        dico['universal_product_code(upc)']=liste_info[0]
        dico['price_excluding_tax']=liste_info[2]
        dico['price_including_tax']=liste_info[3]
        dico['number_available']=liste_info[5]
        return dico

    def liste_info(soup_product):
        liste_info=[]
        tds=soup_product.findAll('td')
        [liste_info.append(td.text) for td in tds]
        prix_ht=liste_info[2].replace('Â','') #remplacement du A devant le prix
        liste_info[2]=prix_ht
        prix_ttc=liste_info[3].replace('Â','')
        liste_info[3]=prix_ttc
        return liste_info

    soup_product=recuperation_code_page (url_product)
    liste_info=liste_info(soup_product)
    dico={'product_page_url':url_product, 'universal_product_code(upc)':'', 'title' :'', 'price_excluding_tax' : '', 'price_including_tax': '', 'number_available':'', 'product_description' : '', 'category':'', 'review_rating' : '', 'image_url':''}
    recuperation_info_livre (dico, liste_info)
    dico['title']=recup_titre_livre(soup_product)
    dico['product_description']=recuperation_description_produit (soup_product)
    dico['category']=recuperation_categorie (soup_product)
    dico['review_rating']=review_rating_extraction(soup_product)
    dico['image_url']=recuperation_url_image(url_site, soup_product)
    return dico







