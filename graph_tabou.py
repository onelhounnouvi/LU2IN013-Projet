import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabou import recherche_tabou
from substitution import *

def evaluer_tabou_iterations(message, dico_ref, n, tabu_size, iteration_counts, repetitions):
    """Évalue les scores finaux moyens pour différents nombres d'itérations avec une tabu_size fixe"""
    moyennes = []

    for nb_iter in iteration_counts:
        scores = []
        for _ in range(repetitions):
            _, score_final, _ = recherche_tabou(message, nb_iter, dico_ref, n, tabu_size=tabu_size)
            scores.append(score_final)
        moyenne = np.mean(scores)
        moyennes.append(moyenne)
        print(f"iter={nb_iter}, avg_score={moyenne:.2f}")

    return moyennes


def tracer_courbe(scores_moyens, iteration_counts, taille_texte, score_clair):
    plt.figure(figsize=(10, 6))
    plt.plot(iteration_counts, scores_moyens, marker='o', linestyle='-', color='blue', label='Score moyen (tabou)')
    
    # Ligne horizontale rouge pour le score du texte clair
    plt.axhline(
        y=score_clair,
        color='red',
        linestyle='--',
        linewidth=2,
        label=f'Score texte clair ≈ {score_clair:.2f}'
    )

    plt.xlabel("Nombre d'itérations")
    plt.ylabel("Score moyen final")
    plt.title(f"Évolution du score – Recherche tabou (texte {taille_texte})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    filename = f"courbe_tabou_{taille_texte}.png"
    plt.savefig(filename)
    plt.close()
    print(f"Courbe sauvegardée sous {filename}")




"""Programme principal"""
textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    205: file_to_str("chiffres/chiffre_germinal_5_205_1"),
    318: file_to_str("chiffres/chiffre_germinal_3_318_1")
}
textes_clairs = {
    110: "ETTOUTLETEMPSQUELESVISITEURSRESTERENTENFACEELLESENDEGOISERENTLESVOILAQUISORTENTDITENFINLALEVAQUEILSFONTLETOUR",
    205: "ETMAHEUSEDESESPERAITENCOREDELAMALCHANCEVOILAQUILPERDAITUNEDESESHERSCHEUSESSANSPOUVOIRLAREMPLACERIMMEDIATEMENTILTRAVAILLAITAUMARCHANDAGEILSETAIENTQUATREHAVEURSASSOCIESDANSSATAILLELUIBACHARIELEVAQUEETCHAVAL ",
    318: "ALZIRELESYEUXGRANDSOUVERTSREGARDAITTOUJOURSLESDEUXMIOCHESLENOREETHENRIAUXBRASLUNDELAUTRENAVAIENTPASREMUERESPIRANTDUMEMEPETITSOUFFLEMALGRELEVACARMECATHERINEDONNEMOILACHANDELLECRIAMAHEUELLEFINISSAITDEBOUTONNERSAVESTEELLEPORTALACHANDELLEDANSLECABINETLAISSANTSESFRERESCHERCHERLEURSVETEMENTSAUPEUDECLARTEQUIVENAITDELAPORTE"
}

texte_ref = file_to_str("germinal_nettoye")
n=3
tabu_size = 1000000  # Par exemple
iteration_counts = list(range(10, 151, 10))
repetitions = 200

for taille, message in textes_chiffres.items():
    dico_ref = normaliser_dico(dico_n_grammes(texte_ref, n))
    texte_clair = textes_clairs[taille]
    score_clair = score(dico_ref, texte_clair, n)

    scores_moyens = evaluer_tabou_iterations(message, dico_ref, n, tabu_size, iteration_counts, repetitions)
    tracer_courbe(scores_moyens, iteration_counts, taille, score_clair)
