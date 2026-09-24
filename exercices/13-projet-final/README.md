# Exercice 13 — Projet final : analyste de la boutique

> 🎯 **Objectif** : Répondre à de vraies questions « métier » en combinant tout ce que tu as appris, avec une dernière notion : `CASE`.  
> 📚 **Notions** : tout le cours + `CASE WHEN … THEN … ELSE … END`  
> ⏱️ **Durée estimée** : 1 à 2 heures

---

## 📖 La mission

Félicitations, tu es embauché(e) comme **analyste de données** de la boutique ! La direction te pose des questions, et chacune mélange plusieurs notions du cours. Prends ton temps : c'est normal de chercher.

### La méthode pour les requêtes compliquées

1. **Quelles tables ?** Où se trouvent les informations demandées ? (regarde [base/README.md](../../base/README.md))
2. **Quelles jointures ?** Comment relier ces tables (quelles clés) ? `JOIN` ou `LEFT JOIN` ?
3. **Quel filtre sur les lignes ?** → `WHERE`
4. **Faut-il regrouper ?** « par client », « par mois », « pour chaque » → `GROUP BY`. Un filtre sur le groupe ? → `HAVING`
5. **Quel affichage ?** Colonnes, calculs, alias → `SELECT`
6. **Quel ordre, combien ?** → `ORDER BY`, `LIMIT`

💡 **Construis ta requête petit à petit** dans la console (`python3 executer.py`) : écris d'abord le `FROM` et les `JOIN` avec un `SELECT *`, regarde le résultat, puis ajoute le `WHERE`, puis le `GROUP BY`…

### Rappel : l'ordre des mots-clés

```sql
SELECT … FROM … JOIN … ON … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT …;
```

### Dernière notion : CASE (le « si… alors… » du SQL)

`CASE` permet de choisir une valeur selon des conditions, comme un « si… sinon si… sinon » :

```sql
CASE
    WHEN condition1 THEN valeur1
    WHEN condition2 THEN valeur2
    ELSE valeur_par_defaut
END
```

Les conditions sont testées **dans l'ordre** : la première qui est vraie l'emporte. On l'utilise le plus souvent dans le `SELECT`, avec un alias.

## 🔍 Exemples

Classer les clients par tranche d'âge :

```sql
SELECT prenom, age,
       CASE
           WHEN age < 25 THEN 'jeune'
           WHEN age < 50 THEN 'adulte'
           ELSE 'senior'
       END AS tranche
FROM clients
LIMIT 6;
```

**Résultat :**

| prenom | age | tranche |
| --- | --- | --- |
| Alice | 28 | adulte |
| Bruno | 35 | adulte |
| Chloé | 22 | jeune |
| David | 41 | adulte |
| Emma | 19 | jeune |
| Fatima | 30 | adulte |

*6 lignes*

`CASE` pour traduire des valeurs :

```sql
SELECT id, statut,
       CASE statut
           WHEN 'livrée' THEN '✅'
           WHEN 'en cours' THEN '🚚'
           ELSE '❌'
       END AS icone
FROM commandes
LIMIT 5;
```

**Résultat :**

| id | statut | icone |
| --- | --- | --- |
| 1 | livrée | ✅ |
| 2 | livrée | ✅ |
| 3 | livrée | ✅ |
| 4 | annulée | ❌ |
| 5 | livrée | ✅ |

*5 lignes*

Le montant de chaque commande (une brique utile pour plusieurs questions !) :

```sql
SELECT co.id, SUM(p.prix * lc.quantite) AS montant
FROM commandes co
JOIN lignes_commande lc ON lc.commande_id = co.id
JOIN produits p ON p.id = lc.produit_id
GROUP BY co.id
LIMIT 5;
```

**Résultat :**

| id | montant |
| --- | --- |
| 1 | 104.89 |
| 2 | 23.9 |
| 3 | 34 |
| 4 | 249 |
| 5 | 530.5 |

*5 lignes*

## 🧠 Bon à savoir

