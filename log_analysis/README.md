
Objectif du projet:
Ce projet consiste à analyser les journaux 
d’authentification d’un serveur Linux afin d’étudier
les tentatives de connexion SSH. Le programme 
identifie les connexions réussies et les mots de 
passe échoués, recherche le pays d’origine des 
adresses IP et génère trois graphiques pour
présenter les résultats.

Lecture et analyse :
Le fichier ingestion/raw.py :permet de lire les 
fichiers et de regrouper leurs lignes dans une seule 
liste. Les fichiers compressés sont ouverts avec gzip.
open, tandis que les autres sont lus avec open.

Le fichier processing/extract_tansforme.py :analyse 
les lignes à l’aide d’expressions régulières (re) 
pour récupérer les informations nécessaires et 
classer les tentatives en trois catégories : Success 
(connexion réussie), Failed (mot de passe incorrect) 
et Invalid (utilisateur inexistant).

Géolocalisation:
Le fichier processing/geo_location.py utilise le 
service ipinfo.io pour trouver le pays d’origine des 
adresses IP. Les résultats sont conservés dans un
cache pour éviter les requêtes répétées. Seules les
100 adresses IP les plus actives sont géolocalisées.
  
Création des graphiques:
Le fichier serving/dashboard.py utilise la 
bibliothèque matplotlib pour générer trois 
graphiques: les tentatives échouées par pays 
(failed_by_country.png), les connexions réussies par 
utilisateur (success_by_user.png) et les tentatives 
avec un utilisateur inexistant (invalid_users.png).

Lancement :
Le fichier main.py lance les différentes étapes du 
projet : lecture, analyse et création des graphiques.
Le fichier storage/app.log enregistre le déroulement
du programme et les éventuelles erreurs.

Résultats:
Le programme a détecté 14 129 tentatives de connexion 
SSH provenant de 1 906 adresses IP, dont 10 962 mots 
de passe échoués, 3 166 tentatives avec un 
utilisateur inexistant et une seule connexion réussie
avec l’utilisateur adminesisa. Les noms  d’utilisateur les plus essayés sont admin (407 
fois), esisa (193 fois) et ubuntu (144 fois).

Problèmes rencontrés et solutions:
Nous avons corrigé plusieurs problèmes, notamment le comptage des tentatives en double, la répétition des lignes concernant les utilisateurs inexistants et la lecture des fichiers gzip incomplets. L’encodage UTF-8 a également été précisé pour assurer une lecture correcte des fichiers.
