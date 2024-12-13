Web server : en python, avec Flask
--> pas d'ui, juste une API
--> att ! bien faire tourner dans le venv (appelé env) avec . env/bin/activate

Caching strategy : 

write : pas besoin dans ce cas parce que le user ne rentre jamais de données, il ne fait que les fetch vers le serveur central 
read : strategy read through (si le CDN n'a pas le fichier, il demande au serveur qui lui renvoie, il le cache et le renvoie au user)
keep in memory : LRFU : least recently-frequently used : 
- donner à chaque fichier une note entre 0 et 1 pour frequently et recently
- frequently : par rapport au nombre total de vues : faire un pourcentage
- recently : par rapport au nombre max de jours (càd depuis le fichier le + ancien) : faire un pourcentage
- donner une note en combinant les deux (peut être pondéré)
- à chaque ajout de fichier, on supprime celui qui a la moins bonne note

Where to get the file : 

DHT : Distributed Hash Table : 
Quand on veut un fichier, on le hash, puis on a une table qui lie les IP des serveurs qui possèdent le fichier en fonction de la valeur de hash (dans une plage). Avantages : on est jamais obligé de repropager la table puisqu'elle n'est pas statique. 


To get cache to run (rappel pour les debilos comme moi (eolia)): 
- run /main_server/app.py in a terminal (port 5000)
- run /replica_server/main.py in another term (port 5001)
- from a browser, go to "http://127.0.0.1:5001/ask_cache/your_image.png" 

--> Problème : avec le default.png dans le main server, quand le file n'existe pas on renvoie le default mais sans prevenir le replica que c'est pas la file demandée et du coup le replica croit que c'est toujours le bon fichier