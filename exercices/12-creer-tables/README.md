# Exercice 12 — Créer ses propres tables : CREATE TABLE

> 🎯 **Objectif** : Concevoir une table : choisir les types, la clé primaire et les règles que les données doivent respecter.  
> 📚 **Notions** : `CREATE TABLE`, types (`INTEGER`, `REAL`, `TEXT`), `PRIMARY KEY`, `NOT NULL`, `DEFAULT`, `REFERENCES`, `ALTER TABLE`, `DROP TABLE`, `INSERT … SELECT`  
> ⏱️ **Durée estimée** : 40 minutes

---

## 📖 Le cours

### CREATE TABLE

```sql
CREATE TABLE nom_de_la_table (
    colonne1 TYPE contraintes,
    colonne2 TYPE contraintes,
    colonne3 TYPE contraintes
);
```

Chaque colonne a un **nom**, un **type**, et éventuellement des **contraintes** (des règles). Les colonnes sont séparées par des virgules, mais il n'y a **pas de virgule après la dernière**.

### Les types en SQLite

| Type | Pour stocker | Exemples |
| --- | --- | --- |
| `INTEGER` | des nombres entiers | `42`, `-3`, `0` |
| `REAL` | des nombres à virgule | `19.90`, `3.14` |
| `TEXT` | du texte (et les dates, en SQLite) | `'Paris'`, `'2024-03-15'` |

Dans MySQL ou PostgreSQL, tu verras aussi `VARCHAR(100)`, `DATE`, `BOOLEAN`, `DECIMAL(10, 2)`… SQLite les accepte, mais les range dans les trois types ci-dessus. **Pour ces exercices, utilise `INTEGER`, `REAL` et `TEXT`.**

### Les contraintes (les règles)

| Contrainte | Signification |
| --- | --- |
| `PRIMARY KEY` | identifiant unique de chaque ligne (une seule clé primaire par table). En SQLite, une colonne `INTEGER PRIMARY KEY` se remplit toute seule : 1, 2, 3… |
| `NOT NULL` | la valeur est **obligatoire** |
| `UNIQUE` | deux lignes ne peuvent pas avoir la même valeur |
| `DEFAULT valeur` | la valeur utilisée quand on n'en donne pas |
| `CHECK (condition)` | la valeur doit respecter une condition, par exemple `CHECK (prix >= 0)` |
| `REFERENCES table(colonne)` | **clé étrangère** : la valeur doit exister dans l'autre table |

Voici comment la table `commandes` de la boutique a été créée :

```sql
CREATE TABLE commandes (
    id            INTEGER PRIMARY KEY,
    client_id     INTEGER NOT NULL REFERENCES clients(id),
    date_commande TEXT NOT NULL,
    statut        TEXT NOT NULL
);
```

### Modifier ou supprimer une table

```sql
ALTER TABLE clients ADD COLUMN telephone TEXT;  -- ajoute une colonne
ALTER TABLE clients RENAME TO acheteurs;        -- renomme la table
DROP TABLE nom_table;                           -- supprime la table ET tout son contenu !
DROP TABLE IF EXISTS nom_table;                 -- pas d'erreur si elle n'existe pas
```

### Remplir une table à partir d'une autre : INSERT … SELECT

Au lieu de `VALUES`, on peut donner une requête `SELECT` : toutes les lignes qu'elle renvoie sont insérées.

```sql
INSERT INTO table_cible (colonne1, colonne2)
SELECT colonneA, colonneB FROM autre_table WHERE …;
```

## 🔍 Exemples

Créer une table avec une clé étrangère et une valeur par défaut, la remplir, puis l'afficher. Remarque : l'id est rempli automatiquement, et les frais valent 4.99 quand on ne les précise pas.

```sql
CREATE TABLE livraisons (
    id           INTEGER PRIMARY KEY,
    commande_id  INTEGER NOT NULL REFERENCES commandes(id),
    transporteur TEXT NOT NULL,
    frais        REAL DEFAULT 4.99
);

INSERT INTO livraisons (commande_id, transporteur) VALUES (1, 'La Poste');
INSERT INTO livraisons (commande_id, transporteur, frais) VALUES (5, 'Chronopost', 12.50);

SELECT * FROM livraisons;
```

**Résultat :**

| id | commande_id | transporteur | frais |
| --- | --- | --- | --- |
| 1 | 1 | La Poste | 4.99 |
| 2 | 5 | Chronopost | 12.5 |

*2 lignes*

`INSERT … SELECT` : copier les clients lyonnais dans une nouvelle table :

```sql
CREATE TABLE contacts_lyon (
    id     INTEGER PRIMARY KEY,
    prenom TEXT NOT NULL,
    email  TEXT
);

INSERT INTO contacts_lyon (prenom, email)
SELECT prenom, email FROM clients WHERE ville = 'Lyon';

SELECT * FROM contacts_lyon;
```

