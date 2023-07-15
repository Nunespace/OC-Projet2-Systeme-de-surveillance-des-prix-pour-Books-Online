from book import *

class FileCategory:
    def __init__(self, url_category):
        self.url_category = url_category
        self.soup_category = Book(url_category).soup()

    def extraction_list_url_books(self):
        """fonction qui crée une liste des liens des livres de la catégorie (d'une page)"""
        article = self.soup_category.findAll('article', class_="product_pod")
        links_list = []
        for a_href in article:
            a = a_href.find('a')
            link = a['href']
            links_list.append("http://books.toscrape.com/catalogue/"+link[9:])
        return links_list

    def url_category_page_next(self):
        """vérifie l'existence et récupère l'url de ou des page(s) suivante(s) de la catégorie"""
        url_category_beginning = self.url_category[:-10]
        class_next = self.soup_category.find('li', attrs={'class': 'next'})
        if class_next != None:
            a = class_next.find('a')
            lien = a.get('href')  # get retourne la valeur de l'attribut "href" de la balise "a"
            return url_category_beginning + lien
        else:
            return None

        # fonction qui, pour une page, crée une liste contenant un dictionnaire par livre
    def extractionInfoBooksCategory(self):
        links_page1_category = self.extraction_list_url_books()
        list_info_one_category = []
        for link in links_page1_category:
            dict_book_info = Book(link).infoOneBook()
            list_info_one_category.append(dict_book_info)
        while self.url_category_page_next() != None:
            url_next = self.url_category_page_next()
            links_url_next = self.extraction_list_url_books()
            for link in links_url_next :
                dict_book_info = Book(link).infoOneBook()
                list_info_one_category.append(dict_book_info)
        return list_info_one_category

    def extractionHeadTitleCategory(self):
        """fonction qui récupère le titre de la page (catégorie) et le nettoie"""
        soup = self.soup_category
        head_title_raw = soup.find('h1').text
        head_title_cleaned = "".join([i for i in head_title_raw if i.isalpha() or i.isalnum() or i == ' '])
        head_title = head_title_cleaned.replace(' ', '_')
        return head_title

    def loadFileCategory(self):
        """cette fonction crée un dossier contenant un fichier CSV et les images d'une seule catégorie"""
        category_name = self.extractionHeadTitleCategory()
        directory = 'categories/' + category_name
        os.makedirs(directory, exist_ok=True)
        date = str(datetime.date.today())
        today = date.replace('-', '_')
        file = directory + '/' + "category_" + category_name + "_" + today + ".csv"
        dict_list = self.extractionInfoBooksCategory()
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


    def loadImagesCategory (self):
        links_books = self.extraction_list_url_books()
        if self.url_category_page_next() != None :
            links_books.extend(self.url_category_page_next())
        for link in links_books :
            book = Book(link)
            dict_info = book.infoOneBook()
            url_image = dict_info["image_url"]
            category = dict_info["category"]
            category_new = category.replace(" ", "_").replace("/", "_")
            directory = "categories/" + category_new + "/images"
            os.makedirs(directory, exist_ok=True)
            book_name = book.extractionHeadTitle()
            image_name = directory + "/" + book_name + ".jpg"
            f = open(image_name, "wb")  # écriture format b inaire
            response = requests.get(url_image)
            f.write(response.content)
            f.close()


"""
category1 = FileCategory("https://books.toscrape.com/catalogue/category/books/christian_43/index.html")
category1.loadFileCategory()
category1.loadImagesCategory()
"""