# Exercice 07 — Regrouper : GROUP BY et HAVING

> 🎯 **Objectif** : Calculer des résumés par groupe (par catégorie, par ville, par client…) et filtrer ces groupes.  
> 📚 **Notions** : `GROUP BY`, `HAVING`, `WHERE` ou `HAVING` ?, ordre d'exécution  
> ⏱️ **Durée estimée** : 40 minutes

---

## 📖 Le cours

### Le problème

Avec `COUNT(*)`, on sait combien il y a de produits **au total**. Mais comment savoir combien il y en a **par catégorie** ? On pourrait écrire 5 requêtes avec un `WHERE` différent à chaque fois… ou **une seule** avec `GROUP BY` !

### GROUP BY : faire des paquets

`GROUP BY colonne` rassemble les lignes qui ont la **même valeur** dans cette colonne pour former des **groupes**. Ensuite, les fonctions d'agrégation (`COUNT`, `SUM`, `AVG`…) calculent un résultat **par groupe**.

```sql
SELECT categorie, COUNT(*) AS nb_produits
FROM produits
GROUP BY categorie;
```

Ce qui se passe :

```
 produits (16 lignes)          GROUP BY categorie               résultat
 ────────────────────────      ──────────────────────           ─────────────────────
 Clavier    Informatique ┐
 Souris     Informatique │──►  paquet « Informatique » ──►     Informatique │ 4
 Écran      Informatique │
 Casque     Informatique ┘
 Petit P.   Livres       ┐
 SQL        Livres       │──►  paquet « Livres »       ──►     Livres       │ 3
 H. Potter  Livres       ┘
 …                              …                               …
```

### La règle d'or du GROUP BY

Dans le `SELECT`, tu ne peux mettre que :

1. les colonnes du `GROUP BY` ;
2. des fonctions d'agrégation (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).

C'est logique : une ligne de résultat = un groupe. Si tu demandes la colonne `nom`, lequel des 4 noms du groupe « Informatique » faudrait-il afficher ?

### HAVING : filtrer les groupes

- `WHERE` filtre les **lignes**, **avant** le regroupement.
- `HAVING` filtre les **groupes**, **après** le regroupement. Il peut donc utiliser `COUNT`, `SUM`…

```sql
SELECT categorie, COUNT(*) AS nb_produits
FROM produits
GROUP BY categorie
HAVING COUNT(*) >= 4;      -- seulement les catégories d'au moins 4 produits
```

| | `WHERE` | `HAVING` |
| --- | --- | --- |
| Filtre… | les lignes | les groupes |
| Quand ? | avant le `GROUP BY` | après le `GROUP BY` |
| Peut utiliser `COUNT`, `SUM`… ? | ❌ non | ✅ oui |

### L'ordre complet des mots-clés

```sql
SELECT    colonnes       -- 5. ce qu'on affiche
FROM      table          -- 1. d'où viennent les données
WHERE     condition      -- 2. on filtre les lignes
GROUP BY  colonnes       -- 3. on fait des groupes
HAVING    condition      -- 4. on filtre les groupes
ORDER BY  colonnes       -- 6. on trie
LIMIT     n;             -- 7. on coupe
```

On **écrit** les mots-clés dans cet ordre. Les numéros montrent l'ordre dans lequel la base les **exécute** : c'est pour ça qu'un `WHERE` ne peut pas utiliser un `COUNT`, puisque les groupes n'existent pas encore à ce moment-là !

## 🔍 Exemples

Le nombre de produits par catégorie :

```sql
SELECT categorie, COUNT(*) AS nb_produits
FROM produits
GROUP BY categorie;
```

**Résultat :**

| categorie | nb_produits |
| --- | --- |
| Informatique | 4 |
| Jeux | 3 |
| Livres | 3 |
| Maison | 3 |
| Sport | 3 |

*5 lignes*

Le prix le plus bas et le plus haut de chaque catégorie :

```sql
SELECT categorie, MIN(prix) AS moins_cher, MAX(prix) AS plus_cher
FROM produits
GROUP BY categorie;
```

**Résultat :**

| categorie | moins_cher | plus_cher |
| --- | --- | --- |
| Informatique | 24.99 | 249 |
| Jeux | 14.9 | 29.99 |
| Livres | 7.5 | 34 |
| Maison | 19.9 | 45 |
| Sport | 22 | 39 |

*5 lignes*

Les commandes qui contiennent au moins 3 articles (`HAVING` filtre les groupes) :

```sql
SELECT commande_id, SUM(quantite) AS nb_articles
FROM lignes_commande
GROUP BY commande_id
HAVING SUM(quantite) >= 3;
```

**Résultat :**

| commande_id | nb_articles |
| --- | --- |
| 2 | 3 |
| 5 | 3 |
| 6 | 4 |
| 9 | 3 |
| 10 | 3 |
| 11 | 3 |
| 13 | 3 |
| 14 | 3 |

*8 lignes*

`WHERE` puis `GROUP BY` : l'âge moyen par ville, en ne comptant que les clients de 25 ans et plus. Remarque le groupe `NULL` : les clients sans ville forment leur propre groupe.

