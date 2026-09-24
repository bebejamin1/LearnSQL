# Exercice 11 — Modifier les données : INSERT, UPDATE, DELETE

> 🎯 **Objectif** : Ajouter, modifier et supprimer des lignes, sans rien casser.  
> 📚 **Notions** : `INSERT INTO … VALUES`, `UPDATE … SET … WHERE`, `DELETE FROM … WHERE`, clés étrangères  
> ⏱️ **Durée estimée** : 40 minutes

---

## 📖 Le cours

Jusqu'ici, on a seulement **lu** des données. SQL sert aussi à les **modifier** :

| Commande | Rôle |
| --- | --- |
| `INSERT INTO` | **ajouter** des lignes |
| `UPDATE` | **modifier** des lignes existantes |
| `DELETE FROM` | **supprimer** des lignes |

### INSERT INTO : ajouter une ligne

```sql
INSERT INTO table (colonne1, colonne2, colonne3)
VALUES (valeur1, valeur2, valeur3);
```

- les valeurs sont données dans le **même ordre** que les colonnes ;
- les colonnes que tu ne cites pas reçoivent `NULL` (ou leur valeur par défaut) ;
- la colonne `id` (`INTEGER PRIMARY KEY`) peut être omise : SQLite lui donne automatiquement le numéro suivant.

Pour ajouter plusieurs lignes d'un coup :

```sql
INSERT INTO produits (nom, categorie, prix, stock)
VALUES ('Stylo', 'Maison', 1.50, 100),
       ('Cahier', 'Maison', 2.90, 50);
```

### UPDATE : modifier des lignes

```sql
UPDATE table
SET colonne1 = nouvelle_valeur, colonne2 = nouvelle_valeur
WHERE condition;
```

La nouvelle valeur peut être calculée à partir de l'ancienne : `SET stock = stock - 1`.

> ⚠️ **SANS WHERE, TOUTES LES LIGNES SONT MODIFIÉES !**
> `UPDATE produits SET prix = 0;` met le prix de **tous** les produits à 0. C'est LA catastrophe classique en entreprise.

### DELETE FROM : supprimer des lignes

```sql
DELETE FROM table
WHERE condition;
```

> ⚠️ Même danger : `DELETE FROM clients;` **vide toute la table**.

### Le bon réflexe : SELECT d'abord

Avant un `UPDATE` ou un `DELETE`, teste ton `WHERE` avec un `SELECT` pour voir quelles lignes seront touchées :

```sql
-- 1. Je regarde ce que je vais modifier
SELECT * FROM produits WHERE categorie = 'Jeux';
-- 2. Je modifie, avec exactement le même WHERE
UPDATE produits SET stock = 0 WHERE categorie = 'Jeux';
```

### Les clés étrangères protègent la base

La base **refuse** de supprimer une commande qui a encore des lignes dans `lignes_commande`, sinon ces lignes pointeraient vers une commande qui n'existe plus. Tu obtiens l'erreur `FOREIGN KEY constraint failed`.

Il faut donc supprimer **d'abord les lignes qui dépendent** (les « enfants » : `lignes_commande`), **puis** la ligne principale (le « parent » : `commandes`).

### Plusieurs requêtes dans un fichier

Tu peux écrire plusieurs requêtes à la suite, chacune terminée par un `;`. Elles sont exécutées dans l'ordre, de haut en bas.

## 🔍 Exemples

Chaque exemple est suivi d'un `SELECT` pour voir le résultat. Ajouter un client sans préciser l'id (SQLite choisit 16). Les colonnes non citées valent NULL :

```sql
INSERT INTO clients (prenom, nom, ville, age)
VALUES ('Zoé', 'Blanc', 'Nice', 21);

SELECT * FROM clients WHERE id >= 14;
```

**Résultat :**

| id | prenom | nom | ville | age | email | date_inscription |
| --- | --- | --- | --- | --- | --- | --- |
| 14 | Nina | David | Nantes | 29 | nina.david@mail.fr | 2024-04-21 |
| 15 | Oscar | Bertrand | Lyon | 62 | oscar.bertrand@mail.fr | 2024-05-30 |
| 16 | Zoé | Blanc | Nice | 21 | NULL | NULL |

*3 lignes*

Modifier deux colonnes d'un produit, en partant des anciennes valeurs :

```sql
UPDATE produits
SET prix = prix - 5, stock = stock + 10
WHERE id = 1;

SELECT * FROM produits WHERE id = 1;
```

**Résultat :**

| id | nom | categorie | prix | stock |
| --- | --- | --- | --- | --- |
| 1 | Clavier mécanique | Informatique | 74.9 | 35 |

*1 ligne*

Supprimer les lignes de commande dont la quantité est d'au moins 3 (il en restait 29) :

```sql
DELETE FROM lignes_commande WHERE quantite >= 3;

SELECT COUNT(*) AS lignes_restantes FROM lignes_commande;
```

**Résultat :**

| lignes_restantes |
| --- |
| 27 |

*1 ligne*

## 🧠 Bon à savoir