- Le **montant** d'une commande = la somme de `prix × quantite` de ses lignes : il faut `commandes`, `lignes_commande` **et** `produits`.
- « Livrée » = `statut = 'livrée'`. « Non annulée » = `statut <> 'annulée'`.
- Si ton résultat a trop de lignes, vérifie tes `JOIN` (lignes répétées ?) et ton `GROUP BY`.
- Tu peux regrouper sur un `CASE` : `GROUP BY tranche` (avec l'alias).

## ⚠️ Erreurs fréquentes

| Erreur | ❌ Faux | ✅ Correct |
| --- | --- | --- |
| `END` oublié à la fin d'un `CASE` | `CASE WHEN age < 25 THEN 'jeune' ELSE 'autre' AS tranche` | `CASE WHEN … ELSE 'autre' END AS tranche` |
| Conditions dans le mauvais ordre (la 1ʳᵉ vraie l'emporte) | `WHEN age < 50 … WHEN age < 25 …` (personne n'est « jeune ») | `WHEN age < 25 … WHEN age < 50 …` |
| Statut sans accent | `statut = 'livree'` | `statut = 'livrée'` |

---

## ✍️ À toi de jouer !

### Comment faire

1. Ouvre le fichier `q1.sql` de ce dossier (chaque question a son fichier : `q1.sql`, `q2.sql`…).
2. Écris ta requête **sous** le cadre de commentaires.
3. Enregistre le fichier (**Ctrl+S**).
4. Dans le terminal, à la racine du projet `LearnSQL`, lance :

   ```bash
   python3 verifier.py 13
   ```

5. ✅ = réussi. ❌ = lis l'explication, corrige, et relance. Tu peux vérifier une seule question avec `python3 verifier.py 13 2` (question 2).

> 🧪 Pour tester librement avant de répondre : `python3 executer.py` ouvre une console SQL sur la base. Tu peux aussi lancer `python3 executer.py exercices/13-projet-final/q1.sql` pour voir le résultat de ton fichier.

### Question 1 — Top 3 des clients

📄 Fichier : `q1.sql`

Qui sont nos 3 meilleurs clients ? Affiche le prénom, le nom et le **total dépensé** (arrondi à 2 décimales) des 3 clients qui ont dépensé le plus, en ne comptant que les commandes **livrées**. Du plus gros total au plus petit.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

4 tables : `clients`, `commandes`, `lignes_commande`, `produits`. `WHERE co.statut = 'livrée'`, `GROUP BY cl.id, cl.prenom, cl.nom`, `ROUND(SUM(p.prix * lc.quantite), 2) AS total`, `ORDER BY total DESC LIMIT 3`.

</details>

### Question 2 — Grosses commandes

📄 Fichier : `q2.sql`

Affiche l'id, la date et le montant des commandes dont le montant dépasse **100 €** (tous statuts confondus), de la plus grosse à la plus petite.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Calcule le montant par commande (`GROUP BY co.id`), puis filtre les groupes avec `HAVING SUM(p.prix * lc.quantite) > 100`.

</details>

### Question 3 — Gammes de prix

📄 Fichier : `q3.sql`

Affiche le nom, le prix et la **gamme** de chaque produit (colonne `gamme`) :
- `petit prix` si le prix est inférieur à 20 € ;
- `moyen` si le prix va de 20 € à 50 € (inclus) ;
- `premium` au-delà de 50 €.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`CASE WHEN prix < 20 THEN 'petit prix' WHEN prix <= 50 THEN 'moyen' ELSE 'premium' END AS gamme`

</details>

### Question 4 — Les clients parisiens

📄 Fichier : `q4.sql`

Pour chaque client qui habite à `Paris`, affiche son prénom, son nom et le montant total de ses commandes **non annulées**.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Deux filtres dans le `WHERE` : la ville du client **et** `co.statut <> 'annulée'`. Puis regroupe par client.

</details>

### Question 5 — À réapprovisionner

📄 Fichier : `q5.sql`

Affiche le nom et le stock des produits dont le stock est **inférieur à 10** **et** qui ont déjà été commandés au moins une fois (inutile de racheter ce qui ne se vend pas !). Trie du plus petit stock au plus grand.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`WHERE stock < 10 AND id IN (SELECT produit_id FROM lignes_commande)`, puis `ORDER BY stock`.

</details>

### Question 6 — Clients par tranche d'âge

📄 Fichier : `q6.sql`

Combien de clients dans chaque tranche d'âge ? Affiche la tranche (colonne `tranche`) et le nombre de clients (colonne `nb_clients`). Les tranches sont :
- `moins de 30 ans` ;
- `30 à 49 ans` ;
- `50 ans et plus`.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Un `CASE … END AS tranche` dans le `SELECT`, `COUNT(*) AS nb_clients`, puis `GROUP BY tranche`.

</details>

### Question 7 — Clients curieux

📄 Fichier : `q7.sql`

Affiche le prénom des clients qui ont commandé des produits d'**au moins 2 catégories différentes**, avec leur nombre de catégories différentes (colonne `nb_categories`).

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

Relie les 4 tables, `GROUP BY cl.id, cl.prenom`, `COUNT(DISTINCT p.categorie) AS nb_categories` et `HAVING nb_categories >= 2`.

</details>

### Question 8 — Le rapport mensuel

📄 Fichier : `q8.sql`

La direction veut le **chiffre d'affaires par mois** (commandes **livrées** uniquement). Affiche le mois au format `AAAA-MM` (colonne `mois`) et le chiffre d'affaires arrondi à 2 décimales (colonne `chiffre_affaires`), du plus ancien mois au plus récent.

<details>
<summary>💡 Indice (clique si tu bloques)</summary>

`strftime('%Y-%m', co.date_commande) AS mois`, les jointures habituelles pour calculer `SUM(p.prix * lc.quantite)`, `GROUP BY mois`, `ORDER BY mois`.

</details>

---

🏆 C'est le dernier exercice. Lance `python3 verifier.py` pour voir ta progression complète !

⬅️ [Retour au sommaire](../../README.md)
