"""Moteur commun : base de données, exécution, affichage et comparaison."""

import base64
import itertools
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, Callable, Optional

RACINE = Path(__file__).resolve().parent.parent
FICHIER_BASE = RACINE / "base" / "boutique.sql"
DOSSIER_EXERCICES = RACINE / "exercices"
TOLERANCE = 0.0051

Ligne = tuple[Any, ...]
Resultat = tuple[list[str], list[Ligne]]

# ---------------------------------------------------------------------------
# Couleurs dans le terminal
# ---------------------------------------------------------------------------

_COULEURS = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _style(code: str) -> Callable[[object], str]:
    """Renvoie une fonction qui colore un texte avec le code ANSI donné."""
    def colorer(texte: object) -> str:
        if not _COULEURS:
            return str(texte)
        return f"\033[{code}m{texte}\033[0m"
    return colorer


vert = _style("32")
rouge = _style("31")
jaune = _style("33")
bleu = _style("36")
gris = _style("90")
gras = _style("1")

# ---------------------------------------------------------------------------
# Base de données et exécution des requêtes
# ---------------------------------------------------------------------------


def creer_base() -> sqlite3.Connection:
    """Crée une base neuve, en mémoire, remplie avec la boutique."""
    con = sqlite3.connect(":memory:", isolation_level=None)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(FICHIER_BASE.read_text(encoding="utf-8"))
    return con


def _fin_chaine(sql: str, debut: int) -> int:
    """Renvoie l'indice du guillemet qui ferme la chaîne ouverte à debut."""
    guillemet = sql[debut]
    i = debut + 1
    while i < len(sql):
        if sql[i] == guillemet:
            if sql[i + 1:i + 2] != guillemet:
                return i
            i += 1
        i += 1
    return len(sql)


def sans_commentaires(sql: str) -> str:
    """Retire les commentaires (-- et /* */) sans toucher aux chaînes."""
    morceaux = []
    i = 0
    while i < len(sql):
        if sql[i] in "'\"":
            fin = _fin_chaine(sql, i)
            morceaux.append(sql[i:fin + 1])
            i = fin + 1
        elif sql.startswith("--", i):
            fin = sql.find("\n", i)
            i = len(sql) if fin == -1 else fin
        elif sql.startswith("/*", i):
            fin = sql.find("*/", i + 2)
            i = len(sql) if fin == -1 else fin + 2
        else:
            morceaux.append(sql[i])
            i += 1
    return "".join(morceaux)


def est_vide(sql: str) -> bool:
    """Vrai si le texte ne contient que des commentaires ou des espaces."""
    return not sans_commentaires(sql).strip().strip(";").strip()


def decouper(sql: str) -> list[str]:
    """Découpe un script en instructions SQL séparées par des « ; »."""
    instructions = []
    courant = ""
    for caractere in sql:
        courant += caractere
        if caractere == ";" and sqlite3.complete_statement(courant):
            instructions.append(courant)
            courant = ""
    instructions.append(courant)
    return [i for i in instructions if not est_vide(i)]


def executer_tout(con: sqlite3.Connection, sql: str) -> list[Any]:
    """Exécute un script, instruction par instruction.

    Renvoie, pour chaque instruction, soit un résultat (colonnes, lignes)
    pour un SELECT, soit le nombre de lignes modifiées.
    """
    resultats: list[Any] = []
    for instruction in decouper(sql):
        curseur = con.execute(instruction)
        if curseur.description:
            colonnes = [d[0] for d in curseur.description]
            resultats.append((colonnes, curseur.fetchall()))
        else:
            resultats.append(curseur.rowcount)
    return resultats


def executer(con: sqlite3.Connection, sql: str) -> Optional[Resultat]:
    """Exécute un script et renvoie le résultat du dernier SELECT."""
    selects = [r for r in executer_tout(con, sql) if isinstance(r, tuple)]
    return selects[-1] if selects else None


# ---------------------------------------------------------------------------
# Traduction des erreurs SQLite en français
# ---------------------------------------------------------------------------

