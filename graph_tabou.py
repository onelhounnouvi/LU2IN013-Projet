import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabou import recherche_tabou
from substitution import *

def evaluer_tabou_heatmap(message, dico_ref, n, tabu_sizes, iteration_counts, repetitions):
    """Évalue les scores finaux moyens pour différentes combinaisons (tabu_size, nb_iter)"""
    heatmap_data = np.zeros((len(tabu_sizes), len(iteration_counts)))

    for i, ts in enumerate(tabu_sizes):
        for j, nb_iter in enumerate(iteration_counts):
            scores = []
            for _ in range(repetitions):
                _, score_final, _ = recherche_tabou(message, nb_iter, dico_ref, n, tabu_size=ts)
                scores.append(score_final)
            heatmap_data[i, j] = np.mean(scores)
            print(f"tabu_size={ts}, iter={nb_iter}, avg_score={heatmap_data[i, j]:.2f}")

    return heatmap_data

def tracer_heatmap(data, tabu_sizes, iteration_counts, taille_texte):
    plt.figure(figsize=(12, 8))
    sns.heatmap(data, xticklabels=iteration_counts, yticklabels=tabu_sizes, annot=True, fmt=".1f", cmap="viridis")
    plt.xlabel("Nombre d'itérations")
    plt.ylabel("Taille de la liste tabou")
    plt.title(f"Score moyen final – Recherche tabou (texte {taille_texte})")
    plt.tight_layout()
    filename = f"heatmap_tabou_{taille_texte}_dense.png"
    plt.savefig(filename)
    plt.close()
    print(f"Heatmap sauvegardée sous {filename}")

"""Programme principal"""
textes_chiffres = {
    509: file_to_str("chiffres/chiffre_germinal_22_509_1"),
    1150: file_to_str("chiffres/chiffre_germinal_58_1150_2")
}
#110: file_to_str("chiffres/chiffre_germinal_20_110_1") a rajouter dedans une fois exécution fini

texte_ref = file_to_str("germinal_nettoye")
n = 3
tabu_sizes = list(range(100, 500, 30))         # ➤ [10, 40, 70, ..., 190]
iteration_counts = list(range(100, 500, 30))   # ➤ [10, 40, 70, ..., 190]
repetitions = 30  # Peut être réduit à 10–20 pour tests rapides

for taille, message in textes_chiffres.items():
    dico_ref = normaliser_dico(dico_n_grammes(texte_ref, n))
    data = evaluer_tabou_heatmap(message, dico_ref, n, tabu_sizes, iteration_counts, repetitions)
    tracer_heatmap(data, tabu_sizes, iteration_counts, taille)