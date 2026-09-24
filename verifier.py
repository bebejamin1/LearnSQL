#!/usr/bin/env python3
"""Vérifie tes réponses aux exercices SQL.

Utilisation :
  python3 verifier.py                → ta progression sur tous les exercices
  python3 verifier.py 3              → vérifie les questions de l'exercice 03
  python3 verifier.py 3 2            → vérifie seulement la question 2
  python3 verifier.py 3 --solutions  → solutions des questions réussies
"""

import re
import sys
from pathlib import Path
from typing import Any, Optional

from outils.moteur import (DOSSIER_EXERCICES, Resultat, bleu,
                           charger_verification, difference, gras, gris,
                           jaune, lister_exercices, rouge, tableau,
                           verifier_question, vert)

ICONES = {"ok": "✅", "vide": "⬜", "erreur": "💥", "faux": "❌"}


def barre(fait: int, total: int, largeur: int = 10) -> str:
    """Dessine une barre de progression."""
    plein = round(largeur * fait / total) if total else 0
    return vert("█" * plein) + gris("░" * (largeur - plein))


def numero(dossier: Path) -> int:
    """Renvoie le numéro d'un exercice à partir du nom de son dossier."""
    return int(dossier.name[:2])


def trouver_exercice(texte: str) -> Path:
    """Trouve le dossier d'un exercice à partir de « 3 », « 03 »…"""
    trouve = re.search(r"(\d+)", Path(texte).name or texte)
    if trouve:
        for dossier in lister_exercices():
            if numero(dossier) == int(trouve.group(1)):
                return dossier
    print(rouge(f"Exercice « {texte} » introuvable."))
    noms = ", ".join(d.name for d in lister_exercices())
    print(f"Exercices disponibles : {noms}")
    sys.exit(1)


def exercice_courant() -> Optional[Path]:
    """Renvoie le dossier d'exercice où l'on se trouve, s'il y en a un."""
    try:
        relatif = Path.cwd().resolve().relative_to(DOSSIER_EXERCICES)
    except ValueError:
        return None
    if not relatif.parts:
        return None
    return DOSSIER_EXERCICES / relatif.parts[0]


def afficher_progression() -> None:
    """Affiche l'avancement sur tous les exercices."""
    print(gras("\n📊 Ta progression\n"))
    lignes = []
    prochain = None
    for dossier in lister_exercices():
        infos = charger_verification(dossier)
        questions = infos["questions"]
        ok = sum(verifier_question(dossier, q)["statut"] == "ok"
                 for q in questions)
        if ok < len(questions) and prochain is None:
            prochain = dossier
        titre = f"{numero(dossier):02d} {infos['titre']}"
        lignes.append((titre, ok, len(questions)))

    largeur = max(len(titre) for titre, _, _ in lignes)
    for titre, ok, nombre in lignes:
        print(f"  {titre:<{largeur}}  {barre(ok, nombre)} {ok}/{nombre} "
              f"{'✅' if ok == nombre else ''}")
    total_ok = sum(ok for _, ok, _ in lignes)
    total = sum(nombre for _, _, nombre in lignes)

    score = gras(f"{total_ok}/{total}")
    print(f"\n  Total : {score} questions réussies "
          f"{barre(total_ok, total, 20)}")
    if prochain is None:
        print(vert("\n🏆 Tu as terminé TOUS les exercices. "
                   "Félicitations, tu parles SQL !\n"))
        return
    cours = bleu(f"exercices/{prochain.name}/README.md")
    commande = bleu(f"python3 verifier.py {numero(prochain)}")
    print(f"\n👉 Continue avec l'exercice {numero(prochain):02d} :")
    print(f"   1. Lis le cours : {cours}")
    print(f"   2. Vérifie tes réponses : {commande}\n")


def afficher_solution(entete: str, question: dict[str, Any],
                      statut: str) -> None:
    """Affiche la solution proposée, seulement si la question est réussie."""
    print(gras(entete))
    if statut != "ok":
        print(gris("   🔒 Réussis d'abord cette question pour voir "
                   "la solution.\n"))
        return
    print(gris("   Solution proposée (la tienne peut être différente "
               "et tout aussi juste) :"))
    for ligne in question["solution"].strip().splitlines():
        print(bleu("     " + ligne))
    print()