_TRADUCTIONS = [
    (r"no such table: (\S+)",
     "La table « {0} » n'existe pas. Vérifie l'orthographe. Tables "
     "disponibles : clients, produits, commandes, lignes_commande."),
    (r"no such column: (\S+)",
     "La colonne « {0} » n'existe pas. Vérifie l'orthographe et la table "
     "interrogée. Astuce : un texte s'écrit entre apostrophes 'comme ceci'."),
    (r"ambiguous column name: (\S+)",
     "La colonne « {0} » existe dans plusieurs tables de ta jointure : "
     "précise laquelle, par exemple clients.{0} ou commandes.{0}."),
    (r'near "(.+?)": syntax error',
     "Erreur de syntaxe près de « {0} ». Vérifie les virgules entre les "
     "colonnes (mais pas avant FROM !), l'ordre des mots-clés (SELECT, "
     "FROM, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT), les apostrophes "
     "et les parenthèses."),
    (r"incomplete input",
     "Requête incomplète : il manque sûrement une parenthèse fermante "
     "« ) » ou une apostrophe « ' »."),
    (r"unrecognized token: (.+)",
     "Symbole non reconnu {0} : souvent une apostrophe mal fermée."),
    (r"misuse of aggregate(?: function)?:? (\S+)",
     "Mauvaise utilisation de {0} : COUNT, SUM, AVG… sont interdits dans "
     "un WHERE. Pour filtrer après un regroupement, utilise HAVING."),
    (r"a GROUP BY clause is required before HAVING",
     "HAVING s'utilise uniquement après un GROUP BY."),
    (r"UNIQUE constraint failed: (\S+)",
     "Doublon interdit : cette valeur de « {0} » existe déjà (clé "
     "primaire ou colonne UNIQUE)."),
    (r"NOT NULL constraint failed: (\S+)",
     "La colonne « {0} » est obligatoire (NOT NULL) : donne-lui une "
     "valeur."),
    (r"FOREIGN KEY constraint failed",
     "Clé étrangère non respectée : soit tu fais référence à une ligne qui "
     "n'existe pas, soit tu supprimes une ligne encore utilisée par une "
     "autre table (supprime d'abord les lignes qui dépendent d'elle)."),
    (r"table (\S+) already exists",
     "La table « {0} » existe déjà."),
    (r"table (\S+) has (\d+) columns but (\d+) values were supplied",
     "La table « {0} » a {1} colonnes mais tu donnes {2} valeurs. Précise "
     "les colonnes : INSERT INTO table (col1, col2) VALUES (…)."),
    (r"(\d+) values for (\d+) columns",
     "Tu donnes {0} valeur(s) pour {1} colonne(s) : il en faut autant."),
    (r"sub-select returns (\d+) columns - expected 1",
     "Ta sous-requête renvoie {0} colonnes, mais ici elle ne doit en "
     "renvoyer qu'une seule."),
    (r"no such function: (\S+)",
     "La fonction « {0} » n'existe pas en SQLite. Vérifie son nom."),
    (r"wrong number of arguments to function (\S+)",
     "Mauvais nombre d'arguments pour la fonction {0}."),
    (r"duplicate column name: (\S+)",
     "La colonne « {0} » est déclarée deux fois."),
]


def traduire_erreur(erreur: Exception) -> str:
    """Traduit un message d'erreur SQLite en explication française."""
    message = str(erreur)
    for motif, traduction in _TRADUCTIONS:
        trouve = re.search(motif, message)
        if trouve:
            explication = traduction.format(*trouve.groups())
            return f"{explication}\n   (message d'origine : {message})"
    return message


# ---------------------------------------------------------------------------
# Affichage d'un résultat sous forme de tableau
# ---------------------------------------------------------------------------


def formater_valeur(valeur: Any) -> str:
    """Transforme une valeur SQL en texte lisible."""
    if valeur is None:
        return "NULL"
    if isinstance(valeur, float):
        return format(valeur, ".10g")
    return str(valeur)


def _trait(largeurs: list[int], gauche: str, milieu: str,
           droite: str) -> str:
    """Construit une ligne de bordure du tableau."""
    return gauche + milieu.join("─" * (lg + 2) for lg in largeurs) + droite


