import requests
from bs4 import BeautifulSoup
import csv
import datetime
import os


class Book:
    nb = 0
    def __init__(self, url_book, url_site="http://books.toscrape.com"):
        self.url_book = url_book
        self.url_site = url_site

    def soup(self):
        """transforme (parse) le HTML en objet BeautifulSoup. text est ajouté pour avoir le texte et non le code 200"""
        response = requests.get(self.url_book)
        soup = BeautifulSoup(response.content, "html.parser")
        # cad si requests.get renvoie le code 200
        if response.ok:
            return soup

    def extractionBookTitle(self):
        div_title = self.soup().find("div", class_="col-sm-6 product_main")
        title = div_title.find("h1")
        return title.text

    def extractionHeadTitle(self):
        """fonction qui récupère le titre de la page (livre) et le nettoie"""
        soup = self.soup()
        head_title_raw = soup.find('h1').text
        head_title_cleaned = "".join([i for i in head_title_raw if i.isalpha() or i.isalnum() or i == ' '])
        head_title = head_title_cleaned.replace(' ', '_')
        return head_title

    def extractionUrlImage(self):
        div_image = self.soup().find("div", class_="item active")
        link_image = div_image.find("img")
        source = link_image["src"]
        src = source[5:]
        return self.url_site + src

    def extractionProductDescription(self):
        """extraction du résumé du livre"""
        description = self.soup().findAll("p")
        return description[3].string

    def extractionCategory(self):
        category1 = self.soup().findAll("li")
        category1 = str(category1[2].text)
        category = (
            category1.strip()
        )  # supprime les blancs au début et à la fin de la catégorie
        return category

    def reviewRatingExtraction(self):
        review_rating_string_int_correspondance = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
        }
        paragraphs_attributes = []
        paragraphs = self.soup().findAll("p")
        for paragraph in paragraphs:
            paragraphs_attributes.append(paragraph.attrs)
        review_rating_string = paragraphs_attributes[2]["class"][
            1
        ]  # le 3è paragraphe contient la note du livre (les autres en bas de page indiquent la note des livres déjà visités)
        review_rating = review_rating_string_int_correspondance[review_rating_string]
        return review_rating

    def productInformation(self):
        """Ici, les informations du tableau "Product Information" du bas de la page du livre sont extraites"""
        list_product_info = []
        tds = self.soup().findAll("td")
        [list_product_info.append(td.text) for td in tds]
        prix_ht = list_product_info[2].replace(
            "Â", ""
        )  # remplacement du A devant le prix
        list_product_info[2] = prix_ht
        price_including_tax = list_product_info[3].replace("Â", "")
        list_product_info[3] = price_including_tax
        number_available = list_product_info[
            5
        ]  # récupération uniquement du nombre dans "number available"
        number_available = "".join(
            [i for i in number_available if not i.isalpha() and i.isalnum()]
        )
        list_product_info[5] = int(number_available)
        return list_product_info

    def infoOneBook(self):
        dict_info = {
            "product_page_url": self.url_book,
            "universal_product_code(upc)": "",
            "title": "",
            "price_excluding_tax": "",
            "price_including_tax": "",
            "number_available": "",
            "product_description": "",
            "category": "",
            "review_rating": "",
            "image_url": "",
        }
        list_info = self.productInformation()
        dict_info["title"] = self.extractionBookTitle()
        dict_info["product_description"] = self.extractionProductDescription()
        dict_info["category"] = self.extractionCategory()
        dict_info["review_rating"] = self.reviewRatingExtraction()
        dict_info["image_url"] = self.extractionUrlImage()
        dict_info["universal_product_code(upc)"] = list_info[0]
        dict_info["price_excluding_tax"] = list_info[2]
        dict_info["price_including_tax"] = list_info[3]
        dict_info["number_available"] = list_info[5]
        Book.nb +=1
        print (Book.nb, "/1000 books")
        return dict_info






