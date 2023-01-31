from category import *

url_site= "http://books.toscrape.com"

def extraction_category_links (url):
    soup = recuperation_code_page(url)
    links=soup.findAll('a') #class_="side_categories")
    list_links=[]
    for link in links:
        list_links.append (url_site+"/"+link['href'])
        category_links=list_links[3:53]
    return category_links

def load_file_all_books (url):
    category_links=extraction_category_links(url)
    for link in category_links:
        extraction_info_category(link)
        file_category = "category_" + extraction_head_title(link) + "_2023_02.csv"
        list_info_category = extraction_info_category(link)
        creation_csv_file(file_category, list_info_category)

load_file_all_books(url_site)
