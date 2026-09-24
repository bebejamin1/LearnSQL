# Exercice 02 — Filtrer avec WHERE

> 🎯 **Objectif** : Ne garder que les lignes qui t'intéressent.  
> 📚 **Notions** : `WHERE`, `=`, `<>`, `<`, `>`, `<=`, `>=`, `AND`, `OR`, `NOT`, parenthèses  
> ⏱️ **Durée estimée** : 30 minutes

---

## 📖 Le cours

### Le problème

Jusqu'ici, on affichait **toutes** les lignes d'une table. Mais le plus souvent, on n'en veut que certaines : « les clients de Lyon », « les produits à moins de 20 € », « les commandes annulées »…

### La solution : WHERE

`WHERE` (« où ») ajoute une **condition**. Seules les lignes pour lesquelles la condition est **vraie** sont gardées.

```sql
SELECT colonnes
FROM table
WHERE condition;
```

L'ordre est **toujours** : `SELECT` → `FROM` → `WHERE`.

### Les opérateurs de comparaison

| Opérateur | Signification | Exemple |
| --- | --- | --- |
| `=` | égal à | `ville = 'Paris'` |
| `<>` (ou `!=`) | différent de | `ville <> 'Paris'` |
| `<` | strictement inférieur à | `prix < 20` |
| `>` | strictement supérieur à | `age > 30` |
| `<=` | inférieur ou égal à | `stock <= 10` |
| `>=` | supérieur ou égal à | `age >= 18` |

### Texte ou nombre ?

- Un **texte** s'écrit entre **apostrophes** : `'Paris'`, `'Livres'`, `'livrée'`.
- Un **nombre** s'écrit **sans** apostrophes : `20`, `3.5`. Attention, le séparateur décimal est un **point** et non une virgule !

### Combiner des conditions : AND, OR, NOT

- `AND` (et) : les **deux** conditions doivent être vraies.
- `OR` (ou) : **au moins une** des deux conditions doit être vraie.
- `NOT` (non) : inverse une condition.

| Condition A | Condition B | A `AND` B | A `OR` B |
| --- | --- | --- | --- |
| vrai | vrai | ✅ vrai | ✅ vrai |
| vrai | faux | ❌ faux | ✅ vrai |
| faux | vrai | ❌ faux | ✅ vrai |
| faux | faux | ❌ faux | ❌ faux |

### Les parenthèses

