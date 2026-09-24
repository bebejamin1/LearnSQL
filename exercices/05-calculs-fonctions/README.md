# Exercice 05 — Calculs, alias et fonctions

> 🎯 **Objectif** : Faire des calculs, renommer les colonnes et transformer du texte ou des dates.  
> 📚 **Notions** : `+ - * /`, `AS`, `ROUND`, `UPPER`, `LOWER`, `LENGTH`, `SUBSTR`, `||`, `strftime`  
> ⏱️ **Durée estimée** : 40 minutes

---

## 📖 Le cours

### Faire des calculs dans un SELECT

SQL sait calculer ! Tu peux utiliser `+`, `-`, `*` (multiplier) et `/` (diviser) directement sur les colonnes :

```sql
SELECT nom, prix * stock FROM produits;
```

Le calcul est fait **pour chaque ligne**.

### AS : renommer une colonne (un « alias »)

Le résultat d'un calcul porte un nom peu lisible (`prix * stock`). Avec `AS`, on lui donne un nom :

```sql
SELECT nom, prix * stock AS valeur_stock FROM produits;
```

Conseil : pas d'espace ni d'accent dans un alias. Utilise `_` pour séparer les mots.

### Les fonctions

Une **fonction** reçoit une ou plusieurs valeurs entre parenthèses et renvoie un résultat :

| Fonction | Rôle | Exemple | Résultat |
| --- | --- | --- | --- |
| `ROUND(x, n)` | arrondit x à n décimales | `ROUND(3.14159, 2)` | `3.14` |
| `UPPER(t)` | met en MAJUSCULES | `UPPER('Paris')` | `'PARIS'` |
| `LOWER(t)` | met en minuscules | `LOWER('Paris')` | `'paris'` |
| `LENGTH(t)` | compte les caractères | `LENGTH('Lyon')` | `4` |
| `SUBSTR(t, début, n)` | extrait n caractères à partir de la position début | `SUBSTR('Bonjour', 1, 3)` | `'Bon'` |
| `ABS(x)` | valeur absolue | `ABS(-5)` | `5` |

### || : coller des textes (concaténation)

L'opérateur `||` (deux barres verticales, **AltGr + 6** sur un clavier AZERTY) colle des textes bout à bout :

```sql
SELECT prenom || ' habite à ' || ville FROM clients;
-- Alice habite à Paris
```

### Les dates : strftime

`strftime(format, date)` extrait une partie d'une date :

| Format | Donne | Avec `'2024-03-18'` |
| --- | --- | --- |
| `'%Y'` | l'année | `'2024'` |
| `'%m'` | le mois | `'03'` |
| `'%d'` | le jour | `'18'` |
| `'%Y-%m'` | l'année et le mois | `'2024-03'` |

⚠️ `strftime` renvoie du **texte** : on compare avec `'03'`, pas avec `3`.
Et `date('now')` donne la date du jour.

### Les calculs marchent partout

Un calcul ou une fonction peut aussi servir dans le `WHERE` ou le `ORDER BY` :

```sql
SELECT nom, prix * stock AS valeur_stock
FROM produits
WHERE prix * stock > 1000
ORDER BY valeur_stock DESC;
```

## 🔍 Exemples

Un calcul avec un alias : le prix en centimes :

```sql
SELECT nom, prix * 100 AS prix_en_centimes
FROM produits
LIMIT 4;
```

**Résultat :**

| nom | prix_en_centimes |
| --- | --- |
| Clavier mécanique | 7990 |
| Souris sans fil | 2499 |
| Écran 27 pouces | 24900 |
| Casque audio | 5990 |

*4 lignes*

`ROUND` : le prix divisé par 1.2, arrondi à 2 décimales :

```sql
SELECT nom, prix, ROUND(prix / 1.2, 2) AS prix_divise
FROM produits
WHERE categorie = 'Livres';
```

**Résultat :**

| nom | prix | prix_divise |
| --- | --- | --- |
| Le Petit Prince | 7.5 | 6.25 |
| Apprendre le SQL | 34 | 28.33 |
| Harry Potter tome 1 | 8.9 | 7.42 |

*3 lignes*

`||` : fabriquer une étiquette à partir de deux colonnes :

```sql
SELECT nom || ' (' || categorie || ')' AS etiquette
FROM produits
LIMIT 4;
```

**Résultat :**

| etiquette |
| --- |
| Clavier mécanique (Informatique) |
| Souris sans fil (Informatique) |
| Écran 27 pouces (Informatique) |
| Casque audio (Informatique) |

*4 lignes*

`UPPER` et `LOWER` :

```sql
SELECT UPPER(ville) AS ville_majuscule, LOWER(prenom) AS prenom_minuscule
FROM clients
LIMIT 3;
```

**Résultat :**

| ville_majuscule | prenom_minuscule |
| --- | --- |
| PARIS | alice |
| LYON | bruno |
| MARSEILLE | chloé |

*3 lignes*

`LENGTH` dans le `SELECT` et dans le `WHERE` :

```sql
SELECT prenom, LENGTH(prenom) AS nb_lettres
FROM clients
WHERE LENGTH(prenom) <= 4;
```

