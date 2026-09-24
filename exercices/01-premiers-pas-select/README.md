# Exercice 01 — Premiers pas : SELECT

> 🎯 **Objectif** : Comprendre ce qu'est une base de données et lire le contenu d'une table.  
> 📚 **Notions** : base de données, table, ligne, colonne, `SELECT`, `FROM`, `*`  
> ⏱️ **Durée estimée** : 20 à 30 minutes

---

## 📖 Le cours

### C'est quoi une base de données ?

Une **base de données**, c'est un endroit où l'on range des informations de façon organisée. Imagine un classeur Excel très rigoureux :

- la base contient plusieurs **tables** (comme les onglets d'un classeur) ;
- chaque table a des **colonnes** : le *type* d'information (nom, prix, âge…) ;
- chaque table contient des **lignes** : un *élément* (un client, un produit…).

Voici par exemple le début de la table `produits` de notre boutique :

| id | nom | categorie | prix | stock |
| --- | --- | --- | --- | --- |
| 1 | Clavier mécanique | Informatique | 79.9 | 25 |
| 2 | Souris sans fil | Informatique | 24.99 | 60 |
| 3 | Écran 27 pouces | Informatique | 249 | 8 |

→ 5 colonnes (`id`, `nom`, `categorie`, `prix`, `stock`) et une ligne par produit.

### C'est quoi SQL ?

**SQL** (*Structured Query Language*, prononcé « S-Q-L » ou « sequel ») est le langage qui permet de **parler à une base de données**. Tu écris une **requête** (une question), la base te répond avec un **résultat** (un tableau).

SQL est utilisé partout : sites web, applis mobiles, banques, jeux vidéo, analyse de données… Ici on utilise **SQLite**, une version légère de SQL. Ce que tu apprends marche presque à l'identique avec MySQL, PostgreSQL, SQL Server, etc.

### La base de ce cours : une boutique en ligne

Tous les exercices utilisent la même base, qui contient 4 tables :

| Table | Contient | Colonnes |
| --- | --- | --- |
| `clients` | les clients de la boutique | id, prenom, nom, ville, age, email, date_inscription |
| `produits` | les produits vendus | id, nom, categorie, prix, stock |
| `commandes` | les commandes passées | id, client_id, date_commande, statut |
| `lignes_commande` | le détail de chaque commande : quel produit, en quelle quantité | id, commande_id, produit_id, quantite |

👉 Tout le contenu de la base est visible dans [base/README.md](../../base/README.md). Garde-le ouvert à côté, c'est pratique !

### Ta première requête : SELECT … FROM …

Pour **lire** des données, on utilise `SELECT` (« sélectionne ») et `FROM` (« depuis ») :

```sql
SELECT colonne1, colonne2
FROM nom_de_la_table;
```

- après `SELECT` : les colonnes que tu veux voir, **séparées par des virgules** ;
- après `FROM` : la table dans laquelle chercher ;
- le `;` termine la requête (comme le point à la fin d'une phrase).

Pour afficher **toutes** les colonnes, on utilise l'étoile `*` (qui veut dire « tout ») :

```sql
SELECT * FROM nom_de_la_table;
```

## 🔍 Exemples

Afficher le prénom et l'âge de tous les clients :

```sql
SELECT prenom, age
FROM clients;
```

**Résultat :**

| prenom | age |
| --- | --- |
| Alice | 28 |
| Bruno | 35 |
| Chloé | 22 |
| David | 41 |
| Emma | 19 |
| Fatima | 30 |
| Gabriel | 55 |
| Hugo | 26 |

*… et 7 autres lignes (15 au total)*

Afficher toutes les colonnes de la table `lignes_commande` :

```sql
SELECT * FROM lignes_commande;
```

**Résultat :**

| id | commande_id | produit_id | quantite |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 2 | 1 |
| 3 | 2 | 5 | 2 |
| 4 | 2 | 7 | 1 |
| 5 | 3 | 6 | 1 |
| 6 | 4 | 3 | 1 |
| 7 | 5 | 3 | 2 |
| 8 | 5 | 8 | 1 |

*… et 21 autres lignes (29 au total)*

Les colonnes s'affichent **dans l'ordre où tu les écris** :

```sql
SELECT age, prenom FROM clients;
```

**Résultat :**

| age | prenom |
| --- | --- |
| 28 | Alice |
| 35 | Bruno |
| 22 | Chloé |
| 41 | David |
| 19 | Emma |
| 30 | Fatima |
| 55 | Gabriel |
| 26 | Hugo |

*… et 7 autres lignes (15 au total)*

## 🧠 Bon à savoir

- **Majuscules** : SQL ne fait pas la différence entre `SELECT`, `select` ou `Select`. Par convention, on écrit les **mots-clés SQL en MAJUSCULES** et les noms de tables et de colonnes en minuscules : c'est plus lisible.
- **Retours à la ligne** : tu peux écrire une requête sur une seule ligne ou sur plusieurs, c'est pareil pour SQL. Sur plusieurs lignes, c'est plus lisible quand la requête grandit.
- **Commentaires** : tout ce qui suit `--` sur une ligne est ignoré par SQL. Pratique pour prendre des notes :

  ```sql
  -- Ceci est un commentaire
  SELECT nom FROM produits; -- celui-ci aussi
  ```

- **Explorer la base** : lance `python3 executer.py` puis tape `.tables` (liste des tables) ou `.schema produits` (colonnes de la table `produits`).
- **Pas d'accents dans les noms de colonnes** : c'est `prenom` et `categorie`, pas `prénom` ni `catégorie`. En revanche, les *données* peuvent contenir des accents (`'Chloé'`).
- Dans la vraie vie, `SELECT *` est pratique pour découvrir une table, mais on préfère choisir ses colonnes : c'est plus clair et plus rapide.

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| Virgule en trop avant `FROM` | `SELECT nom, prix, FROM produits;` | `SELECT nom, prix FROM produits;` |
| Virgule oubliée entre deux colonnes | `SELECT nom prix FROM produits;` (pas d'erreur, mais la colonne `nom` s'affiche sous le titre « prix » !) | `SELECT nom, prix FROM produits;` |
| Faute de frappe dans le nom de la table | `SELECT nom FROM produit;` | `SELECT nom FROM produits;` |
| Accent dans un nom de colonne | `SELECT prénom FROM clients;` | `SELECT prenom FROM clients;` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 1
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 1 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/01-premiers-pas-select/q1.sql` pour voir le résultat de ton fichier.

### Question 1 — Tout le catalogue

📄 Fichier : `q1.sql`

Affiche **toutes les colonnes** de la table `produits`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Utilise l'étoile `*` juste après `SELECT` pour dire « toutes les colonnes », puis `FROM produits`.

</details>

### Question 2 — Nom et prix

📄 Fichier : `q2.sql`

Affiche uniquement le **nom** et le **prix** de tous les produits (dans cet ordre : le nom, puis le prix).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Écris les deux colonnes après `SELECT`, séparées par une virgule : `SELECT colonne1, colonne2 FROM …`

</details>

### Question 3 — Carnet d'adresses

📄 Fichier : `q3.sql`

Affiche le **prénom**, le **nom** et la **ville** de tous les clients (dans cet ordre).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

La table s'appelle `clients`. Attention, la colonne du prénom s'écrit `prenom`, sans accent.

</details>

### Question 4 — Toutes les commandes

📄 Fichier : `q4.sql`

Affiche toutes les colonnes de la table `commandes`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Même principe que la question 1, avec une autre table.

</details>

### Question 5 — L'ordre compte

📄 Fichier : `q5.sql`

Affiche la **ville** puis le **prénom** de tous les clients (attention : la ville en premier !).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Les colonnes apparaissent dans l'ordre où tu les écris après `SELECT`.

</details>

### Question 6 — État des stocks

📄 Fichier : `q6.sql`

Affiche le **nom**, la **catégorie** et le **stock** de tous les produits (dans cet ordre).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

La colonne de la catégorie s'appelle `categorie` (sans accent).

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 02 — Filtrer avec WHERE](../02-filtrer-where/README.md)

⬅️ [Retour au sommaire](../../README.md)
