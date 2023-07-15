from fileCategory import *

# lien de la page à scrapper
url_site = "http://books.toscrape.com"


def extraction_category_links(url):
    # fonction qui crée une liste des url de chaque catégorie
    soup = Book(url).soup()
    links = soup.findAll('a')
    list_links = []
    for link in links:
        list_links.append(url_site+"/"+link['href'])
    category_links = list_links[3:53]
    return category_links


def load_file_all_books(url):
    # Fonction principale qui crée un dossier par catégorie contenant un fichier CSV et un sous dossier "images"
    category_links = extraction_category_links(url)
    for link in category_links:
        category=FileCategory(link)
        category.loadFileCategory()
        category.loadImagesCategory()

load_file_all_books(url_site)
