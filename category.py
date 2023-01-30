from product_informations import *

url_category_page1= "http://books.toscrape.com/catalogue/category/books/young-adult_21/index.html"
url_category_beginning=url_category_page1[:-10]

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

def category_extraction(url):
    soup_category=recuperation_code_page(url)
    links_page1_category=recuperation_liste_url_livres (soup_category)
    list_info_category=[]
    for link in links_page1_category:
        dict_book_info=recuperation_infos_livre(link)
        list_info_category.append(dict_book_info)
    #list_info_category=','.join (list_info_category)
    return list_info_category

url=url_category_page1
list_info_category= category_extraction(url)

while url_category_page_next (url)!= None:
    url=url_category_page_next (url)
    list_info_category.extend(category_extraction(url))


soup=recuperation_code_page(url_category_page1)
category_old=soup.find('h1').text
category = category_old.replace (' ', '_')
file_category =category+"2023_jan.csv"
creation_csv_file(file_category, list_info_category)
