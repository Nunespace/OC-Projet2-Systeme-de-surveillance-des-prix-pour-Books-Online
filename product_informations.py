import requests
from bs4 import BeautifulSoup
import csv


url_site= "http://books.toscrape.com"

url_product = "http://books.toscrape.com/catalogue/the-art-of-not-breathing_58/index.html" # lien de la page du produit à scrapper


def recuperation_code_page(url):
    reponse = requests.get(url)
    # transforme (parse) le HTML en objet BeautifulSoup. text est ajouté pour avoir le texte et non le code 200
    soup = BeautifulSoup(reponse.content, "html.parser")
    if reponse.ok:  # cad si requests.get renvoie le code 200
        return soup


def recuperation_infos_livre (url):

    def recup_titre_livre(soup_product):
        div_titre=soup_product.find('div', class_='col-sm-6 product_main')
        for h1 in div_titre:
            titre=soup_product.find('h1').text
        return titre


    def recuperation_url_image(url_site, soup_product):
        div_image=soup_product.find('div', class_='item active')
        lien_image=div_image.find('img')
        source=lien_image['src']
        src= source[5:]
        return url_site + src

    def recuperation_description_produit (soup_product):
        description=soup_product.findAll('p')
        return description[3].string

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
        review_rating_string = paragraphs_attributes[2]['class'][1] # le 3è paragraphe contient la note du livre (les autres en bas de page indiquent la note des livres déjà visités)
        review_rating = review_rating_string_int_correspondance[review_rating_string]
        return review_rating  

       

    def product_information (dico):
        liste_info=[]
        tds=soup_product.findAll('td')
        [liste_info.append(td.text) for td in tds]
        prix_ht=liste_info[2].replace('Â','') #remplacement du A devant le prix
        liste_info[2]=prix_ht
        price_including_tax=liste_info[3].replace('Â','')
        liste_info[3]=price_including_tax
        number_available = liste_info[5]  # récupération uniquement du nombre dans "number available"
        number_available = "".join([i for i in number_available if not i.isalpha() and i.isalnum()])
        liste_info[5] = int(number_available)
        dico['universal_product_code(upc)'] = liste_info[0]
        dico['price_excluding_tax'] = liste_info[2]
        dico['price_including_tax'] = liste_info[3]
        dico['number_available'] = liste_info[5]
        return dico

    soup_product=recuperation_code_page (url)
    dico={'product_page_url':url, 'universal_product_code(upc)':'', 'title' :'', 'price_excluding_tax' : '', 'price_including_tax': '', 'number_available':'', 'product_description' : '', 'category':'', 'review_rating' : '', 'image_url':''}
    dico=product_information(dico)
    dico['title']=recup_titre_livre(soup_product)
    dico['product_description']=recuperation_description_produit (soup_product)
    dico['category']=recuperation_categorie (soup_product)
    dico['review_rating']=review_rating_extraction(soup_product)
    dico['image_url']=recuperation_url_image(url_site, soup_product)
    return dico

# fonction pour charger les données dans un fichier csv à partir d'une liste de dictionnaires
def creation_csv_file(file, dict_list):
    with open(file, 'w', encoding="UTF-8") as file:
        writer = csv.writer(file, delimiter=',')
        headers = []
        for key in dict_list[0]:
            headers.append(key)
        writer.writerow(headers)
        for infos_book in dict_list :
            list_info = []
            for key in infos_book:
                list_info.append(infos_book[key])
            writer.writerow(list_info)

dict_one_book = [recuperation_infos_livre (url_product)]
file_book ='book_informations_2023_jan.csv'
creation_csv_file(file_book, dict_one_book)


















