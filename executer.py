#!/usr/bin/env python3
"""Console SQL pour tester tes requêtes sur la base « boutique ».

Utilisation :
  python3 executer.py               → console interactive
  python3 executer.py fichier.sql   → exécute un fichier et affiche le résultat

Commandes de la console :
  .tables            liste les tables de la base
  .schema produits   montre les colonnes d'une table (.schema seul : toutes)
  .reset             remet la base dans son état d'origine
  .aide              affiche cette aide
  .quitter           quitte la console (ou Ctrl+D)
"""

import sqlite3
import sys
from pathlib import Path
from typing import Optional

from outils.moteur import (bleu, creer_base, executer, executer_tout,
                           est_vide, gras, gris, rouge, tableau,
                           traduire_erreur, vert)

REQUETE_TABLES = ("SELECT name AS nom_table FROM sqlite_master "
                  "WHERE type = 'table' ORDER BY name")
REQUETE_SCHEMA = ("SELECT name AS colonne, type, "
                  "CASE WHEN pk > 0 THEN 'oui' ELSE '' END AS cle_primaire, "
                  "CASE WHEN \"notnull\" THEN 'oui' ELSE '' END "
                  "AS obligatoire "
                  "FROM pragma_table_info('{}') ORDER BY cid")


def afficher_resultats(con: sqlite3.Connection, sql: str) -> None:
    """Exécute du SQL et affiche le résultat de chaque instruction."""
    try:
        resultats = executer_tout(con, sql)
    except (sqlite3.Error, sqlite3.Warning) as erreur:
        print(rouge("💥 Erreur SQL : " + traduire_erreur(erreur)))
        return
    for resultat in resultats:
        if isinstance(resultat, tuple):
            print(tableau(*resultat, max_lignes=100))
        elif resultat >= 0:
            print(vert(f"✔ OK — {resultat} ligne(s) modifiée(s)"))
        else:
            print(vert("✔ OK"))


def lister_tables(con: sqlite3.Connection) -> list[str]:
    """Renvoie le nom de toutes les tables de la base."""
    resultat = executer(con, REQUETE_TABLES)
    return [ligne[0] for ligne in resultat[1]] if resultat else []


def afficher_schema(con: sqlite3.Connection, table: str) -> None:
    """Affiche les colonnes d'une table (ou de toutes les tables)."""
    tables = [table] if table else lister_tables(con)
    for nom in tables:
        if nom not in lister_tables(con):
            print(rouge(f"La table « {nom} » n'existe pas. "
                        "Tape .tables pour voir la liste."))
            continue
        print(gras(f"\n   Table {nom}"))
        resultat = executer(con, REQUETE_SCHEMA.format(nom))
        if resultat:
            print(tableau(*resultat, max_lignes=50))


def commande(con: sqlite3.Connection,
             texte: str) -> Optional[sqlite3.Connection]:
    """Exécute une commande spéciale (.tables, .schema…).

    Renvoie la connexion à utiliser ensuite, ou None pour quitter.
    """
    mots = texte.split()
    nom = mots[0].lower()
    argument = mots[1] if len(mots) > 1 else ""
    if nom in (".quitter", ".quit", ".exit", ".q"):
        return None
    if nom == ".tables":
        afficher_resultats(con, REQUETE_TABLES)
    elif nom == ".schema":
        afficher_schema(con, argument)
    elif nom == ".reset":
        con.close()
        con = creer_base()
        print(vert("✔ Base remise à zéro."))
    elif nom in (".aide", ".help"):
        print(__doc__)
    else:
        print(rouge(f"Commande inconnue : {nom}. Tape .aide"))
    return con


def console() -> None:
    """Lance la console SQL interactive."""
    try:
        import readline  # noqa: F401  (historique avec les flèches)
    except ImportError:
        pass
    print(gras("\n🛢️  Console SQL — base « boutique »"))
    print(gris("   Termine chaque requête par un point-virgule « ; ».\n"
               "   .tables = liste des tables · .schema = colonnes · "
               ".aide = aide · .quitter = sortir\n"
               "   La base est neuve à chaque lancement : "
               "tu ne peux rien casser !\n"))
    con: Optional[sqlite3.Connection] = creer_base()
    tampon = ""
    while con is not None:
        try:
            ligne = input(bleu("  ...> ") if tampon else bleu("sql> "))
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print(gris("\n(requête annulée)"))
            tampon = ""
            continue
        if not tampon and ligne.strip().startswith("."):
            con = commande(con, ligne.strip())
            continue
        tampon += ligne + "\n"
        if est_vide(tampon):
            tampon = ""
        elif sqlite3.complete_statement(tampon):
            afficher_resultats(con, tampon)
            tampon = ""
    print(gris("À bientôt !"))


def executer_fichier(chemin: str) -> None:
    """Exécute un fichier .sql et affiche ses résultats."""
    fichier = Path(chemin)
    if not fichier.is_file():
        print(rouge(f"Fichier introuvable : {chemin}"))
        sys.exit(1)
    sql = fichier.read_text(encoding="utf-8")
    if est_vide(sql):
        print(gris(f"Le fichier {chemin} ne contient pas encore de "
                   "requête."))
        return
    print(gras(f"\n▶ {chemin}\n"))
    afficher_resultats(creer_base(), sql)
    print()


def main() -> None:
    """Point d'entrée du script."""
    arguments = sys.argv[1:]
    if not arguments:
        console()
    elif arguments[0] in ("-h", "--help", "--aide"):
        print(__doc__)
    else:
        executer_fichier(arguments[0])


if __name__ == "__main__":
    main()