**Résultat :**

| prenom | nb_lettres |
| --- | --- |
| Emma | 4 |
| Hugo | 4 |
| Inès | 4 |
| Léa | 3 |
| Nina | 4 |

*5 lignes*

`strftime` : extraire le mois d'une date :

```sql
SELECT id, date_commande, strftime('%m', date_commande) AS mois
FROM commandes
LIMIT 4;
```

**Résultat :**

| id | date_commande | mois |
| --- | --- | --- |
| 1 | 2024-01-10 | 01 |
| 2 | 2024-01-15 | 01 |
| 3 | 2024-02-02 | 02 |
| 4 | 2024-02-20 | 02 |

*4 lignes*

`strftime` dans un `WHERE` : les commandes de mai :

```sql
SELECT id, date_commande
FROM commandes
WHERE strftime('%m', date_commande) = '05';
```

**Résultat :**

| id | date_commande |
| --- | --- |
| 9 | 2024-05-07 |
| 10 | 2024-05-25 |

*2 lignes*

## 🧠 Bon à savoir

- ⚠️ **Division entière** : en SQLite, `7 / 2` donne `3` et pas 3.5, car les deux nombres sont entiers ! Pour obtenir 3.5, écris `7 / 2.0` ou `7 * 1.0 / 2`.
- Un alias du `SELECT` peut être réutilisé dans le `ORDER BY`. Dans le `WHERE`, ça marche en SQLite mais pas dans toutes les bases : mieux vaut répéter le calcul.
- En SQLite, `UPPER` et `LOWER` ne transforment que les lettres **sans accent** : `UPPER('Chloé')` donne `'CHLOé'`.
- Un calcul avec `NULL` donne `NULL` : `NULL + 5` vaut `NULL`.
- Dans MySQL, on colle des textes avec `CONCAT(a, b)` plutôt qu'avec `||`.

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| Espace dans un alias | `prix * stock AS valeur stock` | `prix * stock AS valeur_stock` |
| `+` pour coller du texte | `prenom + ' ' + nom` | `prenom \|\| ' ' \|\| nom` |
| Point-virgule entre les arguments | `ROUND(prix * 1.2; 2)` | `ROUND(prix * 1.2, 2)` |
| Comparer `strftime` à un nombre | `strftime('%m', date_commande) = 5` | `strftime('%m', date_commande) = '05'` |
| Division entière inattendue | `SELECT 1 / 3` → `0` | `SELECT 1.0 / 3` → `0.333…` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 5
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 5 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/05-calculs-fonctions/q1.sql` pour voir le résultat de ton fichier.

### Question 1 — Valeur du stock

📄 Fichier : `q1.sql`

Affiche le nom de chaque produit et la **valeur de son stock** (prix × stock), dans une colonne nommée `valeur_stock`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`SELECT nom, prix * stock AS valeur_stock FROM …`

</details>

### Question 2 — Hausse des prix

📄 Fichier : `q2.sql`

Les prix augmentent de 20 % ! Affiche le nom de chaque produit et son nouveau prix (prix × 1.2), **arrondi à 2 décimales**, dans une colonne nommée `nouveau_prix`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`ROUND(calcul, 2)` puis `AS nouveau_prix`.

</details>

### Question 3 — Nom en majuscules

📄 Fichier : `q3.sql`

Affiche le prénom de chaque client et son nom en MAJUSCULES, dans une colonne nommée `nom_majuscule`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

La fonction `UPPER(nom)`, puis un alias.

</details>

### Question 4 — Nom complet

📄 Fichier : `q4.sql`

Affiche **une seule colonne** nommée `nom_complet` qui contient le prénom, un espace, puis le nom de chaque client (par exemple `Alice Martin`).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Colle trois morceaux avec `||` : le prénom, `' '` (un espace entre apostrophes) et le nom.

</details>

### Question 5 — Noms à rallonge

📄 Fichier : `q5.sql`

Affiche le nom de chaque produit et le nombre de caractères de ce nom (colonne `longueur`), uniquement pour les produits dont le nom fait **plus de 15 caractères** (strictement).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`LENGTH(nom)` dans le `SELECT` (avec `AS longueur`) et aussi dans le `WHERE`.

</details>

### Question 6 — Commandes de décembre

📄 Fichier : `q6.sql`

Affiche l'id et la date des commandes passées au mois de **décembre**. Utilise `strftime`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`strftime('%m', date_commande)` renvoie le mois sous forme de texte : `'12'` pour décembre.

</details>

### Question 7 — Les soldes

📄 Fichier : `q7.sql`

C'est les soldes : -10 % sur les produits à plus de 50 €. Affiche le nom, le prix et le prix soldé (prix × 0.9, arrondi à 2 décimales, colonne `prix_solde`) des produits qui coûtent **plus de 50 €**, du plus cher au moins cher.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Trois colonnes : `nom`, `prix` et `ROUND(prix * 0.9, 2) AS prix_solde`. Puis `WHERE`, puis `ORDER BY prix DESC`.

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 06 — Compter et résumer : COUNT, SUM, AVG, MIN, MAX](../06-agregation/README.md)

⬅️ [Retour au sommaire](../../README.md)
