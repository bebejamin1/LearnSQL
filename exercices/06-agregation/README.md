# Exercice 06 — Compter et résumer : COUNT, SUM, AVG, MIN, MAX

> 🎯 **Objectif** : Résumer une table en un seul chiffre : combien, quel total, quelle moyenne, quel minimum ou maximum.  
> 📚 **Notions** : fonctions d'agrégation, `COUNT(*)`, `COUNT(colonne)`, `COUNT(DISTINCT …)`, `SUM`, `AVG`, `MIN`, `MAX`  
> ⏱️ **Durée estimée** : 30 minutes

---

## 📖 Le cours

### Les fonctions d'agrégation

Jusqu'ici, chaque ligne de la table donnait une ligne de résultat. Les **fonctions d'agrégation** font l'inverse : elles prennent **plusieurs lignes** et les **résument en une seule valeur**.

```
 prix
 ──────
 79.90  ┐
 24.99  │
 249.00 │──►  SUM(prix)  ──►  722.38      (une seule ligne !)
 59.90  │
 …      ┘
```

| Fonction | Calcule | Exemple de question |
| --- | --- | --- |
| `COUNT(*)` | le nombre de **lignes** | Combien de clients ? |
| `COUNT(colonne)` | le nombre de valeurs **non NULL** dans la colonne | Combien de clients ont une ville ? |
| `COUNT(DISTINCT colonne)` | le nombre de valeurs **différentes** | Combien de catégories différentes ? |
| `SUM(colonne)` | la **somme** | Combien d'articles vendus au total ? |
| `AVG(colonne)` | la **moyenne** (*average*) | Quel est l'âge moyen ? |
| `MIN(colonne)` | la plus **petite** valeur | Quel est le prix le plus bas ? |
| `MAX(colonne)` | la plus **grande** valeur | Quel est le prix le plus haut ? |

### Avec un WHERE

Le `WHERE` s'applique **avant** le calcul : on garde d'abord les lignes qui nous intéressent, puis on résume celles qui restent.

```sql
SELECT COUNT(*) FROM produits WHERE categorie = 'Livres';   -- 3
```

### Plusieurs résumés dans la même requête

```sql
SELECT MIN(age), MAX(age), AVG(age) FROM clients;
```

## 🔍 Exemples

Combien de produits dans le catalogue ?

```sql
SELECT COUNT(*) AS nb_produits FROM produits;
```

**Résultat :**

| nb_produits |
| --- |
| 16 |

*1 ligne*

Combien d'articles ont été commandés au total ?

```sql
SELECT SUM(quantite) AS total_articles FROM lignes_commande;
```

**Résultat :**

| total_articles |
| --- |
| 40 |

*1 ligne*

L'âge du plus jeune, du plus âgé, et la moyenne :

```sql
SELECT MIN(age) AS plus_jeune, MAX(age) AS plus_age, AVG(age) AS age_moyen
FROM clients;
```

**Résultat :**

| plus_jeune | plus_age | age_moyen |
| --- | --- | --- |
| 19 | 62 | 34.66666667 |

*1 ligne*

La moyenne a beaucoup de décimales : on l'arrondit avec `ROUND` :

```sql
SELECT ROUND(AVG(age), 1) AS age_moyen FROM clients;
```

**Résultat :**

| age_moyen |
| --- |
| 34.7 |

*1 ligne*

Avec un `WHERE` : les livres seulement :

```sql
SELECT COUNT(*) AS nb_livres, AVG(prix) AS prix_moyen
FROM produits
WHERE categorie = 'Livres';
```

**Résultat :**

| nb_livres | prix_moyen |
| --- | --- |
| 3 | 16.8 |

*1 ligne*

`COUNT(*)` compte les lignes, `COUNT(ville)` ignore les NULL :

```sql
SELECT COUNT(*) AS nb_clients, COUNT(ville) AS nb_villes_renseignees
FROM clients;
```

**Résultat :**

| nb_clients | nb_villes_renseignees |
| --- | --- |
| 15 | 14 |

*1 ligne*

`COUNT(DISTINCT …)` compte les valeurs différentes :

```sql
SELECT COUNT(DISTINCT categorie) AS nb_categories FROM produits;
```

