from category import *

# lien de la page à scrapper
url_site = "http://books.toscrape.com"

# fonction qui crée une liste des url de chaque catégorie
def extraction_category_links(url):
    soup = extraction_code_page(url)
    links = soup.findAll('a')
    list_links = []
    for link in links:
        list_links.append(url_site+"/"+link['href'])
    category_links = list_links[3:53]
    return category_links

# Fonction principale qui crée un dossier par catégorie contenant un fichier CSV et un sous dossier "images"
def load_file_all_books(url):
    category_links = extraction_category_links(url)
    for link in category_links:
        load_file_category(link)

load_file_all_books(url_site)
