
# P9 - LitRevu Project 

Projet d'apprentissage. 
Développer une application (MVP) pour demander et écrire des revues d'articles et blivres avec Django, et suivre d'autres utilisateurs. 


## Installation 

1. Télécharger le dossier .zip 
2. Extraire les fichiers dans un dossier local dédié au projet 

3. Configurer l'environnement virtuel : `pipenv install` 
4. Lancer l'environnement virtuel : `pipenv shell` 
5. Démarrer le serveur Django : `pipenv run python manage.py runserver` 
6. Effectuer les migrations :    
    Depuis le terminal, dans le dossier du projet 'litrevu', appeler la commande `commands/createsuperusermigrate_pipenv` 

7. Créer un superutilisateur :    
    71. Depuis le terminal, dans le dossier du projet 'litrevu', appeler la commande `commands/createsuperuser` 
    72. Répondre aux questions :    
        * Username 
        * Mail (facultatif) 
        * Mot de passe 
        * Confirmation du mot de passe 
    73. Visiter l'adresse http://localhost:8000/admin/ pour tester l'interface d'administration, avec les informations de connexion du superutilisateur créé. 

8. Visiter l'adresse http://localhost:8000/home/ pour tester l'application côté utilisateurs. 


## Autres 

### Créer un utilisateur depuis la console 

1.  Ouvrir une console python :    
`python manage.py shell`    

2.  Taper le code pour créer l'utilisateur : 
`from django.contrib.auth.models import User` 
`User.objects.create_user(username='<nom_user>', password='<mdp>')` 

La métohde `save()` hashe le mdp avant de l'enregistrer. 

3.  Vérifier dans l'itf web qu'il est bien créé. 


## Commandes utiles 

Ouvrir le fichier de commande désiré pour vérifier le script (avec / sans Docker, nom du container, chemin de manage.py, nom de l'app à créer...) 

Lancer une commande à partir du dossier `litrevu`. 

`./commands/migrate_pipenv` ou `./commands/migrate_docker` pour effectuer les migrations et mettre à jour la BDD. 
`./commands/install` (pour installer un package ou module Python) 
`./commands/startapp` (pour installer une application Django) 

