# Exercice 08 — Relier les tables : JOIN

> 🎯 **Objectif** : Combiner les informations de plusieurs tables grâce aux clés primaires et étrangères.  
> 📚 **Notions** : clé primaire, clé étrangère, `JOIN … ON …`, `table.colonne`, alias de table, jointures multiples  
> ⏱️ **Durée estimée** : 45 minutes

---

## 📖 Le cours

### Pourquoi plusieurs tables ?

Regarde la table `commandes` : elle ne contient pas le nom du client, seulement un numéro, `client_id`. Pourquoi ? Pour **ne pas répéter** les informations. Si Alice change d'email, on le modifie à **un seul endroit** (dans la table `clients`), et pas dans chacune de ses commandes.

### Clé primaire et clé étrangère

- La **clé primaire** (*primary key*) est la colonne qui identifie chaque ligne de façon **unique** : `clients.id`, `produits.id`… Deux clients ne peuvent pas avoir le même `id`.
- Une **clé étrangère** (*foreign key*) est une colonne qui **fait référence** à la clé primaire d'une autre table : `commandes.client_id` contient l'`id` d'un client.

Les liens de notre boutique :

```
┌──────────┐          ┌───────────────┐          ┌─────────────────┐          ┌──────────┐
│ clients  │          │ commandes     │          │ lignes_commande │          │ produits │
├──────────┤          ├───────────────┤          ├─────────────────┤          ├──────────┤
│ id       │◄─────────│ client_id     │          │ produit_id      │─────────►│ id       │
│ prenom   │          │ id            │◄─────────│ commande_id     │          │ nom      │
│ …        │          │ date_commande │          │ quantite        │          │ prix     │
└──────────┘          └───────────────┘          └─────────────────┘          └──────────┘
```

En français : *un client passe des commandes ; une commande contient des lignes ; chaque ligne concerne un produit.*

### JOIN … ON …

`JOIN` colle côte à côte les lignes de deux tables qui « vont ensemble ». `ON` précise **comment** elles vont ensemble :

```sql
SELECT commandes.id, commandes.date_commande, clients.prenom
FROM commandes
JOIN clients ON commandes.client_id = clients.id;
```

Pour chaque commande, SQL cherche le client dont l'`id` est égal au `client_id` de la commande, et colle les deux lignes :

```
 commandes                          clients                 résultat
 id │ client_id │ date_commande      id │ prenom             id │ date_commande │ prenom
 1  │ 1         │ 2024-01-10   ──►   1  │ Alice      ──►     1  │ 2024-01-10    │ Alice
 2  │ 2         │ 2024-01-15   ──►   2  │ Bruno      ──►     2  │ 2024-01-15    │ Bruno
 3  │ 1         │ 2024-02-02   ──►   1  │ Alice      ──►     3  │ 2024-02-02    │ Alice
```

### table.colonne : lever l'ambiguïté

Quand deux tables ont une colonne du **même nom** (`id`, `nom`…), il faut préciser laquelle on veut en écrivant `table.colonne` : `clients.id`, `commandes.id`. Sinon SQL répond « ambiguous column name ».

### Les alias de table

Écrire `commandes.` partout, c'est long. On peut donner un **surnom** à chaque table :

```sql
SELECT co.id, co.date_commande, cl.prenom
FROM commandes AS co
JOIN clients AS cl ON co.client_id = cl.id;
```

Le mot `AS` est même facultatif : `FROM commandes co` marche aussi.

### Enchaîner plusieurs JOIN

Pour relier 3 ou 4 tables, on ajoute des `JOIN`, **un par lien** :

```sql
SELECT cl.prenom, p.nom, lc.quantite
FROM clients cl
JOIN commandes co       ON co.client_id = cl.id
JOIN lignes_commande lc ON lc.commande_id = co.id
JOIN produits p         ON p.id = lc.produit_id;
```

### Tout le reste fonctionne pareil

Après les `JOIN`, on utilise `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`… exactement comme avant.

## 🔍 Exemples

Les commandes des clients lyonnais, avec le nom du client :

```sql
SELECT co.id, co.date_commande, cl.prenom, cl.nom
FROM commandes co
JOIN clients cl ON co.client_id = cl.id
WHERE cl.ville = 'Lyon';
```

**Résultat :**

| id | date_commande | prenom | nom |
| --- | --- | --- | --- |
| 2 | 2024-01-15 | Bruno | Durand |
| 7 | 2024-04-01 | Bruno | Durand |
| 8 | 2024-04-12 | Fatima | Richard |
| 17 | 2024-12-05 | Bruno | Durand |
| 18 | 2024-12-20 | Oscar | Bertrand |

*5 lignes*

Le contenu de la commande n°1, avec le nom et le prix des produits :

```sql
SELECT lc.commande_id, p.nom, p.prix, lc.quantite
FROM lignes_commande lc
JOIN produits p ON lc.produit_id = p.id
WHERE lc.commande_id = 1;
```

**Résultat :**

| commande_id | nom | prix | quantite |
| --- | --- | --- | --- |
| 1 | Clavier mécanique | 79.9 | 1 |
| 1 | Souris sans fil | 24.99 | 1 |