def afficher_resultat(entete: str, question: dict[str, Any],
                      resultat: dict[str, Any]) -> None:
    """Affiche le verdict d'une question, avec les explications."""
    statut = resultat["statut"]
    if statut == "ok":
        print(vert(entete))
        return
    if statut == "vide":
        print(gris(f"{entete}  (pas encore de réponse dans "
                   f"{question['fichier']})"))
        return
    print(rouge(entete) + gris(f"  ({question['fichier']})"))
    print(jaune("   " + resultat["message"]))
    if statut == "faux" and resultat["modification"]:
        afficher_difference(resultat["attendu"], resultat["obtenu"])
    elif statut == "faux":
        if resultat["obtenu"] is not None:
            print(gris("\n   Ton résultat :"))
            print(tableau(*resultat["obtenu"], max_lignes=10))
        print(gris("\n   Résultat attendu :"))
        print(tableau(*resultat["attendu"], max_lignes=10))
    print()


def afficher_difference(attendu: Resultat, obtenu: Resultat) -> None:
    """Montre uniquement les lignes qui diffèrent après une modification."""
    en_trop, manquantes = difference(attendu[1], obtenu[1])
    if en_trop:
        print(gris("\n   Lignes présentes chez toi mais PAS attendues :"))
        print(tableau(obtenu[0], en_trop, max_lignes=10))
    if manquantes:
        print(gris("\n   Lignes attendues mais ABSENTES chez toi :"))
        print(tableau(attendu[0], manquantes, max_lignes=10))


def afficher_bilan(dossier: Path, reussies: int, total: int) -> None:
    """Affiche le score de l'exercice et la suite du parcours."""
    print(f"\n   Score : {gras(f'{reussies}/{total}')} "
          f"{barre(reussies, total)}")
    if reussies < total:
        print(gris("\n   Modifie tes fichiers qN.sql, enregistre (Ctrl+S), "
                   "puis relance la vérification.\n"))
        return
    print(vert("\n🎉 Bravo, exercice terminé !"))
    print(gris("   Compare avec les solutions proposées : "
               f"python3 verifier.py {numero(dossier)} --solutions"))
    suivants = [d for d in lister_exercices()
                if numero(d) > numero(dossier)]
    if suivants:
        cours = bleu(f"exercices/{suivants[0].name}/README.md")
        print(f"👉 Exercice suivant : {cours}")
    print()


def verifier_exercice(dossier: Path, seule: Optional[int] = None,
                      solutions: bool = False) -> None:
    """Vérifie les questions d'un exercice (ou une seule question)."""
    infos = charger_verification(dossier)
    questions = infos["questions"]
    print(gras(f"\n📘 Exercice {numero(dossier):02d} — {infos['titre']}\n"))
    if seule is not None and not 1 <= seule <= len(questions):
        print(rouge(f"Il n'y a pas de question {seule} "
                    f"(questions de 1 à {len(questions)})."))
        sys.exit(1)

    reussies = 0
    for i, question in enumerate(questions, start=1):
        if seule is not None and i != seule:
            continue
        resultat = verifier_question(dossier, question)
        reussies += resultat["statut"] == "ok"
        entete = (f"{ICONES[resultat['statut']]} Question {i} — "
                  f"{question['titre']}")
        if solutions:
            afficher_solution(entete, question, resultat["statut"])
        else:
            afficher_resultat(entete, question, resultat)

    if seule is None and not solutions:
        afficher_bilan(dossier, reussies, len(questions))
    elif not solutions:
        print()


def main() -> None:
    """Point d'entrée : lit les arguments et lance la vérification."""
    arguments = [a for a in sys.argv[1:] if not a.startswith("-")]
    options = [a for a in sys.argv[1:] if a.startswith("-")]
    if {"-h", "--help", "--aide"} & set(options):
        print(__doc__)
        return

    if arguments:
        dossier: Optional[Path] = trouver_exercice(arguments[0])
    else:
        dossier = exercice_courant()
    if dossier is None:
        afficher_progression()
        return

    seule = None
    if len(arguments) > 1:
        chiffres = re.sub(r"\D", "", arguments[1])
        if not chiffres:
            print(rouge(f"Numéro de question invalide : {arguments[1]}"))
            sys.exit(1)
        seule = int(chiffres)
    verifier_exercice(dossier, seule, "--solutions" in options)


if __name__ == "__main__":
    main()
