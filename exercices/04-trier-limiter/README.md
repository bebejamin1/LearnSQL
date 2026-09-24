# Exercice 04 — Trier et limiter : ORDER BY, LIMIT, DISTINCT

> 🎯 **Objectif** : Ranger les résultats dans l'ordre voulu, faire des classements et supprimer les doublons.  
> 📚 **Notions** : `ORDER BY`, `ASC`, `DESC`, `LIMIT`, `OFFSET`, `DISTINCT`  
> ⏱️ **Durée estimée** : 30 minutes

---

## 📖 Le cours

### ORDER BY : trier les résultats

Sans instruction, la base renvoie les lignes dans un ordre qui n'est **jamais garanti** (souvent l'ordre d'insertion, mais pas toujours). Pour trier, on utilise `ORDER BY` :

```sql
SELECT colonnes FROM table
ORDER BY colonne ASC;    -- croissant : A→Z, 0→9 (c'est le choix par défaut)

SELECT colonnes FROM table
ORDER BY colonne DESC;   -- décroissant : Z→A, 9→0
```

- `ASC` = *ascending* (croissant). C'est le choix par défaut, donc on peut ne pas l'écrire.
- `DESC` = *descending* (décroissant).

### Trier sur plusieurs colonnes

```sql
ORDER BY ville, age DESC
```

trie d'abord par ville (A→Z), puis, **pour les clients d'une même ville**, par âge décroissant. Chaque colonne a son propre `ASC` / `DESC`.

### LIMIT : garder seulement les N premières lignes

```sql
SELECT nom, prix FROM produits
ORDER BY prix DESC
LIMIT 5;          -- les 5 produits les plus chers
```

`ORDER BY` + `LIMIT`, c'est **le combo des classements** : « le top 3 », « les 10 derniers inscrits »…

`OFFSET` permet de **sauter** des lignes : `LIMIT 5 OFFSET 10` veut dire « 5 lignes, en sautant les 10 premières ». C'est comme ça que fonctionnent les pages de résultats d'un site (page 1, page 2…).

### DISTINCT : supprimer les doublons

```sql
SELECT DISTINCT ville FROM clients;
```

affiche chaque ville **une seule fois**. Avec plusieurs colonnes, `DISTINCT` supprime les lignes dont **toutes** les colonnes sont identiques.

### L'ordre des mots-clés (obligatoire !)

```sql
SELECT DISTINCT colonnes
FROM table
WHERE condition
ORDER BY colonne
LIMIT n OFFSET m;
```

## 🔍 Exemples

Les produits du plus gros stock au plus petit :

```sql
SELECT nom, stock
FROM produits
ORDER BY stock DESC;
```

**Résultat :**

| nom | stock |
| --- | --- |
| Le Petit Prince | 120 |
| Harry Potter tome 1 | 80 |
| Souris sans fil | 60 |
| Lampe de bureau | 40 |
| Ballon de football | 35 |
| Clavier mécanique | 25 |
| Puzzle 1000 pièces | 22 |
| Tapis de yoga | 18 |

*… et 8 autres lignes (16 au total)*

Le texte se trie par ordre alphabétique :

```sql
SELECT prenom FROM clients ORDER BY prenom;
```

**Résultat :**

| prenom |
| --- |
| Alice |
| Bruno |
| Chloé |
| David |
| Emma |
| Fatima |
| Gabriel |
| Hugo |

*… et 7 autres lignes (15 au total)*

Les 3 clients les plus jeunes :

```sql
SELECT prenom, age
FROM clients
ORDER BY age
LIMIT 3;
```

**Résultat :**

| prenom | age |
| --- | --- |
| Emma | 19 |
| Chloé | 22 |
| Léa | 24 |

*3 lignes*

Tri sur deux colonnes : par catégorie, puis du plus cher au moins cher dans chaque catégorie :

```sql
SELECT categorie, nom, prix
FROM produits
ORDER BY categorie, prix DESC;
```

**Résultat :**

| categorie | nom | prix |
| --- | --- | --- |
| Informatique | Écran 27 pouces | 249 |
| Informatique | Clavier mécanique | 79.9 |
| Informatique | Casque audio | 59.9 |
| Informatique | Souris sans fil | 24.99 |
| Jeux | Monopoly | 29.99 |
| Jeux | Jeu d'échecs | 25 |
| Jeux | Puzzle 1000 pièces | 14.9 |
| Livres | Apprendre le SQL | 34 |

