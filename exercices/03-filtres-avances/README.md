# Exercice 03 — Filtres malins : IN, BETWEEN, LIKE, IS NULL

> 🎯 **Objectif** : Écrire des filtres plus courts et plus puissants, chercher dans du texte et gérer les cases vides.  
> 📚 **Notions** : `IN`, `NOT IN`, `BETWEEN`, `LIKE`, `%`, `_`, `NULL`, `IS NULL`, `IS NOT NULL`, dates  
> ⏱️ **Durée estimée** : 30 à 40 minutes

---

## 📖 Le cours

### IN : « fait partie de la liste »

Au lieu d'écrire :

```sql
WHERE ville = 'Paris' OR ville = 'Lyon' OR ville = 'Nice'
```

on écrit simplement :

```sql
WHERE ville IN ('Paris', 'Lyon', 'Nice')
```

`NOT IN` fait l'inverse : « ne fait **pas** partie de la liste ». `IN` marche aussi avec des nombres : `WHERE id IN (1, 5, 8)`.

### BETWEEN : « entre … et … »

```sql
WHERE prix BETWEEN 10 AND 20
```

équivaut à `prix >= 10 AND prix <= 20`. ⚠️ Les deux bornes sont **incluses**, et la plus petite valeur s'écrit **en premier**.

### LIKE : chercher un motif dans un texte

`LIKE` compare un texte avec un **motif** qui peut contenir des jokers :

| Joker | Signification |
| --- | --- |
| `%` | n'importe quelle suite de caractères (même aucun) |
| `_` | exactement **un** caractère |

| Motif | Signification | Exemples qui correspondent |
| --- | --- | --- |
| `'A%'` | commence par A | Alice, Ahmed, A |
| `'%s'` | se termine par s | Mathis, Inès, Nantes |
| `'%an%'` | contient « an » | Bertrand, Nantes, Jean |
| `'_a%'` | 2ᵉ lettre = a | Karim, Mathis, Paris |

En SQLite, `LIKE` ne fait **pas** de différence entre majuscules et minuscules (pour les lettres sans accent) : `'a%'` trouve aussi « Alice ».

### NULL : la case vide

Parfois une information est **inconnue** ou **absente** : la case contient alors `NULL` (« rien »). Dans notre base, certains clients n'ont pas d'email, et un client n'a pas de ville.

⚠️ **Le piège n°1 du SQL** : on ne peut PAS écrire `= NULL`. NULL veut dire « inconnu », et on ne peut pas dire si un inconnu est égal à quelque chose. On écrit :

```sql
WHERE email IS NULL       -- l'email est absent
WHERE email IS NOT NULL   -- l'email est présent
```

### Les dates

En SQLite, les dates sont rangées sous forme de texte au format `'AAAA-MM-JJ'` (année-mois-jour), par exemple `'2024-03-15'`. Grâce à ce format, on peut les comparer directement :

```sql
WHERE date_commande >= '2024-06-01'                        -- à partir du 1er juin 2024
WHERE date_commande BETWEEN '2024-01-01' AND '2024-01-31'  -- en janvier 2024
```

## 🔍 Exemples

`IN` : les produits de Sport ou de Maison :

```sql
SELECT nom, categorie
FROM produits
WHERE categorie IN ('Sport', 'Maison');
```

**Résultat :**

| nom | categorie |
| --- | --- |
| Lampe de bureau | Maison |
| Cafetière | Maison |
| Plaid polaire | Maison |
| Ballon de football | Sport |
| Tapis de yoga | Sport |
| Haltères 5 kg | Sport |

*6 lignes*

`BETWEEN` : les clients qui ont entre 25 et 30 ans (30 est inclus, regarde Fatima) :

```sql
SELECT prenom, age
FROM clients
WHERE age BETWEEN 25 AND 30;
```

**Résultat :**

| prenom | age |
| --- | --- |
| Alice | 28 |
| Fatima | 30 |
| Hugo | 26 |
| Nina | 29 |

*4 lignes*

`LIKE` : les clients dont le nom commence par B :

```sql
SELECT prenom, nom
FROM clients
WHERE nom LIKE 'B%';
```

**Résultat :**

| prenom | nom |
| --- | --- |
| Chloé | Bernard |
| Oscar | Bertrand |

*2 lignes*

`LIKE` : les produits dont le nom contient « ou » :

```sql
SELECT nom
FROM produits
WHERE nom LIKE '%ou%';
```

**Résultat :**

| nom |
| --- |
| Souris sans fil |
| Écran 27 pouces |

*2 lignes*

`IS NULL` : le client dont la ville est inconnue :