- Pour ces exercices, le vérificateur regarde **l'état des tables après ta requête**. Si c'est faux, il t'affiche seulement les lignes qui diffèrent.
- Pour t'entraîner librement : `python3 executer.py`, et la commande `.reset` remet la base à neuf.
- **Transactions** (pour aller plus loin) : `BEGIN;` démarre un groupe de modifications, `COMMIT;` les valide, `ROLLBACK;` les **annule** toutes. C'est le filet de sécurité des pros.
- En SQLite, les clés étrangères ne sont vérifiées que si on active `PRAGMA foreign_keys = ON;`. Ici, c'est déjà fait pour toi.

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| `WHERE` oublié : toute la table est modifiée | `UPDATE produits SET prix = 10;` | `UPDATE produits SET prix = 10 WHERE id = 3;` |
| Sans liste de colonnes, il faut donner **toutes** les colonnes | `INSERT INTO clients VALUES ('Paul', 'Garnier');` | `INSERT INTO clients (prenom, nom) VALUES ('Paul', 'Garnier');` |
| `AND` entre deux modifications (pas d'erreur, mais un résultat absurde !) | `SET prix = 10 AND stock = 5` | `SET prix = 10, stock = 5` |
| id déjà utilisé : `UNIQUE constraint failed` | `INSERT INTO clients (id, …) VALUES (1, …)` | choisis un id libre, ou laisse SQLite le choisir |
| Parent supprimé avant ses enfants : `FOREIGN KEY constraint failed` | `DELETE FROM commandes WHERE id = 4;` seul | d'abord `DELETE FROM lignes_commande WHERE commande_id = 4;` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 11
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 11 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/11-modifier-donnees/q1.sql` pour voir le résultat de ton fichier.

> 🛟 Pour chaque question, la base est **recréée à neuf** avant d'exécuter ton fichier : chaque question part de la base d'origine, et tu ne peux rien casser.

### Question 1 — Nouveau client

📄 Fichier : `q1.sql`

Ajoute ce nouveau client : id `16`, prénom `Paul`, nom `Garnier`, ville `Rennes`, âge `27`, email `paul.garnier@mail.fr`, date d'inscription `2024-06-01`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`INSERT INTO clients (id, prenom, nom, ville, age, email, date_inscription) VALUES (16, 'Paul', …);`. Les textes et les dates entre apostrophes, les nombres sans.

</details>

### Question 2 — Nouveau produit

📄 Fichier : `q2.sql`

Ajoute le produit `Gourde isotherme`, de la catégorie `Sport`, au prix de `17.50` €, avec un stock de `50`. Ne précise **pas** l'id : laisse la base le choisir.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Liste seulement les colonnes `nom`, `categorie`, `prix`, `stock`.

</details>

### Question 3 — Retour en stock

📄 Fichier : `q3.sql`

Le casque audio (id `4`) est de retour : mets son stock à `30`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`UPDATE produits SET stock = … WHERE id = …;` Sans le `WHERE`, tous les produits seraient modifiés !

</details>

### Question 4 — Hausse des prix

📄 Fichier : `q4.sql`

Augmente de **10 %** le prix de tous les produits de la catégorie `Jeux`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Augmenter de 10 %, c'est multiplier par 1.1 : `SET prix = prix * 1.1`.

</details>

### Question 5 — Déménagement

📄 Fichier : `q5.sql`

La cliente Chloé (id `3`) déménage à `Nice` et donne enfin son email : `chloe.bernard@mail.fr`. Mets à jour ces deux informations **en une seule requête**.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Plusieurs modifications dans un seul `SET`, séparées par une **virgule** (pas par `AND`).

</details>

### Question 6 — Ménage des clients inactifs

📄 Fichier : `q6.sql`

Supprime tous les clients qui n'ont **jamais passé de commande**. Utilise une sous-requête.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`DELETE FROM clients WHERE id NOT IN (SELECT client_id FROM commandes);`

</details>

### Question 7 — Supprimer une commande

📄 Fichier : `q7.sql`

Supprime la commande n°`4` (elle a été annulée) **ainsi que ses lignes** de commande. Attention à l'ordre, à cause des clés étrangères !

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Deux requêtes, dans cet ordre : d'abord `DELETE FROM lignes_commande WHERE commande_id = 4;` puis la commande elle-même.

</details>

### Question 8 — Une vente !

📄 Fichier : `q8.sql`

La cliente n°`5` passe une nouvelle commande. Écris les 3 requêtes nécessaires :
1. ajoute la commande id `19`, datée du `2024-12-24`, statut `en cours` ;
2. ajoute la ligne de commande id `30` : 2 exemplaires du produit n°`7` dans la commande 19 ;
3. diminue de 2 le stock du produit n°`7`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Deux `INSERT` (un dans `commandes`, un dans `lignes_commande`), puis un `UPDATE produits SET stock = stock - 2 WHERE id = 7;`. La commande doit exister avant sa ligne (clé étrangère).

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 12 — Créer ses propres tables : CREATE TABLE](../12-creer-tables/README.md)

⬅️ [Retour au sommaire](../../README.md)
