# Introduction

Passionné de généalogie, [la base de données des personnes décédées depuis 1970 de l'INSEE](https://www.insee.fr/fr/information/4190491) est pour moi une source incontournable pour compléter les fiches des individus contemporains.

Plusieurs outils permettent de chercher dans cette base de données, notamment [ce site](https://arbre.app/insee) ([repo GitHub](https://github.com/FlorianCassayre/insee-db)) réalisé par [Florian Cassayre](https://florian.cassayre.me), et [matchID](https://deces.matchid.io/search).

Ces outils sont très puissants mais les données affichées différent parfois de celles des fichiers sources. Par exemple, dans le fichier source, une date peut être incomplète (`19350000`). Le premier outil n'affichera aucune date (on perd l'année), et le second affichera 01/01/1935 (on pense alors que la date est le 1er janvier, ce qui est faux).

De plus, les fichiers source ont parfois des informations placées au mauvais endroit, et elles sont perdues si un traitement n'est pas fait avant l'import des fichiers...

# Les fichiers source : problèmes rencontrés

Voici une liste des problèmes que j'ai jusqu'à présent rencontrés dans les fichiers source, et qui nécessite soit une modification de ceux-ci, soit un traitement supplémentaire avant l'import des données dans un système d'indexation comme Elasticsearch:

| Problème 	| Solution 	|
|-	|-	|
| Problème d'encodage des communes de naissance.<br>Des accents ont été introduits alors que la règle<br>avait l'air d'être de ne pas en mettre. 	| Modifier les communes pour rétablir les accents<br>ou supprimer les accents. 	|
| Lorsqu'une commune n'est pas connue, le champs peut<br>prendre plusieurs valeurs : une chaine vide, des tirets,<br>des points de suspension, des X, "INCONNUE", etc. 	| Tout remplacer par une chaîne vide. 	|
| Communes de naissance tronquées et retrait d'espaces<br>pour gagner de la place (limite de caractères). 	| Rétablir le nom des communes. 	|
| Une certaine personne s'est amusée à précéder un grand<br>nombre de communes étrangères par "à".<br><br>Exemple : "A ALGER" au lieu de "ALGER". 	| Supprimer les occurrences de "A " non désirées. 	|
| Dans le cas des communes de naissance fictives, il<br>arrive que l'information soit en double : code lieu<br>finissant par 990 et nom de commune "COMMUNE FICTIVE" 	| Remplacer par une chaîne vide les occurrences de<br>"COMMUNE FICTIVE". 	|
| Code pays incorrect. Exemple : IRLANDE (99136) pour<br>Coalisland, une ville située en Irlande du Nord.<br>Le code doit être ROYAUME-UNI (99132). 	| Corriger le code pays. 	|
| Lorsque la date de naissance exacte n'est pas connue,<br>une période est parfois indiquée dans le champ<br>commune de naissance. 	| Trouver les entrées où il y a ces périodes,<br>et indiquer dans le champ datenaiss le début<br>de la période, et dans le champ datenaiss_end<br>la fin de la période.<br><br>Les individus seront ainsi trouvables et la<br>période pourra être affichée. 	|
| Les dates peuvent être incomplètes, ce qui empêche<br>celles-ci d'être importées comme date dans une base.<br><br>Exemple : 19151000 ou 19740000 ou même 19470030. 	| En plus des champs de type DATE contenant<br>les dates complètes traitées comme on<br>peut (utiles pour Kibana par exemple) :<br>19151000 -> 19151001<br>19740000 -> 19740101<br>19470030 -> 19470130,<br>trois champs par date contenant les vraies<br>valeurs, ainsi qu'un champ par date qui<br>contient un tag indiquant quelle partie<br>de la date n'a pas pu être convertie.<br><br>Tous les individus peuvent ainsi être<br>trouvables lors d'une recherche par période,<br>tout en indiquant les vraies valeurs si la date<br>est partiellement inconnue. 	|
| Des milliers de doublons... 	| Supprimer les doublons.<br><br>idée : faire un hash de l'ensemble nom +<br>prénoms + dates + code lieu + pays pour<br>les détecter. 	|