**Résultat :**

| id | prenom | email |
| --- | --- | --- |
| 1 | Bruno | bruno.durand@mail.fr |
| 2 | Fatima | fatima.richard@mail.fr |
| 3 | Oscar | oscar.bertrand@mail.fr |

*3 lignes*

Pour voir la structure d'une table dans la console : `python3 executer.py` puis `.schema livraisons`.

## 🧠 Bon à savoir

- **Conventions de nommage** : noms de tables et de colonnes en minuscules, sans accent ni espace (`date_commande`), et des noms de tables souvent au pluriel (`clients`).
- **Toujours une clé primaire** dans chaque table.
- En SQLite, les clés étrangères ne sont vérifiées que si on active `PRAGMA foreign_keys = ON;`. Dans ce cours, c'est activé pour toi.
- `CREATE TABLE IF NOT EXISTS …` évite une erreur si la table existe déjà.
- `DROP TABLE` est **définitif** : pas de corbeille !

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| Virgule après la dernière colonne | `stock INTEGER,` puis `);` | `stock INTEGER` puis `);` |
| Parenthèses oubliées | `CREATE TABLE villes id INTEGER, nom TEXT;` | `CREATE TABLE villes (id INTEGER, nom TEXT);` |
| La table existe déjà : `table … already exists` | exécuter deux fois `CREATE TABLE villes (…)` | `CREATE TABLE IF NOT EXISTS villes (…)` |
| Type oublié | `nom NOT NULL` | `nom TEXT NOT NULL` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 12
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 12 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/12-creer-tables/q1.sql` pour voir le résultat de ton fichier.

> 🛟 Pour chaque question, la base est **recréée à neuf** avant d'exécuter ton fichier : chaque question part de la base d'origine, et tu ne peux rien casser.

### Question 1 — Fournisseurs

📄 Fichier : `q1.sql`

Crée une table `fournisseurs` avec 3 colonnes : `id` (entier, clé primaire), `nom` (texte, obligatoire) et `pays` (texte, facultatif).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`id INTEGER PRIMARY KEY`, `nom TEXT NOT NULL`, `pays TEXT`, séparés par des virgules.

</details>

### Question 2 — Villes

📄 Fichier : `q2.sql`

Crée une table `villes` avec les colonnes `id` (entier, clé primaire), `nom` (texte, obligatoire) et `habitants` (entier). Puis ajoute ces 3 villes :
- 1, `Paris`, 2100000
- 2, `Lyon`, 520000
- 3, `Marseille`, 870000

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

D'abord le `CREATE TABLE`, puis un `INSERT INTO villes (id, nom, habitants) VALUES (…), (…), (…);`

</details>

### Question 3 — Avis clients

📄 Fichier : `q3.sql`

Crée une table `avis` avec : `id` (entier, clé primaire), `produit_id` (entier, obligatoire, **clé étrangère** vers `produits(id)`), `note` (entier, obligatoire) et `commentaire` (texte, facultatif).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Pour la clé étrangère : `produit_id INTEGER NOT NULL REFERENCES produits(id)`.

</details>

### Question 4 — Valeur par défaut

📄 Fichier : `q4.sql`

Crée une table `messages` avec : `id` (entier, clé primaire), `contenu` (texte, obligatoire) et `lu` (entier, obligatoire, **valeur par défaut 0**). Puis ajoute un message dont le contenu est `Bonjour !`, **sans préciser** la valeur de `lu`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`lu INTEGER NOT NULL DEFAULT 0`, puis `INSERT INTO messages (contenu) VALUES ('Bonjour !');`

</details>

### Question 5 — Nouvelle colonne

📄 Fichier : `q5.sql`

Ajoute une colonne `telephone` (texte) à la table `clients` existante.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`ALTER TABLE … ADD COLUMN …`

</details>

### Question 6 — Suppression de table

📄 Fichier : `q6.sql`

Supprime complètement la table `lignes_commande`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`DROP TABLE …;` (ici, pas de risque : la base est recréée à chaque vérification).

</details>

### Question 7 — Table des catégories

📄 Fichier : `q7.sql`

Crée une table `categories` avec `id` (entier, clé primaire) et `nom` (texte, obligatoire). Puis remplis-la **automatiquement** avec les catégories différentes de la table `produits`, en une seule requête `INSERT … SELECT`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`INSERT INTO categories (nom) SELECT DISTINCT categorie FROM produits;` : l'id se remplit tout seul.

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 13 — Projet final : analyste de la boutique](../13-projet-final/README.md)

⬅️ [Retour au sommaire](../../README.md)