```sql
SELECT ville, AVG(age) AS age_moyen
FROM clients
WHERE age >= 25
GROUP BY ville;
```

**Résultat :**

| ville | age_moyen |
| --- | --- |
| NULL | 31 |
| Bordeaux | 33 |
| Lille | 47 |
| Lyon | 42.33333333 |
| Marseille | 38 |
| Nantes | 42 |
| Paris | 31.66666667 |

*7 lignes*

Regrouper sur un calcul, puis trier : le nombre de commandes par mois :

```sql
SELECT strftime('%m', date_commande) AS mois, COUNT(*) AS nb_commandes
FROM commandes
GROUP BY mois
ORDER BY nb_commandes DESC, mois;
```

**Résultat :**

| mois | nb_commandes |
| --- | --- |
| 01 | 2 |
| 02 | 2 |
| 03 | 2 |
| 04 | 2 |
| 05 | 2 |
| 12 | 2 |
| 06 | 1 |
| 07 | 1 |

*… et 4 autres lignes (12 au total)*

## 🧠 Bon à savoir

- On peut regrouper sur **plusieurs colonnes** : `GROUP BY ville, age` fait un groupe par combinaison (ville, âge).
- Les `NULL` forment **leur propre groupe**.
- On peut trier sur un résultat d'agrégation : `ORDER BY COUNT(*) DESC` ou `ORDER BY nb_produits DESC` (avec l'alias).
- `COUNT(*)` dans un groupe = le nombre de lignes de ce groupe.

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| Fonction d'agrégation dans le `WHERE` | `WHERE COUNT(*) > 2` | `HAVING COUNT(*) > 2` |
| Colonne ni regroupée ni agrégée (SQLite affiche une valeur au hasard, les autres bases refusent) | `SELECT categorie, nom, COUNT(*) … GROUP BY categorie` | `SELECT categorie, COUNT(*) … GROUP BY categorie` |
| `HAVING` avant `GROUP BY` | `… HAVING COUNT(*) > 2 GROUP BY categorie` | `… GROUP BY categorie HAVING COUNT(*) > 2` |
| `GROUP BY` oublié : une seule ligne au lieu d'une par groupe | `SELECT categorie, COUNT(*) FROM produits` | `… FROM produits GROUP BY categorie` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 7
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 7 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/07-group-by/q1.sql` pour voir le résultat de ton fichier.

### Question 1 — Clients par ville

📄 Fichier : `q1.sql`

Affiche chaque ville et le nombre de clients qui y habitent. Ignore les clients dont la ville est inconnue (NULL).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`WHERE ville IS NOT NULL` (avant le regroupement !), puis `GROUP BY ville`.

</details>

### Question 2 — Commandes par statut

📄 Fichier : `q2.sql`

Affiche chaque statut de commande (`livrée`, `en cours`…) et le nombre de commandes qui ont ce statut.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Même structure que l'exemple des catégories, sur la table `commandes`.

</details>

### Question 3 — Stock par catégorie

📄 Fichier : `q3.sql`

Affiche chaque catégorie et son **stock total** (la somme des stocks de ses produits).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`SUM(stock)` et `GROUP BY categorie`.

</details>

### Question 4 — Prix moyen par catégorie

📄 Fichier : `q4.sql`

Affiche chaque catégorie et le prix moyen de ses produits, **arrondi à 2 décimales**, du prix moyen le plus élevé au plus bas.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`ROUND(AVG(prix), 2) AS prix_moyen`, puis `GROUP BY`, puis `ORDER BY prix_moyen DESC`.

</details>

### Question 5 — Clients fidèles

📄 Fichier : `q5.sql`

Dans la table `commandes`, affiche l'id de chaque client (`client_id`) et son nombre de commandes, uniquement pour les clients qui ont passé **au moins 2 commandes**.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`GROUP BY client_id`, puis on filtre les groupes avec `HAVING COUNT(*) >= 2`.

</details>

### Question 6 — Catégories haut de gamme

📄 Fichier : `q6.sql`

Affiche les catégories dont le produit le plus cher coûte **plus de 40 €**, avec le prix de ce produit le plus cher.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`MAX(prix)` par catégorie, et `HAVING MAX(prix) > 40`.

</details>

### Question 7 — Les meilleures ventes

📄 Fichier : `q7.sql`

Dans la table `lignes_commande`, affiche chaque `produit_id` et la **quantité totale** commandée, uniquement pour les produits commandés **au moins 4 fois** au total. Trie par quantité totale décroissante, puis par `produit_id` croissant en cas d'égalité.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`SUM(quantite) AS total`, `GROUP BY produit_id`, `HAVING SUM(quantite) >= 4`, puis `ORDER BY total DESC, produit_id`.

</details>

### Question 8 — WHERE et HAVING

📄 Fichier : `q8.sql`

En ne comptant que les commandes **livrées**, affiche l'id de chaque client (`client_id`) et son nombre de commandes livrées.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Le statut est une information de **ligne** : on le filtre avec `WHERE`, **avant** le `GROUP BY`.

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 08 — Relier les tables : JOIN](../08-jointures/README.md)

⬅️ [Retour au sommaire](../../README.md)