def tableau(colonnes: list[str], lignes: list[Ligne], max_lignes: int = 15,
            marge: str = "   ") -> str:
    """Transforme un résultat en joli tableau pour le terminal."""
    affichees = lignes[:max_lignes]
    textes = [[formater_valeur(v) for v in ligne] for ligne in affichees]
    largeurs = [len(c) for c in colonnes]
    for ligne in textes:
        largeurs = [max(lg, len(v)) for lg, v in zip(largeurs, ligne)]

    entete = [gras(c.ljust(lg)) for c, lg in zip(colonnes, largeurs)]
    sortie = [
        marge + _trait(largeurs, "┌", "┬", "┐"),
        marge + "│ " + " │ ".join(entete) + " │",
        marge + _trait(largeurs, "├", "┼", "┤"),
    ]
    for brute, texte in zip(affichees, textes):
        cellules = []
        for valeur, cellule, largeur in zip(brute, texte, largeurs):
            cellule = cellule.ljust(largeur)
            cellules.append(gris(cellule) if valeur is None else cellule)
        sortie.append(marge + "│ " + " │ ".join(cellules) + " │")
    sortie.append(marge + _trait(largeurs, "└", "┴", "┘"))

    reste = len(lignes) - len(affichees)
    if reste > 0:
        bilan = f"… et {reste} autre(s) ligne(s), {len(lignes)} au total"
    else:
        bilan = f"{len(lignes)} ligne" + ("s" if len(lignes) > 1 else "")
    sortie.append(gris(marge + bilan))
    return "\n".join(sortie)


# ---------------------------------------------------------------------------
# Comparaison d'un résultat avec le résultat attendu
# ---------------------------------------------------------------------------


def _nombre(valeur: Any) -> Optional[float]:
    """Convertit une valeur en nombre si c'est possible, sinon None."""
    if isinstance(valeur, bool):
        return None
    if isinstance(valeur, (int, float)):
        return float(valeur)
    if isinstance(valeur, str):
        try:
            return float(valeur)
        except ValueError:
            return None
    return None


def valeurs_egales(a: Any, b: Any) -> bool:
    """Égalité tolérante : 45.15 == 45.14875, 12 == 12.0, '2024' == 2024."""
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    na, nb = _nombre(a), _nombre(b)
    if na is not None and nb is not None:
        return abs(na - nb) <= TOLERANCE
    return bool(a == b)


def lignes_egales(a: Ligne, b: Ligne) -> bool:
    """Vrai si deux lignes contiennent les mêmes valeurs."""
    return len(a) == len(b) and all(map(valeurs_egales, a, b))


def difference(attendues: list[Ligne],
               obtenues: list[Ligne]) -> tuple[list[Ligne], list[Ligne]]:
    """Renvoie les lignes obtenues en trop et les lignes attendues absentes."""
    en_trop = list(obtenues)
    manquantes = []
    for ligne in attendues:
        for i, candidate in enumerate(en_trop):
            if lignes_egales(ligne, candidate):
                del en_trop[i]
                break
        else:
            manquantes.append(ligne)
    return en_trop, manquantes


def memes_lignes(attendues: list[Ligne], obtenues: list[Ligne],
                 ordre: bool) -> bool:
    """Vrai si les lignes sont identiques (dans le même ordre si ordre)."""
    if len(attendues) != len(obtenues):
        return False
    if ordre:
        return all(map(lignes_egales, attendues, obtenues))
    return difference(attendues, obtenues) == ([], [])


def _colonnes_melangees(attendues: list[Ligne], obtenues: list[Ligne],
                        nb_colonnes: int) -> bool:
    """Vrai si les valeurs sont justes mais les colonnes mal ordonnées."""
    if nb_colonnes > 6:
        return False
    for ordre in itertools.permutations(range(nb_colonnes)):
        if list(ordre) == list(range(nb_colonnes)):
            continue
        remises = [tuple(ligne[i] for i in ordre) for ligne in obtenues]
        if memes_lignes(attendues, remises, False):
            return True
    return False


def _probleme_nombre_lignes(attendu: int, obtenu: int) -> str:
    """Explique une différence de nombre de lignes."""
    if obtenu > attendu:
        conseil = ("Tu as trop de lignes : ton filtre (WHERE / HAVING) "
                   "laisse passer trop de choses, ou il manque un DISTINCT, "
                   "une LIMIT…")
    else:
        conseil = ("Il te manque des lignes : ton filtre (WHERE / HAVING) "
                   "est trop strict, ou ta jointure élimine des lignes.")
    return (f"Ton résultat a {obtenu} ligne(s), mais on en attend "
            f"{attendu}.\n   {conseil}")


def _probleme_valeurs(attendu: Resultat, obtenu: Resultat,
                      ordre: bool) -> Optional[str]:
    """Explique pourquoi les valeurs diffèrent, ou None si elles collent."""
    lignes_a, lignes_o = attendu[1], obtenu[1]
    if memes_lignes(lignes_a, lignes_o, ordre):
        return None
    if ordre and memes_lignes(lignes_a, lignes_o, False):
        return ("Les bonnes lignes sont là, mais pas dans le bon ordre : "
                "vérifie ton ORDER BY (ASC = croissant, DESC = "
                "décroissant).")
    if _colonnes_melangees(lignes_a, lignes_o, len(attendu[0])):
        return ("Tes valeurs sont justes, mais tes colonnes ne sont pas "
                "dans le bon ordre. Respecte l'ordre demandé.")
    return ("Les valeurs ne correspondent pas au résultat attendu. Vérifie "
            "les colonnes choisies, tes conditions et tes calculs.")


