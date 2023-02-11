import requests
from bs4 import BeautifulSoup
import csv
import datetime
import os

url_site = "http://books.toscrape.com"

# example d'un url d'une page décrivant un livre
url_product = "http://books.toscrape.com/catalogue/red-hoodarsenal-vol-1-open-for-business-red-hoodarsenal-1_729/index.html"  # lien de la page du produit à scrapper

# initialisation d'une variable pour compter les livres lors du scrapping
nb = 0

#  fonction pour récupérer (parser) le code HTML d'une page web
def extraction_code_page(url):
    response = requests.get(url)
    # transforme (parse) le HTML en objet BeautifulSoup. text est ajouté pour avoir le texte et non le code 200
    soup = BeautifulSoup(response.content, "html.parser")
    if response.ok:  # cad si requests.get renvoie le code 200
        return soup

# Cette fonction récupère toutes les informations d'un livre
def extraction_book_info(url):

    global nb

    def extraction_book_title(soup):
        div_title = soup.find('div', class_='col-sm-6 product_main')
        title = div_title.find('h1')
        return title.text

    def extraction_url_image(url, soup):
        div_image = soup.find('div', class_='item active')
        link_image = div_image.find('img')
        source = link_image['src']
        src = source[5:]
        return url + src

    def extraction_product_description(soup):
        description = soup.findAll('p')
        return description[3].string

    def extraction_category(soup):
        category1 = soup.findAll('li')
        category1 = str(category1[2].text)
        category = category1.strip()  # supprime les blancs au début et à la fin de la catégorie
        return category
     
    def review_rating_extraction(soup):
        review_rating_string_int_correspondance = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        paragraphs_attributes = []
        paragraphs = soup.findAll('p')
        for paragraph in paragraphs:
            paragraphs_attributes.append(paragraph.attrs)
        review_rating_string = paragraphs_attributes[2]['class'][1]  # le 3è paragraphe contient la note du livre (les autres en bas de page indiquent la note des livres déjà visités)
        review_rating = review_rating_string_int_correspondance[review_rating_string]
        return review_rating  

# Ici, les informations du tableau "Product description" du bas de la page sont extraites
    def product_information(soup):
        list_product_info = []
        tds = soup.findAll('td')
        [list_product_info.append(td.text) for td in tds]
        prix_ht = list_product_info[2].replace('Â', '')  # remplacement du A devant le prix
        list_product_info[2] = prix_ht
        price_including_tax = list_product_info[3].replace('Â', '')
        list_product_info[3] = price_including_tax
        number_available = list_product_info[5]  # récupération uniquement du nombre dans "number available"
        number_available = "".join([i for i in number_available if not i.isalpha() and i.isalnum()])
        list_product_info[5] = int(number_available)
        return list_product_info

    def load_image(url_image):
        category = dict_info['category']
        category_new = category.replace(' ', '_').replace('/', '_')
        directory = 'categories/' + category_new + '/images'
        os.makedirs(directory, exist_ok=True)
        image_name = directory+'/'+extraction_head_title(url)+".jpg"
        f = open(image_name, 'wb')  # écriture format b inaire
        response = requests.get(url_image)
        f.write(response.content)
        f.close()

    soup_product = extraction_code_page(url)
    dict_info = {'product_page_url': url, 'universal_product_code(upc)': '', 'title': '', 'price_excluding_tax': '', 'price_including_tax': '', 'number_available': '', 'product_description': '', 'category': '', 'review_rating': '', 'image_url': ''}
    list_info = product_information(soup_product)
    dict_info['title'] = extraction_book_title(soup_product)
    dict_info['product_description'] = extraction_product_description(soup_product)
    dict_info['category'] = extraction_category(soup_product)
    dict_info['review_rating'] = review_rating_extraction(soup_product)
    dict_info['image_url'] = extraction_url_image(url_site, soup_product)
    dict_info['universal_product_code(upc)'] = list_info[0]
    dict_info['price_excluding_tax'] = list_info[2]
    dict_info['price_including_tax'] = list_info[3]
    dict_info['number_available'] = list_info[5]
    image_url = dict_info['image_url']
    nb += 1
    print(nb, "/1000 books")
    load_image(image_url)
    return dict_info


# fonction pour charger les données dans un fichier csv à partir d'une liste de dictionnaires
def creation_csv_file(file, dict_list):
    with open(file, 'w', encoding="UTF-8") as file:
        writer = csv.writer(file, delimiter=',')
        headers = []
        for key in dict_list[0]:
            headers.append(key)
        writer.writerow(headers)
        for infos_book in dict_list:
            list_info = []
            for key in infos_book:
                list_info.append(infos_book[key])
            writer.writerow(list_info)


# fonction qui récupère le titre de la page : book ou category
def extraction_head_title(url):
    soup = extraction_code_page(url)
    head_title_raw = soup.find('h1').text
    head_title_cleaned = "".join([i for i in head_title_raw if i.isalpha() or i.isalnum() or i == ' '])
    head_title = head_title_cleaned.replace(' ', '_')
    return head_title

# fonction qui sert à créer un fichier .csv pour un seul livre
def load_file_one_book(url):
    dict_one_book = [extraction_book_info(url)]
    date = str(datetime.date.today())
    today = date.replace('-', '_')
    file_book = extraction_head_title(url) + "_" + today + ".csv"
    creation_csv_file(file_book, dict_one_book)

#  pour exécuter la fonction : retirer le # la ligne suivante
#  load_file_one_book(url_product)
