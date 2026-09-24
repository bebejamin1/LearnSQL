# Exercice 10 — Des requêtes dans les requêtes : les sous-requêtes

> 🎯 **Objectif** : Utiliser le résultat d'une requête à l'intérieur d'une autre requête.  
> 📚 **Notions** : sous-requête, sous-requête à une valeur, `IN (SELECT …)`, `NOT IN`, sous-requête dans le `FROM`  
> ⏱️ **Durée estimée** : 45 minutes

---

## 📖 Le cours

### L'idée

Une **sous-requête** est une requête `SELECT` écrite **entre parenthèses** à l'intérieur d'une autre requête. La base calcule d'abord la sous-requête, puis se sert de son résultat dans la requête principale.

Exemple : « quels clients sont plus âgés que la moyenne ? ». Il faut deux étapes :

1. calculer l'âge moyen : `SELECT AVG(age) FROM clients` → 34.67 ;
2. filtrer : `SELECT prenom FROM clients WHERE age > 34.67`.

Avec une sous-requête, on fait tout d'un coup :

```sql
SELECT prenom, age
FROM clients
WHERE age > (SELECT AVG(age) FROM clients);
```

Avantage : si les âges changent, la requête reste juste, puisqu'aucun chiffre n'est écrit « en dur ».

### 1. La sous-requête renvoie UNE valeur

On l'utilise avec `=`, `<`, `>`… comme n'importe quel nombre (voir ci-dessus).

### 2. La sous-requête renvoie une LISTE : IN

```sql
-- Les clients qui ont au moins une commande annulée
SELECT prenom, nom
FROM clients
WHERE id IN (SELECT client_id FROM commandes WHERE statut = 'annulée');
```

La sous-requête doit renvoyer **une seule colonne**. `NOT IN` veut dire « n'est pas dans la liste ».

### 3. La sous-requête dans le FROM

Le résultat d'une requête est un tableau… qu'on peut interroger comme une table ! Il faut simplement lui donner un nom (un alias) :

```sql
-- Nombre moyen d'articles par commande
SELECT AVG(nb_articles)
FROM (
    SELECT commande_id, SUM(quantite) AS nb_articles
    FROM lignes_commande
    GROUP BY commande_id
) AS par_commande;
```

C'est très utile pour faire une « moyenne de sommes » ou un « maximum de comptages » : on calcule d'abord par groupe, puis on résume.

### Sous-requête ou JOIN ?

Souvent, les deux marchent. La sous-requête est souvent plus lisible pour les questions du type « … qui ont / qui n'ont pas … ». Le `JOIN` est nécessaire quand on veut **afficher** des colonnes qui viennent de plusieurs tables.

## 🔍 Exemples

Les clients plus âgés que la moyenne :

```sql
SELECT prenom, age
FROM clients
WHERE age > (SELECT AVG(age) FROM clients);
```

**Résultat :**

| prenom | age |
| --- | --- |
| Bruno | 35 |
| David | 41 |
| Gabriel | 55 |
| Jules | 47 |
| Karim | 38 |
| Oscar | 62 |

*6 lignes*

Le produit le plus cher (la sous-requête trouve le prix maximum) :

```sql
SELECT nom, prix
FROM produits
WHERE prix = (SELECT MAX(prix) FROM produits);
```

**Résultat :**

| nom | prix |
| --- | --- |
| Écran 27 pouces | 249 |

*1 ligne*

Les clients qui ont une commande annulée :

```sql
SELECT prenom, nom
FROM clients
WHERE id IN (SELECT client_id FROM commandes WHERE statut = 'annulée');
```

**Résultat :**

| prenom | nom |
| --- | --- |
| Chloé | Bernard |
| Fatima | Richard |

*2 lignes*

Une sous-requête dans le `FROM` : le nombre moyen d'articles par commande :

```sql
SELECT ROUND(AVG(nb_articles), 2) AS moyenne_articles
FROM (
    SELECT commande_id, SUM(quantite) AS nb_articles
    FROM lignes_commande
    GROUP BY commande_id
) AS par_commande;
```

**Résultat :**

| moyenne_articles |
| --- |
| 2.22 |

*1 ligne*

## 🧠 Bon à savoir

