# Exercice 09 — Garder tout le monde : LEFT JOIN

> 🎯 **Objectif** : Relier des tables sans perdre les lignes sans correspondance, et trouver « ce qui manque ».  
> 📚 **Notions** : `LEFT JOIN`, `NULL` après jointure, `COUNT(colonne)`, `COALESCE`  
> ⏱️ **Durée estimée** : 40 minutes

---

## 📖 Le cours

### Le problème du JOIN classique

Un `JOIN` ne garde que les lignes qui ont une correspondance **des deux côtés**. Résultat : les clients qui n'ont **jamais commandé** disparaissent ! Alors comment faire la liste de *tous* les clients avec leurs commandes, ou trouver ceux qui n'ont rien acheté ? Avec `LEFT JOIN`.

### LEFT JOIN

`LEFT JOIN` garde **toutes** les lignes de la table de **gauche** (celle écrite en premier, dans le `FROM`), même quand elles n'ont aucune correspondance à droite. Dans ce cas, les colonnes de la table de droite sont remplies avec `NULL`.

```
 clients (gauche)       commandes (droite)            résultat du LEFT JOIN
 Alice   (id 1)   ──►   commandes 1, 3 et 11    ──►   Alice   │ 1
                                                      Alice   │ 3
                                                      Alice   │ 11
 Gabriel (id 7)   ──►   (aucune commande)       ──►   Gabriel │ NULL   ◄── gardé quand même !
```

| | `JOIN` | `LEFT JOIN` |
| --- | --- | --- |
| Client avec 3 commandes | 3 lignes | 3 lignes |
| Client sans commande | ❌ disparaît | ✅ 1 ligne, avec NULL côté commande |

### Trouver ce qui manque : LEFT JOIN + IS NULL

C'est une technique très utilisée. Après un `LEFT JOIN`, les lignes **sans correspondance** ont `NULL` dans les colonnes de droite. Il suffit de les garder :

```sql
SELECT cl.prenom
FROM clients cl
LEFT JOIN commandes co ON co.client_id = cl.id
WHERE co.id IS NULL;      -- « qui n'a aucune commande »
```

### Compter avec un LEFT JOIN : attention au piège !

```sql
SELECT cl.prenom, COUNT(*)      -- ❌ Gabriel aurait 1 : sa ligne avec NULL est comptée !
SELECT cl.prenom, COUNT(co.id)  -- ✅ Gabriel a 0 : COUNT(colonne) ignore les NULL
```

### COALESCE : remplacer un NULL par une valeur

`COALESCE(valeur, remplacement)` renvoie `valeur` si elle n'est pas NULL, sinon `remplacement`.

```sql
COALESCE(SUM(lc.quantite), 0)   -- 0 au lieu de NULL quand il n'y a rien à additionner
COALESCE(email, 'inconnu')      -- 'inconnu' quand l'email est NULL
```

(`IFNULL(a, b)` fait la même chose en SQLite et MySQL.)

## 🔍 Exemples

Les clients de Marseille et leurs commandes. Karim n'a jamais commandé, mais il apparaît quand même, avec des NULL :

```sql
SELECT cl.prenom, co.id AS commande_id, co.statut
FROM clients cl
LEFT JOIN commandes co ON co.client_id = cl.id
WHERE cl.ville = 'Marseille';
```

**Résultat :**

| prenom | commande_id | statut |
| --- | --- | --- |
| Chloé | 4 | annulée |
| Karim | NULL | NULL |

*2 lignes*

Les clients qui n'ont jamais passé de commande :

```sql
SELECT cl.prenom, cl.nom
FROM clients cl
LEFT JOIN commandes co ON co.client_id = cl.id
WHERE co.id IS NULL;
```

**Résultat :**

| prenom | nom |
| --- | --- |
| Gabriel | Moreau |
| Karim | Lefebvre |
| Mathis | Roux |

*3 lignes*

`COALESCE` pour remplacer les NULL :

