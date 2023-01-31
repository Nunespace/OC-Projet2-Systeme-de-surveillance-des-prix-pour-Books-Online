from product_informations import *

url_category_page1= "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"


def extraction_info_category (url):
    url_category_beginning = url[:-10]

    def url_category_page_next (url):
        soup_category = recuperation_code_page(url)
        class_next=soup_category.find('li', attrs={'class': 'next'})
        if class_next !=None:
            a=class_next.find('a')
            lien= a.get('href') #get retourne la valeur de l'attribut "href" de la balise "a"
            return url_category_beginning+lien
        else:
            return None


    def recuperation_liste_url_livres (soup_category):
        article=soup_category.findAll('article', class_="product_pod")
        links_list=[]
        for a_href in article :
            a=a_href.find('a')
            link= a['href']
            links_list.append("http://books.toscrape.com/catalogue/"+link[9:])
        return links_list

    # fonction qui, pour une page, crée une liste contenant un dictionnaire par livre
    def category_extraction(url):
        soup_category=recuperation_code_page(url)
        links_page1_category=recuperation_liste_url_livres (soup_category)
        list_info_category=[]
        for link in links_page1_category:
            dict_book_info=recuperation_infos_livre(link)
            list_info_category.append(dict_book_info)
        return list_info_category

    list_info_one_category= category_extraction(url)
    while url_category_page_next (url)!= None:
        url=url_category_page_next (url)
        list_info_one_category.extend(category_extraction(url))

    return list_info_one_category


def load_file_category (url):
    dir = extraction_head_title (url)
    date = str(datetime.date.today())
    today = date.replace('-', '_')
    dir + '/' + extraction_head_title(url) + ".jpg"
    file_category = dir + '/' +"category_" + extraction_head_title (url) + "_"+today+".csv"
    list_info_example_category=extraction_info_category(url)
    creation_csv_file(file_category, list_info_example_category)

load_file_category (url_category_page1)