- Toujours des **parenthèses** autour d'une sous-requête.
- On peut imbriquer des sous-requêtes dans des sous-requêtes.
- **Astuce de travail** : écris et teste d'abord la sous-requête **seule** dans la console (`python3 executer.py`), puis mets-la dans la requête principale.
- ⚠️ `NOT IN` et `NULL` : si la sous-requête renvoie un seul NULL, `NOT IN` ne renvoie plus **rien** ! Par sécurité, ajoute `WHERE colonne IS NOT NULL` dans la sous-requête.
- Pour aller plus loin : `EXISTS (sous-requête)` est vrai si la sous-requête renvoie au moins une ligne.

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| Fonction d'agrégation dans le `WHERE` | `WHERE prix > AVG(prix)` | `WHERE prix > (SELECT AVG(prix) FROM produits)` |
| Plusieurs colonnes dans une sous-requête `IN` | `WHERE id IN (SELECT * FROM commandes)` | `WHERE id IN (SELECT client_id FROM commandes)` |
| `=` avec une sous-requête qui renvoie plusieurs lignes (SQLite prend la première sans prévenir !) | `WHERE categorie = (SELECT categorie FROM produits WHERE prix > 40)` | `WHERE categorie IN (SELECT …)` |
| Parenthèses oubliées | `WHERE age > SELECT AVG(age) FROM clients` | `WHERE age > (SELECT AVG(age) FROM clients)` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 10
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 10 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/10-sous-requetes/q1.sql` pour voir le résultat de ton fichier.

### Question 1 — Plus cher que la moyenne

📄 Fichier : `q1.sql`

Affiche le nom et le prix des produits qui coûtent **plus cher que le prix moyen** de tous les produits.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`WHERE prix > (SELECT AVG(prix) FROM produits)`

</details>

### Question 2 — Le plus jeune

📄 Fichier : `q2.sql`

Affiche le prénom et l'âge du (ou des) client(s) **le(s) plus jeune(s)**, en utilisant une sous-requête.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

La sous-requête `SELECT MIN(age) FROM clients` donne l'âge minimum.

</details>

### Question 3 — Commandes en cours

📄 Fichier : `q3.sql`

Affiche le prénom et le nom des clients qui ont au moins une commande `en cours`. Utilise `IN` avec une sous-requête.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

La sous-requête renvoie les `client_id` des commandes dont le statut est `'en cours'`.

</details>

### Question 4 — Jamais commandés (le retour)

📄 Fichier : `q4.sql`

Affiche le nom des produits qui n'ont **jamais été commandés**, cette fois avec `NOT IN` et une sous-requête (pas de `JOIN`).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`WHERE id NOT IN (SELECT produit_id FROM lignes_commande)`

</details>

### Question 5 — Même catégorie

📄 Fichier : `q5.sql`

Affiche le nom et le prix des produits qui sont de la **même catégorie que la `Cafetière`** (la Cafetière comprise). N'écris pas le nom de la catégorie en dur : trouve-la avec une sous-requête.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`WHERE categorie = (SELECT categorie FROM produits WHERE nom = 'Cafetière')`

</details>

### Question 6 — Les lecteurs

📄 Fichier : `q6.sql`

Affiche le prénom et le nom des clients qui ont commandé au moins un produit de la catégorie `Livres`. Chaque client ne doit apparaître **qu'une seule fois**.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Des sous-requêtes imbriquées : les clients dont l'id est dans (les client_id des commandes dont l'id est dans (les commande_id des lignes dont le produit_id est dans (les id des produits de catégorie Livres))). Avec des `JOIN`, il faudrait un `DISTINCT` pour éviter les doublons.

</details>

### Question 7 — Panier moyen

📄 Fichier : `q7.sql`

Défi : quel est le **montant moyen d'une commande livrée**, arrondi à 2 décimales ? (Le montant d'une commande = la somme de prix × quantité de ses lignes.)

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Étape 1 (sous-requête dans le `FROM`) : calcule le montant de chaque commande livrée avec des `JOIN` et un `GROUP BY co.id`. Étape 2 : fais la moyenne de ces montants avec `ROUND(AVG(montant), 2)`.

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 11 — Modifier les données : INSERT, UPDATE, DELETE](../11-modifier-donnees/README.md)

⬅️ [Retour au sommaire](../../README.md)
