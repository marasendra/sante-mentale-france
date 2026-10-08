# La santé mentale en France a de multiples visages

**Équipe :** Marie-Ange RASENDRA  
**Mail(s) de contact:** ma.rasendra@gmail.com  
**Défi :** Défi 1 — Santé mentale 

## Question

En 2023, plus de 90 000 séjours hospitaliers et près de 9 000 décès par suicide ont été recensés en France (métropole et DROM). Ce dashboard croise les hospitalisations, les suicides et le Baromètre de Santé publique France
pour répondre à une question : quels profils de personnes sont les plus touchés ?

## Visualisation

Vous pouvez consulter la visualisation via le [site](https://marasendra.github.io/sante-mentale-france/) ou télécharger le `index.html` associé.

Au début de la visualisation il y a une animation de boules qui tombent pour former un barchart. Une boule tombe pour chaque décès ou séjour hospitalier. Elle rappelle que chaque chiffre est une histoire, et elle montre l'ampleur du phénomène. Pour celles et ceux qui traversent une période difficile, le dashboard rappelle qu'ils ne sont pas seuls et renvoie vers le 3114.

L'objectif de ce rapport est d'identifier les groupes de personnes les plus à risque en France (métropolitaine et DROM).


## Les données utilisées

| Source | Jeu de données | Lien |
|---|---|---|
| Odissé | Suicides : Moyens utilisés (France) | https://odisse.santepubliquefrance.fr/explore/assets/suicides-moyens-utilises-france/ |
| Odissé | Suicides : Décès (France) | https://odisse.santepubliquefrance.fr/explore/assets/suicides-deces-france/ |
| Odissé | Gestes auto-infligés : Patients hospitalisés (France) | https://odisse.santepubliquefrance.fr/explore/assets/gestes-auto-infliges-patients-hospitalises-france/ |
| Odissé | Gestes auto-infligés : Moyens utilisés ayant mené à une hospitalisation (France) | https://odisse.santepubliquefrance.fr/explore/assets/gestes-auto-infliges-moyens-utilises-ayant-mene-a-une-hospitalisation-france/ |
| Odissé | Gestes auto-infligés : Patients hospitalisés (Région) | https://odisse.santepubliquefrance.fr/explore/assets/gestes-auto-infliges-patients-hospitalises-region/ |
| Odissé | Suicides : Décès (Région) | https://odisse.santepubliquefrance.fr/explore/assets/suicides-deces-region/ |
| Odissé | Changement climatique : Indicateurs du Baromètre de Santé publique France 2024 | https://odisse.santepubliquefrance.fr/explore/assets/changement-climatique-indicateurs-du-barometre-2024/ |
| Odissé | Santé mentale : Episodes dépressifs caractérisés dans les 12 derniers mois (France) | https://odisse.santepubliquefrance.fr/explore/assets/sante-mentale-episodes-depressifs-caracterises-dans-les-12-derniers-mois_fra/ |
| Odissé | Santé mentale : Pensées suicidaires et tentatives de suicide (France) | https://odisse.santepubliquefrance.fr/explore/assets/sante-mentale-pensees-suicidaires-et-tentatives-de-suicide_fra/ |
| Odissé | Conduites suicidaires : Indicateurs du Baromètre de Santé publique France 2024 | https://odisse.santepubliquefrance.fr/explore/assets/conduites-sucidaires-indicateurs-du-barometre-2024/ |
| Odissé | Trouble anxieux généralisé : Indicateurs du Baromètre de Santé publique France 2024 | https://odisse.santepubliquefrance.fr/explore/assets/trouble-anxieux-generalise-indicateurs-du-barometre-2024/ |

## Les outils employés

J'ai réalisé la partie data cleaning, preprocessing et exploration en Python 3.11 avec les librairies matplotlib, seaborn et pyWaffle sur VSCode.

Toute la partie sélection des charts et storytelling a été réalisée par mes soins.

J'ai utilisé l'aide de l'IA Claude d'Anthropic pour générer le fichier `index.html`.

## Licence

Ce projet est publié sous licence MIT.