*… et 8 autres lignes (16 au total)*

Les différents statuts de commande, sans doublons :

```sql
SELECT DISTINCT statut FROM commandes;
```

**Résultat :**

| statut |
| --- |
| livrée |
| annulée |
| en cours |

*3 lignes*

## 🧠 Bon à savoir

- Tu peux trier sur une colonne **que tu n'affiches pas** : `SELECT nom FROM produits ORDER BY prix;`.
- En SQLite, les valeurs `NULL` arrivent **en premier** dans un tri croissant, et en dernier dans un tri décroissant.
- Le tri du texte suit l'ordre des caractères de l'ordinateur : les majuscules passent avant les minuscules, et les lettres accentuées comme « É » passent **après** le « z » (regarde où se range « Écran 27 pouces »).
- `ORDER BY 2` trie selon la 2ᵉ colonne du `SELECT`. C'est pratique mais moins lisible : préfère le nom de la colonne.

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| `ORDER BY` avant `WHERE` | `SELECT … FROM produits ORDER BY prix WHERE stock > 0` | `SELECT … FROM produits WHERE stock > 0 ORDER BY prix` |
| « Top 3 » sans `ORDER BY` : 3 lignes au hasard | `SELECT nom FROM produits LIMIT 3` | `SELECT nom FROM produits ORDER BY prix DESC LIMIT 3` |
| `DISTINCT` mal placé | `SELECT nom, DISTINCT ville FROM clients` | `SELECT DISTINCT ville FROM clients` |
| Virgule avant `DESC` | `ORDER BY prix, DESC` | `ORDER BY prix DESC` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 4
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 4 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/04-trier-limiter/q1.sql` pour voir le résultat de ton fichier.

### Question 1 — Du moins cher au plus cher

📄 Fichier : `q1.sql`

Affiche le nom et le prix de tous les produits, triés du **moins cher au plus cher**.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`ORDER BY prix` (croissant par défaut).

</details>

### Question 2 — Les aînés d'abord

📄 Fichier : `q2.sql`

Affiche le prénom, le nom et l'âge de tous les clients, du **plus âgé au plus jeune**.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Décroissant = `DESC`.

</details>

### Question 3 — Le podium

📄 Fichier : `q3.sql`

Affiche le nom et le prix des **3 produits les plus chers**, du plus cher au moins cher.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Trie du plus cher au moins cher, puis garde les 3 premières lignes avec `LIMIT`.

</details>

### Question 4 — Villes sans doublon

📄 Fichier : `q4.sql`

Affiche la liste des villes des clients **sans doublons**, sans la ville non renseignée (NULL), triée par ordre alphabétique.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`SELECT DISTINCT ville`, un `WHERE ville IS NOT NULL`, puis un `ORDER BY`. Respecte l'ordre des mots-clés !

</details>

### Question 5 — Tri à deux niveaux

📄 Fichier : `q5.sql`

Affiche le prénom, le nom et la ville de tous les clients, triés par **ville** (A→Z), puis par **prénom** (A→Z) pour les clients d'une même ville.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Deux colonnes dans le `ORDER BY`, séparées par une virgule : la plus importante d'abord.

</details>

### Question 6 — Top 3 Maison et Sport

📄 Fichier : `q6.sql`

Affiche le nom, la catégorie et le prix des produits des catégories `Maison` et `Sport`, du plus cher au moins cher, en ne gardant que les **3 premiers**.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Combine tout, dans l'ordre : `WHERE … IN (…)`, puis `ORDER BY … DESC`, puis `LIMIT`.

</details>

### Question 7 — Page 2

📄 Fichier : `q7.sql`

Le site affiche les produits **par pages de 5**, du moins cher au plus cher. Affiche le nom et le prix des produits de la **page 2**, c'est-à-dire les produits n°6 à 10 de ce classement.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`LIMIT 5 OFFSET 5` : 5 lignes, en sautant les 5 premières.

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 05 — Calculs, alias et fonctions](../05-calculs-fonctions/README.md)

⬅️ [Retour au sommaire](../../README.md)