```sql
SELECT prenom, COALESCE(email, 'pas d''email') AS email
FROM clients
WHERE ville = 'Marseille';
```

**Résultat :**

| prenom | email |
| --- | --- |
| Chloé | pas d'email |
| Karim | pas d'email |

*2 lignes*

## 🧠 Bon à savoir

- Avec un `LEFT JOIN`, **l'ordre des tables compte** : `FROM clients LEFT JOIN commandes` garde tous les clients, alors que `FROM commandes LEFT JOIN clients` garde toutes les commandes.
- `RIGHT JOIN` (tout garder à droite) existe aussi, mais on peut toujours s'en passer en inversant l'ordre des tables. `FULL JOIN` garde tout des deux côtés.
- ⚠️ Une condition sur la table de droite dans le `WHERE` (autre que `IS NULL`) supprime les lignes NULL : ton `LEFT JOIN` redevient un `JOIN` classique ! Pour filtrer la table de droite tout en gardant tout le monde, mets la condition dans le `ON` :
  `LEFT JOIN commandes co ON co.client_id = cl.id AND co.statut = 'livrée'`.

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| `COUNT(*)` après un `LEFT JOIN` : compte 1 au lieu de 0 | `COUNT(*)` | `COUNT(co.id)` |
| Table à garder placée à droite | `FROM commandes LEFT JOIN clients …` (pour trouver les clients sans commande) | `FROM clients LEFT JOIN commandes …` |
| `= NULL` au lieu de `IS NULL` | `WHERE co.id = NULL` | `WHERE co.id IS NULL` |
| NULL au lieu de 0 dans une somme | `SUM(lc.quantite)` | `COALESCE(SUM(lc.quantite), 0)` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 9
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 9 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/09-left-join/q1.sql` pour voir le résultat de ton fichier.

### Question 1 — Tous les clients

📄 Fichier : `q1.sql`

Affiche le prénom et le nom de **tous** les clients, avec l'id de chacune de leurs commandes. Les clients sans commande doivent apparaître aussi (avec un id de commande NULL).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`FROM clients cl LEFT JOIN commandes co ON co.client_id = cl.id`, et affiche `co.id`.

</details>

### Question 2 — Produits jamais commandés

📄 Fichier : `q2.sql`

Affiche le nom des produits qui n'ont **jamais été commandés** (ils n'apparaissent dans aucune ligne de commande).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Garde **tous** les produits (à gauche), relie-les à `lignes_commande`, puis garde ceux dont la ligne de commande est `NULL`.

</details>

### Question 3 — Compter aussi les zéros

📄 Fichier : `q3.sql`

Affiche le prénom de **chaque** client et son nombre de commandes, **y compris 0** pour ceux qui n'en ont aucune. Trie par nombre de commandes décroissant, puis par prénom (A→Z).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`LEFT JOIN`, `GROUP BY cl.id, cl.prenom` et surtout `COUNT(co.id)` (pas `COUNT(*)` !). Puis `ORDER BY nb_commandes DESC, cl.prenom`.

</details>

### Question 4 — Quantités vendues

📄 Fichier : `q4.sql`

Affiche le nom de **chaque** produit et la quantité totale commandée. Les produits jamais commandés doivent afficher **0** (et pas NULL).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`LEFT JOIN lignes_commande`, `GROUP BY p.id, p.nom`, et `COALESCE(SUM(lc.quantite), 0)`.

</details>

### Question 5 — Clients à relancer

📄 Fichier : `q5.sql`

Le service marketing veut écrire aux clients qui n'ont **jamais commandé**. Affiche le prénom et l'email de ces clients, mais seulement ceux qui **ont** une adresse email.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Technique `LEFT JOIN` + `WHERE co.id IS NULL`, avec en plus `AND cl.email IS NOT NULL`.

</details>

---

✅ Tout est vert ? Passe à la suite : [Exercice 10 — Des requêtes dans les requêtes : les sous-requêtes](../10-sous-requetes/README.md)

⬅️ [Retour au sommaire](../../README.md)
