# Système de surveillance des prix pour Books Online
***
_Système de surveillance des prix limité à un seul revendeur en ligne : Books to Scrape_




## Fonctionnalités de l'application

Cette application permet de récupérer les informations suivantes de chaque livre mis en vente sur le site [books.toscrape.com](books.toscrape.com) : 

* product_page_url
* universal_ product_code (upc)
* title
* price_including_tax
* price_excluding_tax
* number_available
* product_description
* category
* review_rating
* image_url

L'application enregistre toutes ces données dans des fichiers .csv et les classe par catégorie de livres. Les images associées aux livres sont également téléchargées et classées dans le dossier de la catégorie concernée. 


## Prérequis

**Python** doit être préalablement installé.

Si vous travaillez dans un environnement Linux ou MacOS : Python est en principe déjà installé. Pour le vérifier, ouvrez votre terminal et tapez : `python --version` ou `python3 --version`


Si Python n'est pas installé, vous pouvez le télécharger à l'adresse suivante : 
[Télécharger Python3](https://www.python.org/downloads)

Vous aurez aussi besoin de l'installateur de paquets de Python **pip** qui est compris par défaut si vous disposez d'une version de Python >= 3.4. Vous pouvez vérifier qu'il est disponible via votre ligne de commande, en saisissant : `pip --version`

Vous aurez aussi besoin de Git pour cloner l'application sur votre ordinateur. Vérifier son installation en tapant   `git --version`

Sinon, choisissez et téléchargez la version de Git qui correspond à votre installation : MacOS, Windows ou Linux/Unix en cliquant sur le lien suivant : [télécharger git](https://git-scm.com/downloads)

 <sub>Puis exécutez le fichier que vous venez de télécharger. Appuyez sur _Suivant_ à chaque fenêtre puis sur _Installer_. Lors de l’installation, laissez toutes les options par défaut, elles conviennent bien. 
Git Bash est l’interface permettant d’utiliser Git en ligne de commande.


## Installation

1. Ouvrez le terminal et tapez :


```
$ git clone https://github.com/Nunespace/Projet2.git
```

2. Placez-vous dans le répertoire Projet2 :

```
$ CD Projet2
ou
$ CD chemin .../Projet2
```

3. Créez votre environnement virtuel : 

```
python3 -m venv env 
```

ou[^1]

```
python -m venv env 
```

> sous mac ou Linux :

```
$ source env/bin/activate  
```

> sous Windows, la commande sera :

```
$ env/Scripts/activate.bat
```

5. Puis installez les paquets Python répertoriés dans le fichier requirements.txt :

```
$ pip install -r requirements.txt
```

6. Enfin, **lancez le programme** en tapant : 

```
$ python3 all_products.py
ou
$ python all_products.py
```
Pour lire les fichiers .csv avec Excel, il est conseillé de les ouvrir via l'onglet _Données_ en cliquant sur _A partir d'un fichier texte/CSV_

[^1]: selon la version de Python installée sur votre PC.