def _probleme_noms(attendues: list[str], obtenues: list[str]) -> str:
    """Explique une différence de noms de colonnes, ou renvoie ''."""
    if [c.lower() for c in attendues] == [c.lower() for c in obtenues]:
        return ""
    return ("Les valeurs sont justes 👍 mais les noms de colonnes ne sont "
            "pas ceux demandés.\n"
            f"   Attendu : {', '.join(attendues)}\n"
            f"   Obtenu  : {', '.join(obtenues)}\n"
            "   Utilise AS pour renommer une colonne.")


def comparer(attendu: Resultat, obtenu: Optional[Resultat],
             ordre: bool = False, colonnes: bool = False) -> Optional[str]:
    """Compare deux résultats.

    Renvoie None si c'est juste, sinon une explication en français.
    """
    if obtenu is None:
        return ("Ta requête n'affiche aucun résultat : il faut une requête "
                "SELECT qui renvoie des lignes.")
    if len(obtenu[0]) != len(attendu[0]):
        return (f"Ton résultat a {len(obtenu[0])} colonne(s), mais on en "
                f"attend {len(attendu[0])}. Relis bien quelles colonnes "
                "sont demandées.")
    if len(obtenu[1]) != len(attendu[1]):
        return _probleme_nombre_lignes(len(attendu[1]), len(obtenu[1]))
    probleme = _probleme_valeurs(attendu, obtenu, ordre)
    if probleme is None and colonnes:
        probleme = _probleme_noms(attendu[0], obtenu[0]) or None
    return probleme


# ---------------------------------------------------------------------------
# Exercices
# ---------------------------------------------------------------------------


def lister_exercices() -> list[Path]:
    """Renvoie les dossiers d'exercices, dans l'ordre."""
    return sorted(d for d in DOSSIER_EXERCICES.iterdir()
                  if d.is_dir() and d.name[:2].isdigit())


def charger_verification(dossier: Path) -> dict[str, Any]:
    """Lit le fichier caché .verif d'un exercice (encodé pour éviter
    de voir les solutions par accident)."""
    contenu = (dossier / ".verif").read_text(encoding="utf-8")
    return json.loads(base64.b64decode(contenu).decode("utf-8"))


def _resultat_attendu(question: dict[str, Any]) -> Optional[Resultat]:
    """Calcule le résultat attendu à partir de la solution."""
    con = creer_base()
    try:
        attendu = executer(con, question["solution"])
        if question.get("verif"):
            attendu = executer(con, question["verif"])
    finally:
        con.close()
    return attendu


def verifier_question(dossier: Path,
                      question: dict[str, Any]) -> dict[str, Any]:
    """Vérifie la réponse à une question.

    Renvoie un dictionnaire avec le statut (ok, vide, erreur ou faux),
    un message d'explication et les résultats obtenu et attendu.
    """
    fichier = dossier / question["fichier"]
    sql = fichier.read_text(encoding="utf-8") if fichier.exists() else ""
    if est_vide(sql):
        return {"statut": "vide"}

    verif = question.get("verif")
    attendu = _resultat_attendu(question)
    con = creer_base()
    etape = "Erreur SQL : "
    try:
        obtenu = executer(con, sql)
        if verif:
            etape = ("Ta requête s'exécute, mais la vérification du "
                     "résultat échoue : ")
            obtenu = executer(con, verif)
    except (sqlite3.Error, sqlite3.Warning) as erreur:
        return {"statut": "erreur",
                "message": etape + traduire_erreur(erreur)}
    finally:
        con.close()

    ordre = bool(question.get("ordre")) and not verif
    probleme = comparer(attendu, obtenu, ordre,
                        bool(question.get("colonnes")))
    if probleme is None:
        return {"statut": "ok"}
    if verif:
        probleme = ("Après ta requête, les données ne sont pas dans l'état "
                    "attendu.\n   " + probleme)
    return {"statut": "faux", "message": probleme, "attendu": attendu,
            "obtenu": obtenu, "modification": bool(verif)}
