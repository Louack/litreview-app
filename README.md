# Application LITReview

## DESCRIPTION
L'application LITReview permet à différents utilisateurs de demander et d'échanger des critiques littéraires.

## INSTALLATION

1. Cloner le dépôt du projet avec la commande '$ git clone clone https://github.com/Louack/OC_PP9.git' ou télécharger le fichier zip du projet à l'adresse 'https://github.com/Louack/OC_PP9/archive/refs/heads/master.zip'
2. Placer le projet dans un dossier et se rendre dans ce dossier depuis le terminal de commande
3. Créer un environnement virtuel dans ce dossier avec `$ py -m venv env` sous windows ou bien `$ python3 -m venv env` sous macos ou linux.
4. Activer l'environnement virtuel avec la commande `$ env\Scripts\activate` sous windows ou bien `$ source env/bin/activate` sous macos ou linux.
5. Installer les packages nécessaires au bon fonctionnement du projet avec la commande `$ pip install -r requirements.txt`.
6. Se placer ensuite dans le dossier 'src' et créer et effectuer les migrations vers la base de données grâce à la commande '$ py manage.py makemigrations' suivie de la commande '$ py manage.py migrate'
7. Créer un superutilisateur disposant des droits d'administration avec la commande '$ py manage.py createsuperuser'
8. Enfin lancer le serveur avec la commande '$ py manage.py runserver'. 

## UTILISATION ET FONCTIONNALITES

L'application est accessible depuis l'adresse locale 'http://127.0.0.1:8000/'
L'application propose les fonctionnalités suivantes :
* Inscription d'un nouvel utilisateur et connexion d'un utilisateur existant à l'adresse 'http://127.0.0.1:8000/auth'. Un nom d'utilisateur suivi d'un mot de passe sont demandés
* Une fois connecté, l'utilisateur est redirigé vers son flux. Le panneau de navigation situé en haut à droite permet d'accéder au différentes informations enregistrés conernant l'utilisateur
* Consultation du flux d'informations via la rubrique 'Flux' du panneau de navigation. Le flux rassemble toutes les publications de l'utilisateur ainsi que celles de ses abonnements et les réponses des non-abonnés à ses publications
* Création de demande de critique et création de critique directe sont disponibles grâce aux deux boutons situé en haut du flux. La demande de critique nécessite d'entrer un titre et optionnellement une description et une image. La création de critique nécessite l'entrée d'un titre et d'une note ainsi que d'un commentaire en option.
* Sous chaque demande de critique, un bouton de création de réponse est disponible. Une seule réponse par utilisateur est acceptée.
* Chaque publication peut être modifiée ou supprimée par son utilisateur via les boutons situés en bas à droite des publications.
* Toutes les publications de l'utilisateur sont disponibles via la rubrique 'Mes Publications' du panneau de navigation.
* La rubrique 'Mes Abonnements' du panneau de navigation permet de consulter abonnements et abonnés ainsi que suivre et se désabonner des utilisateurs du site via un menu déroulant.
* Toutes les fonctionnalités citées précédemment peuvent être effectuées par superutilisateur via l'interface d'administration accessible à l'adresse 'http://127.0.0.1:8000/admin/'

## BASE DE DONNEES FOURNIE

L'utilisateur 'Loïc' dispose des droits d'administration.
Le mot de passe attribué à tous les utilisateurs est : 'projet_django'

## GENERATION D'UN RAPPORT FLAKE8

Afin de s'assurer que le programme suit les conventions d'écriture de code PEP 8, un rapport flake8 peut être généré à tout moment dans la console grâce à la commande :

'$ flake8 my_project_folder_path'

Le fichier setup.cfg permet de configurer les préférences d'utilisation du package flake8 :
* max-line-length permet de modifier le nombre de lignes maximum (réglé sur 119 dans le fichier setup d'origine)
* si le répertoire de l'environnement virtuel est présent dans le répertoire du projet, l'exclure (exclude = my_venv_directory)