Quand tu mélanges `AND` et `OR`, **mets des parenthèses**. Sans elles, `AND` passe avant `OR` (comme la multiplication passe avant l'addition en maths), et le résultat peut te surprendre :

```sql
-- Produits de Sport OU de Jeux, qui coûtent moins de 25 € :
WHERE (categorie = 'Sport' OR categorie = 'Jeux') AND prix < 25

-- Sans parenthèses, SQL comprend :
-- « Sport (à n'importe quel prix) » OU « Jeux à moins de 25 € »
WHERE categorie = 'Sport' OR categorie = 'Jeux' AND prix < 25
```

## 🔍 Exemples

Les clients qui habitent à Marseille :

```sql
SELECT prenom, nom, ville
FROM clients
WHERE ville = 'Marseille';
```

**Résultat :**

| prenom | nom | ville |
| --- | --- | --- |
| Chloé | Bernard | Marseille |
| Karim | Lefebvre | Marseille |

*2 lignes*

Les produits dont le stock dépasse 50 :

```sql
SELECT nom, stock
FROM produits
WHERE stock > 50;
```

**Résultat :**

| nom | stock |
| --- | --- |
| Souris sans fil | 60 |
| Le Petit Prince | 120 |
| Harry Potter tome 1 | 80 |

*3 lignes*

Les commandes annulées :

```sql
SELECT * FROM commandes WHERE statut = 'annulée';
```

**Résultat :**

| id | client_id | date_commande | statut |
| --- | --- | --- | --- |
| 4 | 3 | 2024-02-20 | annulée |
| 8 | 6 | 2024-04-12 | annulée |

*2 lignes*

Les clients de Lyon **et** de plus de 32 ans (les deux conditions à la fois) :

```sql
SELECT prenom, ville, age
FROM clients
WHERE ville = 'Lyon' AND age > 32;
```

**Résultat :**

| prenom | ville | age |
| --- | --- | --- |
| Bruno | Lyon | 35 |
| Oscar | Lyon | 62 |

*2 lignes*

Les produits de Sport **ou** de Jeux, à moins de 25 € (remarque les parenthèses) :

```sql
SELECT nom, categorie, prix
FROM produits
WHERE (categorie = 'Sport' OR categorie = 'Jeux') AND prix < 25;
```

**Résultat :**

| nom | categorie | prix |
| --- | --- | --- |
| Ballon de football | Sport | 22 |
| Puzzle 1000 pièces | Jeux | 14.9 |

*2 lignes*

Les produits qui ne sont **pas** de l'informatique et coûtent plus de 30 € :

```sql
SELECT nom, categorie, prix
FROM produits
WHERE categorie <> 'Informatique' AND prix > 30;
```

**Résultat :**

| nom | categorie | prix |
| --- | --- | --- |
| Apprendre le SQL | Livres | 34 |
| Lampe de bureau | Maison | 32.5 |
| Cafetière | Maison | 45 |
| Haltères 5 kg | Sport | 39 |

*4 lignes*

## 🧠 Bon à savoir

- **Majuscules et accents comptent dans les données** : `'paris'` n'est pas égal à `'Paris'`, et `'livree'` n'est pas égal à `'livrée'`. Recopie les valeurs exactement comme elles sont dans la base.
- **Apostrophe dans un texte** : on la double. `'Jeu d''échecs'` représente le texte « Jeu d'échecs ».
- **Guillemets doubles** : en SQL standard, `"…"` sert pour les noms de colonnes, pas pour le texte. Prends l'habitude des apostrophes simples `'…'` pour le texte.
- On peut filtrer sur une colonne **qu'on n'affiche pas** : `SELECT nom FROM produits WHERE prix < 10;` fonctionne très bien.
- `NOT` s'utilise devant une condition : `WHERE NOT (ville = 'Paris')` revient à `WHERE ville <> 'Paris'`.

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| Texte sans apostrophes : SQL croit que c'est un nom de colonne | `WHERE ville = Paris` | `WHERE ville = 'Paris'` |
| Virgule décimale | `WHERE prix < 20,5` | `WHERE prix < 20.5` |
| Colonne non répétée après `OR` (pas d'erreur, mais un résultat faux !) | `WHERE ville = 'Paris' OR 'Lyon'` | `WHERE ville = 'Paris' OR ville = 'Lyon'` |
| Mauvais ordre des mots-clés | `SELECT nom WHERE prix < 10 FROM produits` | `SELECT nom FROM produits WHERE prix < 10` |
| `AND` et `OR` mélangés sans parenthèses | `WHERE a = 1 OR a = 2 AND b > 5` | `WHERE (a = 1 OR a = 2) AND b > 5` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 2
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 2 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/02-filtrer-where/q1.sql` pour voir le résultat de ton fichier.

### Question 1 — Les Lyonnais

📄 Fichier : `q1.sql`

Affiche toutes les colonnes des clients qui habitent à `Lyon`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`WHERE ville = …` et n'oublie pas les apostrophes autour du texte : `'Lyon'`.

</details>

### Question 2 — Petits prix

📄 Fichier : `q2.sql`

Affiche le nom et le prix des produits qui coûtent **strictement moins de 25 €** (un produit à 25 € ne doit pas apparaître).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Un nombre s'écrit sans apostrophes, et « strictement moins » s'écrit `<` : `WHERE prix < 25`.

</details>

### Question 3 — Rupture de stock

📄 Fichier : `q3.sql`

Affiche le nom et le stock des produits en **rupture de stock** (stock égal à 0).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

« égal à » s'écrit avec un seul `=` en SQL.

</details>

### Question 4 — Trente ans et plus

📄 Fichier : `q4.sql`

Affiche le prénom et l'âge des clients qui ont **au moins 30 ans** (30 ans compris).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

« au moins » = supérieur **ou égal** : `>=`.

</details>

### Question 5 — Jeunes Parisiens

📄 Fichier : `q5.sql`

Affiche le prénom, le nom et l'âge des clients qui habitent à `Paris` **et** qui ont **moins de 30 ans**.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Deux conditions qui doivent être vraies en même temps : relie-les avec `AND`.

</details>

### Question 6 — Lecture et jeux

📄 Fichier : `q6.sql`

Affiche toutes les colonnes des produits de la catégorie `Livres` **ou** de la catégorie `Jeux`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`WHERE categorie = 'Livres' OR categorie = …` : il faut répéter le nom de la colonne après `OR`.

</details>

### Question 7 — Stock faible

📄 Fichier : `q7.sql`

Affiche le nom, la catégorie et le stock des produits des catégories `Maison` ou `Sport` dont le stock est **inférieur à 15**.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Tu mélanges `OR` et `AND` : entoure la partie avec `OR` de parenthèses, sinon la condition sur le stock ne s'appliquera pas à la catégorie Maison.

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 03 — Filtres malins : IN, BETWEEN, LIKE, IS NULL](../03-filtres-avances/README.md)

⬅️ [Retour au sommaire](../../README.md)