*2 lignes*

`JOIN` + `GROUP BY` : le nombre d'articles vendus par catégorie :

```sql
SELECT p.categorie, SUM(lc.quantite) AS articles_vendus
FROM lignes_commande lc
JOIN produits p ON lc.produit_id = p.id
GROUP BY p.categorie;
```

**Résultat :**

| categorie | articles_vendus |
| --- | --- |
| Informatique | 11 |
| Jeux | 7 |
| Livres | 11 |
| Maison | 5 |
| Sport | 6 |

*5 lignes*

## 🧠 Bon à savoir

- `JOIN` s'écrit aussi `INNER JOIN` (c'est pareil). Il ne garde que les lignes qui ont une correspondance **des deux côtés** : un client sans commande n'apparaît pas. Pour le garder, il faut un `LEFT JOIN` (exercice suivant).
- Si une ligne correspond à plusieurs lignes de l'autre table, elle est **répétée** : un client qui a 3 commandes apparaît 3 fois.
- Pour un `JOIN` classique, l'ordre des tables ne change pas le résultat.
- Sans `ON`, chaque ligne est combinée avec **chaque** ligne de l'autre table : 15 clients × 18 commandes = 270 lignes absurdes !
- **Regrouper par client** : regroupe par son `id` (deux clients peuvent avoir le même prénom !) et ajoute les colonnes que tu affiches, pour respecter la règle d'or du `GROUP BY` : `GROUP BY cl.id, cl.prenom, cl.nom`.
- Une fois qu'on a donné un alias à une table (`FROM clients cl`), on doit utiliser l'alias (`cl.prenom`) et non plus le nom complet.

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| Colonne ambiguë | `SELECT id FROM commandes JOIN clients ON …` | `SELECT commandes.id FROM …` |
| Mauvaises colonnes reliées (l'id d'un client n'a rien à voir avec l'id d'une commande) | `ON clients.id = commandes.id` | `ON clients.id = commandes.client_id` |
| `ON` oublié | `FROM commandes JOIN clients` | `FROM commandes JOIN clients ON commandes.client_id = clients.id` |
| Nom complet utilisé après un alias | `FROM clients cl … WHERE clients.ville = 'Lyon'` | `… WHERE cl.ville = 'Lyon'` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 8
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 8 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/08-jointures/q1.sql` pour voir le résultat de ton fichier.

### Question 1 — Qui a commandé ?

📄 Fichier : `q1.sql`

Affiche l'id de chaque commande, sa date, et le **prénom** du client qui l'a passée (dans cet ordre).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`FROM commandes JOIN clients ON commandes.client_id = clients.id`. Pense à préciser `commandes.id`.

</details>

### Question 2 — Les commandes d'Alice

📄 Fichier : `q2.sql`

Affiche l'id, la date et le statut des commandes passées par la cliente dont le prénom est `Alice`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Une jointure entre `commandes` et `clients`, puis `WHERE cl.prenom = 'Alice'`.

</details>

### Question 3 — Détail des lignes

📄 Fichier : `q3.sql`

Pour chaque ligne de commande, affiche l'id de la commande (`commande_id`), le **nom du produit** et la quantité.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Relie `lignes_commande` et `produits` avec `lignes_commande.produit_id = produits.id`.

</details>

### Question 4 — Facture n°5

📄 Fichier : `q4.sql`

Pour la commande n°5, affiche le nom de chaque produit, la quantité, le prix unitaire, et le montant de la ligne (prix × quantité) dans une colonne nommée `montant`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Même jointure qu'à la question précédente, avec un calcul `p.prix * lc.quantite AS montant` et un `WHERE lc.commande_id = 5`.

</details>

### Question 5 — Le panier d'Emma

📄 Fichier : `q5.sql`

Affiche le nom de tous les produits commandés par la cliente dont le prénom est `Emma`. (Il faut relier les 4 tables !)

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`clients` → `commandes` (client_id) → `lignes_commande` (commande_id) → `produits` (produit_id). Trois `JOIN`, puis `WHERE cl.prenom = 'Emma'`.

</details>

### Question 6 — Commandes par client

📄 Fichier : `q6.sql`

Affiche le prénom et le nom de chaque client qui a passé au moins une commande, avec son **nombre de commandes**.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`JOIN` entre `clients` et `commandes`, puis `GROUP BY cl.id, cl.prenom, cl.nom` et `COUNT(*)`.

</details>

### Question 7 — Chiffre d'affaires par catégorie

📄 Fichier : `q7.sql`

Affiche chaque catégorie de produit et son **chiffre d'affaires** (la somme de prix × quantité), en ne comptant que les commandes **livrées**. Trie du plus grand chiffre d'affaires au plus petit.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Il faut 3 tables : `lignes_commande`, `produits` (pour le prix et la catégorie) et `commandes` (pour le statut). Puis `WHERE`, `GROUP BY p.categorie`, `SUM(p.prix * lc.quantite)` et `ORDER BY … DESC`.

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 09 — Garder tout le monde : LEFT JOIN](../09-left-join/README.md)

⬅️ [Retour au sommaire](../../README.md)
