from product_informations import *

# example d'url pour une catégorie de livre
url_category_page1 = "http://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html"

# Cette fonction crée une liste de dictionnaires contenant les informations de chaque livre de la catégorie: un dictionnaire par livre
def extraction_info_category(url):
    url_category_beginning = url[:-10]

    # vérifie l'existence et récupère l'url de ou des page(s) suivante(s) de la catégorie
    def url_category_page_next(url):
        soup_category = extraction_code_page(url)
        class_next = soup_category.find('li', attrs={'class': 'next'})
        if class_next != None:
            a = class_next.find('a')
            lien = a.get('href')  # get retourne la valeur de l'attribut "href" de la balise "a"
            return url_category_beginning+lien
        else:
            return None

    # fonction qui crée une liste des liens des livres de la catégorie
    def extraction_list_url_books(soup_category):
        article = soup_category.findAll('article', class_="product_pod")
        links_list = []
        for a_href in article:
            a = a_href.find('a')
            link = a['href']
            links_list.append("http://books.toscrape.com/catalogue/"+link[9:])
        return links_list

    # fonction qui, pour une page, crée une liste contenant un dictionnaire par livre
    def extraction_info_books_category(url):
        soup_category = extraction_code_page(url)
        links_page1_category = extraction_list_url_books(soup_category)
        list_info_one_category = []
        for link in links_page1_category:
            dict_book_info = extraction_book_info(link)
            list_info_one_category.append(dict_book_info)
        return list_info_one_category

    list_info_one_category = extraction_info_books_category(url)
    while url_category_page_next(url) != None:
        url = url_category_page_next(url)
        list_info_one_category.extend(extraction_info_books_category(url))
    return list_info_one_category

# cette fonction crée un dossier contenant un fichier CSV et les images d'une seule catégorie
def load_file_category(url):
    category = extraction_head_title(url)
    directory = 'categories/' + category
    os.makedirs(directory, exist_ok=True)
    date = str(datetime.date.today())
    today = date.replace('-', '_')
    directory + '/' + extraction_head_title(url) + ".jpg"
    file_category = directory + '/' + "category_" + extraction_head_title(url) + "_" + today + ".csv"
    list_info_one_category = extraction_info_category(url)
    creation_csv_file(file_category, list_info_one_category)

#  pour exécuter la fonction : retirer le # de la ligne suivante
# load_file_category(url_category_page1)
