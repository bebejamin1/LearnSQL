# 🎓 Apprendre le SQL, en partant de zéro

Bienvenue ! Ce projet t'apprend le SQL **pas à pas**, avec **13 exercices** progressifs et **94 questions** corrigées automatiquement. Aucune connaissance préalable n'est nécessaire.

Chaque exercice a son propre dossier, avec :

- 📖 un **cours** clair, avec des exemples et leurs résultats ;
- 🧠 des **infos pratiques** et les **erreurs fréquentes** à éviter ;
- ✍️ des **questions** : une question = un fichier `qN.sql` où tu écris ta réponse ;
- ✅ une **vérification immédiate** : une commande te dit si c'est juste et, sinon, **pourquoi**.

---

## 🚀 Démarrage rapide (2 minutes)

**Ce qu'il te faut** : Python 3, déjà installé sur ta machine. Rien d'autre : pas de serveur ni de logiciel de base de données à installer.

1. Ouvre un terminal dans le dossier `LearnSQL` (dans VS Code : menu **Terminal → Nouveau terminal**).
2. Lis le premier cours : [exercices/01-premiers-pas-select/README.md](exercices/01-premiers-pas-select/README.md).
   💡 Dans VS Code, **Ctrl+Shift+V** affiche un fichier `.md` joliment mis en forme.
3. Ouvre `exercices/01-premiers-pas-select/q1.sql` et écris ta requête sous le cadre de commentaires.
4. Enregistre (**Ctrl+S**), puis vérifie :

   ```bash
   python3 verifier.py 1
   ```

5. Tout est vert ✅ ? Passe à l'exercice suivant !

---

## 🔁 La méthode de travail

```
  ┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
  │ 1. Lis le cours │ ──► │ 2. Teste dans la │ ──► │ 3. Écris ta réponse │ ──► │ 4. Vérifie       │
  │    README.md    │     │    console       │     │    dans qN.sql      │     │    verifier.py   │
  └─────────────────┘     └──────────────────┘     └─────────────────────┘     └────────┬─────────┘
          ▲                                                                              │
          └────────────────────── ❌ lis l'explication, corrige ◄───────────────────────┘
```

---

## 🧰 Les commandes

À lancer depuis le dossier `LearnSQL` :

| Commande | À quoi ça sert |
| --- | --- |
| `python3 verifier.py` | Affiche ta **progression** sur tous les exercices et te dit quoi faire ensuite |
| `python3 verifier.py 3` | **Vérifie** toutes les questions de l'exercice 03 |
| `python3 verifier.py 3 2` | Vérifie seulement la **question 2** de l'exercice 03 |
| `python3 verifier.py 3 --solutions` | Montre la **solution proposée** des questions que tu as **déjà réussies** (pour comparer) |
| `python3 executer.py` | Ouvre une **console SQL** pour tester librement tes requêtes |
| `python3 executer.py exercices/03-filtres-avances/q1.sql` | Exécute un fichier et **affiche son résultat** |

Dans la console (`python3 executer.py`) :

| Commande | Effet |
| --- | --- |
| `SELECT * FROM clients;` | exécute une requête (termine toujours par `;`) |
| `.tables` | liste les tables |
| `.schema produits` | montre les colonnes de la table `produits` |
| `.reset` | remet la base dans son état d'origine |
| `.quitter` (ou Ctrl+D) | quitte la console |

### Ce que te dit le vérificateur

| Symbole | Signification |
| --- | --- |
| ✅ | Bonne réponse ! |
| ❌ | Ta requête marche, mais le résultat n'est pas le bon. Le vérificateur t'explique pourquoi (trop de lignes, mauvais ordre, mauvaise colonne…) et affiche **ton résultat** à côté du **résultat attendu**. |
| 💥 | Ta requête contient une erreur SQL. Le message est traduit en français, avec une piste pour corriger. |
| ⬜ | Tu n'as pas encore répondu. |

---

## 📚 Le programme