```sql
SELECT prenom, nom, ville
FROM clients
WHERE ville IS NULL;
```

**Résultat :**

| prenom | nom | ville |
| --- | --- | --- |
| Mathis | Roux | NULL |

*1 ligne*

Dates : les commandes passées à partir du 1er novembre 2024 :

```sql
SELECT id, date_commande
FROM commandes
WHERE date_commande >= '2024-11-01';
```

**Résultat :**

| id | date_commande |
| --- | --- |
| 16 | 2024-11-11 |
| 17 | 2024-12-05 |
| 18 | 2024-12-20 |

*3 lignes*

## 🧠 Bon à savoir

- Tout se combine avec `AND` / `OR` : `WHERE categorie IN ('Livres', 'Jeux') AND prix BETWEEN 10 AND 30`.
- `NOT BETWEEN`, `NOT LIKE` et `NOT IN` existent aussi.
- **Accents** : `'%e'` ne trouve pas « Chloé », car `é` et `e` sont deux caractères différents.
- Dans d'autres bases (PostgreSQL par exemple), `LIKE` fait la différence entre majuscules et minuscules.
- `NULL` n'est pas `0` et n'est pas un texte vide `''` : c'est l'**absence** de valeur.

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| Comparer avec NULL (ne renvoie **jamais** rien !) | `WHERE email = NULL` | `WHERE email IS NULL` |
| `LIKE` sans joker : cherche exactement « L » | `WHERE nom LIKE 'L'` | `WHERE nom LIKE 'L%'` |
| Parenthèses oubliées après `IN` | `WHERE ville IN 'Paris', 'Lyon'` | `WHERE ville IN ('Paris', 'Lyon')` |
| Bornes à l'envers : aucun résultat | `WHERE prix BETWEEN 40 AND 20` | `WHERE prix BETWEEN 20 AND 40` |
| Date dans un mauvais format | `WHERE date_commande > '01/06/2024'` | `WHERE date_commande > '2024-06-01'` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 3
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 3 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/03-filtres-avances/q1.sql` pour voir le résultat de ton fichier.

### Question 1 — Trois villes

📄 Fichier : `q1.sql`

Affiche le prénom, le nom et la ville des clients qui habitent à `Paris`, `Lyon` ou `Nantes`. Utilise `IN`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`WHERE ville IN ('Paris', …)` avec les trois villes entre parenthèses, séparées par des virgules.

</details>

### Question 2 — Budget moyen

📄 Fichier : `q2.sql`

Affiche le nom et le prix des produits dont le prix est compris **entre 20 et 40 €** (bornes incluses).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`WHERE prix BETWEEN … AND …`

</details>

### Question 3 — La lettre L

📄 Fichier : `q3.sql`

Affiche le prénom et le nom des clients dont le **nom** (pas le prénom !) commence par la lettre `L`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`LIKE 'L%'` : le `%` remplace « n'importe quelle suite de caractères ».

</details>

### Question 4 — Chercher un mot

📄 Fichier : `q4.sql`

Affiche le nom et le prix des produits dont le nom **contient** `de` (par exemple « Lampe de bureau »).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Pour « contient », mets un `%` de chaque côté : `'%de%'`.

</details>

### Question 5 — Sans email

📄 Fichier : `q5.sql`

Affiche toutes les colonnes des clients dont l'**email n'est pas renseigné** (il vaut NULL).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

On n'écrit jamais `= NULL`. Utilise `IS NULL`.

</details>

### Question 6 — Un i et un email

📄 Fichier : `q6.sql`

Affiche le prénom, le nom et l'email des clients dont le **prénom contient la lettre `i`** **et** qui **ont** une adresse email.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Deux conditions reliées par `AND` : `prenom LIKE '%i%'` et `email IS NOT NULL`.

</details>

### Question 7 — Printemps 2024

📄 Fichier : `q7.sql`

Affiche toutes les colonnes des commandes passées **entre le 1er mars et le 30 juin 2024** (inclus).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Les dates s'écrivent `'AAAA-MM-JJ'` : `BETWEEN '2024-03-01' AND …`

</details>

### Question 8 — Ni l'un ni l'autre

📄 Fichier : `q8.sql`

Affiche le nom et la catégorie des produits qui ne sont **ni** de la catégorie `Informatique` **ni** de la catégorie `Livres`. Utilise `NOT IN`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`WHERE categorie NOT IN ('Informatique', 'Livres')`

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 04 — Trier et limiter : ORDER BY, LIMIT, DISTINCT](../04-trier-limiter/README.md)

⬅️ [Retour au sommaire](../../README.md)