**Résultat :**

| nb_categories |
| --- |
| 5 |

*1 ligne*

## 🧠 Bon à savoir

- Les fonctions d'agrégation **ignorent les NULL** (sauf `COUNT(*)`, qui compte les lignes). `AVG(age)` fait la moyenne des âges **connus**.
- On peut mettre un **calcul** dans une fonction d'agrégation : `SUM(prix * stock)` donne la valeur totale du stock.
- `MIN` et `MAX` marchent aussi sur du texte (ordre alphabétique) et sur des dates (la plus ancienne, la plus récente).
- Sans `GROUP BY` (exercice suivant), ne mélange pas une colonne « normale » et une fonction d'agrégation : `SELECT nom, MAX(prix) FROM produits` n'a pas de sens logique (quel nom afficher ?). SQLite l'accepte, mais la plupart des autres bases le refusent.
- Les fonctions d'agrégation sont **interdites dans le WHERE** : `WHERE prix > AVG(prix)` provoque une erreur. La solution arrive à l'exercice 10 (sous-requêtes).

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| Parenthèses oubliées | `SELECT COUNT * FROM clients` | `SELECT COUNT(*) FROM clients` |
| Compter une colonne qui contient des NULL pour compter les lignes | `SELECT COUNT(email) FROM clients` (→ 12, pas 15) | `SELECT COUNT(*) FROM clients` |
| Espace entre la fonction et la parenthèse (refusé par certaines bases) | `SUM (stock)` | `SUM(stock)` |
| Fonction d'agrégation dans le `WHERE` | `WHERE COUNT(*) > 2` | `HAVING COUNT(*) > 2` (exercice 07) |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 6
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 6 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/06-agregation/q1.sql` pour voir le résultat de ton fichier.

### Question 1 — Nombre de clients

📄 Fichier : `q1.sql`

Combien y a-t-il de clients au total ? (une seule colonne, une seule ligne)

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`COUNT(*)` compte les lignes d'une table.

</details>

### Question 2 — Prix moyen

📄 Fichier : `q2.sql`

Quel est le **prix moyen** des produits, arrondi à 2 décimales ?

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`ROUND(AVG(prix), 2)` : une fonction dans une fonction.

</details>

### Question 3 — Les extrêmes

📄 Fichier : `q3.sql`

Affiche le prix du produit **le moins cher**, puis celui du **plus cher** (deux colonnes, dans cet ordre).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`MIN(prix)` et `MAX(prix)` dans le même `SELECT`, séparés par une virgule.

</details>

### Question 4 — Emails connus

📄 Fichier : `q4.sql`

Combien de clients ont renseigné leur **adresse email** ?

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`COUNT(colonne)` ne compte que les valeurs qui ne sont pas NULL.

</details>

### Question 5 — Stock total

📄 Fichier : `q5.sql`

Combien d'articles y a-t-il en stock au total, tous produits confondus ?

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Il faut **additionner** la colonne `stock` : `SUM`.

</details>

### Question 6 — Âge moyen des Parisiens

📄 Fichier : `q6.sql`

Quel est l'**âge moyen** des clients qui habitent à `Paris` ?

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`AVG(age)` avec un `WHERE ville = 'Paris'`.

</details>

### Question 7 — Villes différentes

📄 Fichier : `q7.sql`

Dans combien de villes **différentes** habitent les clients ? (une ville inconnue ne compte pas)

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`COUNT(DISTINCT ville)` : les doublons et les NULL ne sont pas comptés.

</details>

### Question 8 — Commandes livrées

📄 Fichier : `q8.sql`

Combien de commandes ont le statut `livrée` ?

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`COUNT(*)` avec un `WHERE statut = 'livrée'` (attention à l'accent !).

</details>

### Question 9 — Valeur totale du stock

📄 Fichier : `q9.sql`

Quelle est la valeur totale du stock de la boutique (la somme de prix × stock pour tous les produits), arrondie à 2 décimales ?

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

On peut calculer à l'intérieur d'un `SUM` : `SUM(prix * stock)`.

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 07 — Regrouper : GROUP BY et HAVING](../07-group-by/README.md)

⬅️ [Retour au sommaire](../../README.md)