| # | Exercice | Tu vas apprendre | Questions |
| --- | --- | --- | --- |
| 01 | [Premiers pas : SELECT](exercices/01-premiers-pas-select/README.md) | Ce qu'est une base de données, lire une table | 6 |
| 02 | [Filtrer avec WHERE](exercices/02-filtrer-where/README.md) | Garder certaines lignes, `AND`, `OR` | 7 |
| 03 | [Filtres malins](exercices/03-filtres-avances/README.md) | `IN`, `BETWEEN`, `LIKE`, `NULL`, les dates | 8 |
| 04 | [Trier et limiter](exercices/04-trier-limiter/README.md) | `ORDER BY`, `LIMIT`, `DISTINCT` | 7 |
| 05 | [Calculs, alias et fonctions](exercices/05-calculs-fonctions/README.md) | Calculer, renommer, transformer du texte | 7 |
| 06 | [Compter et résumer](exercices/06-agregation/README.md) | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` | 9 |
| 07 | [Regrouper](exercices/07-group-by/README.md) | `GROUP BY`, `HAVING` | 8 |
| 08 | [Relier les tables](exercices/08-jointures/README.md) | Clés, `JOIN` | 7 |
| 09 | [Garder tout le monde](exercices/09-left-join/README.md) | `LEFT JOIN`, trouver ce qui manque | 5 |
| 10 | [Les sous-requêtes](exercices/10-sous-requetes/README.md) | Des requêtes dans les requêtes | 7 |
| 11 | [Modifier les données](exercices/11-modifier-donnees/README.md) | `INSERT`, `UPDATE`, `DELETE` | 8 |
| 12 | [Créer ses tables](exercices/12-creer-tables/README.md) | `CREATE TABLE`, types, contraintes | 7 |
| 13 | [Projet final](exercices/13-projet-final/README.md) | Tout combiner, + `CASE` | 8 |

👉 Fais les exercices **dans l'ordre** : chacun s'appuie sur les précédents.

---

## 🛢️ La base de données

Tous les exercices utilisent la même base : une **boutique en ligne** avec 4 tables (`clients`, `produits`, `commandes`, `lignes_commande`). Sa description et son contenu complet sont dans [base/README.md](base/README.md).

La base est **recréée à neuf** à chaque vérification et à chaque lancement de la console : tu peux faire toutes les bêtises que tu veux, **tu ne peux rien casser** 😉

---

## 📁 Organisation du projet

```
LearnSQL/
├── README.md              ← tu es ici
├── verifier.py            ← vérifie tes réponses
├── executer.py            ← console SQL pour tester
├── base/
│   ├── README.md          ← description et contenu de la base
│   └── boutique.sql       ← le script qui crée la base
├── exercices/
│   ├── 01-premiers-pas-select/
│   │   ├── README.md      ← le cours + les questions
│   │   ├── q1.sql         ← ta réponse à la question 1
│   │   ├── q2.sql         ← ta réponse à la question 2
│   │   ├── …
│   │   └── .verif         ← données de correction (ne pas modifier)
│   ├── 02-filtrer-where/
│   └── …
└── outils/
    └── moteur.py          ← le moteur commun (exécution, comparaison)
```

---

## 💡 Conseils de débutant

- **Tape les requêtes toi-même** plutôt que de copier-coller les exemples : c'est comme ça que la syntaxe rentre.
- **Teste petit à petit** dans la console : commence par `SELECT * FROM table;`, puis ajoute le `WHERE`, puis le reste.
- **Lis les messages d'erreur** : ils sont en français et te disent généralement où chercher.
- **Tu bloques ?** Chaque question a un **indice** caché dans le README de l'exercice (clique sur « 💡 Indice »).
- **Tu as réussi ?** Compare avec la solution proposée (`--solutions`) : il y a souvent plusieurs bonnes façons d'écrire une requête.
- **Garde [base/README.md](base/README.md) ouvert** à côté : les noms exacts des colonnes et des valeurs y sont.

## ❓ Dépannage

| Problème | Solution |
| --- | --- |
| `python3: command not found` | Essaie `python` au lieu de `python3`. |
| `Exercice introuvable` | Lance la commande depuis le dossier `LearnSQL` (celui qui contient `verifier.py`). |
| ⬜ alors que j'ai répondu | As-tu bien **enregistré** le fichier (Ctrl+S) ? Ta requête doit être **sous** le cadre, pas dans un commentaire `--`. |
| Je veux recommencer une question | Efface ta requête dans le fichier `qN.sql` (garde le cadre de commentaires). |

---

## 🌍 Et après ?

Le SQL que tu apprends ici (SQLite) fonctionne à 95 % pareil dans **PostgreSQL**, **MySQL**, **MariaDB** ou **SQL Server**. Les petites différences concernent surtout les fonctions de texte et de dates.

Bon apprentissage ! 🚀
