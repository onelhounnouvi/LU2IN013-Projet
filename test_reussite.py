import numpy as np
from matplotlib import pyplot as plt
from hill_climbing import *
from recuit_simule import *
from tabou import *

corpus_ref = file_to_str("germinal_nettoye")
FREQS_LETTRES = normaliser_dico(dico_n_grammes(corpus_ref, 1))

def taux_comprehension(dico_trouve, dico_cle):
    """Calcule le taux de compréhension (entre 0 et 1) en prenant en compte le dictionnaire de chiffrement
    et celui trouvé par cryptanalyse tout en pondérant par la fréquence d'apparition de chaque lettre en français."""

    correct_weight = 0.0
    for lettre, substitution_correcte in dico_cle.items():
        poids = FREQS_LETTRES.get(lettre, 0)
        if dico_trouve.get(lettre, "") == substitution_correcte:
            correct_weight += poids

    return correct_weight  #La division par le poids total n'est pas nécessaire, car les fréquences sont normalisées


def evaluer_taux_reussite(metaheur_func, message, dico_clair, repetitions, seuil, **params):
    """Fonction générique d'évaluation du taux de réussite d'une méthode de cryptanalyse.
        **params: paramètres spécifiques pour la fonction de cryptanalyse
    """
    succes = 0
    for _ in range(repetitions):
        _,_,_,dico_trouve = metaheur_func(message, **params)
        ratio = taux_comprehension(dico_trouve, dico_clair)
        if ratio >= seuil:
            succes += 1
    return (succes / repetitions) * 100

# Chargement des textes
textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    205: file_to_str("chiffres/chiffre_germinal_5_205_1"),
    318: file_to_str("chiffres/chiffre_germinal_3_318_1"),
    509: file_to_str("chiffres/chiffre_germinal_22_509_1")
}

dicos_clairs = {
    110: {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'X', 'E': 'L', 'F': 'H', 'G': 'K', 'H': 'H', 'I': 'V', 'J': 'J', 'K': 'K', 'L': 'S', 'M': 'P', 'N': 'B', 'O': 'M', 'P': 'O', 'Q': 'E', 'R': 'R', 'S': 'Y', 'T': 'D', 'U': 'N', 'V': 'W', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'},
    205: {'A': 'T', 'B': 'B', 'C': 'D', 'D': 'H', 'E': 'Z', 'F': 'F', 'G': 'O', 'H': 'U', 'I': 'F', 'J': 'J', 'K': 'K', 'L': 'P', 'M': 'X', 'N': 'C', 'O': 'N', 'P': 'L', 'Q': 'V', 'R': 'Y', 'S': 'K', 'T': 'J', 'U': 'B', 'V': 'M', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'I'},
    318: {'A': 'N', 'B': 'R', 'C': 'B', 'D': 'C', 'E': 'T', 'F': 'V', 'G': 'X', 'H': 'Q', 'I': 'M', 'J': 'A', 'K': 'K', 'L': 'D', 'M': 'L', 'N': 'J', 'O': 'S', 'P': 'Y', 'Q': 'E', 'R': 'U', 'S': 'F', 'T': 'I', 'U': 'W', 'V': 'H', 'W': 'W', 'X': 'Z', 'Y': 'G', 'Z': 'O'},
    509: {'A': 'T', 'B': 'X', 'C': 'G', 'D': 'Z', 'E': 'B', 'F': 'D', 'G': 'A', 'H': 'I', 'I': 'R', 'J': 'J', 'K': 'K', 'L': 'Y', 'M': 'Q', 'N': 'W', 'O': 'U', 'P': 'K', 'Q': 'E', 'R': 'V', 'S': 'O', 'T': 'C', 'U': 'J', 'V': 'P', 'W': 'W', 'X': 'X', 'Y': 'S', 'Z': 'Z'}
}

# --- Paramètres globaux ---
repetitions = 500
nbPerm = 8000
seuil = 0.9

# --- Paramètres optimaux
n_gramme = 3
max_stagnation_classique = 400
max_stagnation_opt = 300
cool_ratio = 0.75
cool_time = 200
tabu_nb_iter = 100

# --- Listes de stockage des taux de réussite ---
rates_hc = []
rates_hco = []
rates_rs = []
rates_tb = []

# Avant la boucle principale
dico_ref = normaliser_dico(dico_n_grammes(corpus_ref, n_gramme))

# --- Boucle sur chaque taille de texte ---
for taille, msg_chiffre in textes_chiffres.items():
    print(f"Sur texte {taille}")

    # Hill Climbing Classique
    print("Hill Climbing Classique")
    taux_hc = evaluer_taux_reussite(
        hill_climbing,
        message=msg_chiffre, dico_clair=dicos_clairs[taille], repetitions=repetitions,
        seuil=seuil, nbPermutations=nbPerm, dico_ref=dico_ref, n=n_gramme, max_stagnation=max_stagnation_classique
    )
    rates_hc.append(taux_hc)

    # Hill Climbing Optimisé
    print("Hill Climbing Optimisé")
    taux_hco = evaluer_taux_reussite(
        hill_climbing_optimise,
        message=msg_chiffre, dico_clair=dicos_clairs[taille], repetitions=repetitions, seuil=seuil,
        nbPermutations=nbPerm, dico_ref=dico_ref, n=n_gramme, max_stagnation=max_stagnation_opt
    )
    rates_hco.append(taux_hco)

    # Recuit Simulé
    print("Recuit simulé")
    t_init = calculer_temperature_initiale(msg_chiffre, dico_ref, n_gramme)
    taux_rs = evaluer_taux_reussite(
        recuit_simule,
        message=msg_chiffre, dico_clair=dicos_clairs[taille], repetitions=repetitions, seuil=seuil,
        nbPermutations=nbPerm, dico_ref=dico_ref, n=n_gramme, cool_ratio=cool_ratio, cool_time=cool_time,
        t_initial=t_init
    )
    rates_rs.append(taux_rs)

    # Recherche Tabou
    print("Recherche Tabou")
    taux_tb = evaluer_taux_reussite(
        recherche_tabou,
        message=msg_chiffre, dico_clair=dicos_clairs[taille], repetitions=repetitions, seuil=seuil,
        nb_iter=tabu_nb_iter, dico_ref=dico_ref, n=n_gramme
    )
    rates_tb.append(taux_tb)

# --- Affichage graphique ---
x = np.arange(len(rates_hc))
width = 0.15

plt.figure(figsize=(12, 6))
plt.bar(x - 1.5 * width, rates_hc, width, label="Hill Climbing")
plt.bar(x - 0.5 * width, rates_hco, width, label="Hill Climbing optimisé")
plt.bar(x + 0.5 * width, rates_rs, width, label="Recuit simulé")
plt.bar(x + 1.5 * width, rates_tb, width, label="Recherche tabou")

plt.xticks(x, sorted(textes_chiffres.keys()))
plt.xlabel("Longueur du texte chiffré")
plt.ylabel("Taux de réussite (%)")
plt.title(f"Taux de réussite")
plt.legend()
plt.grid(True, axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(f"taux_reussite.png")
print("Fichier sauvegardé")
plt.close()