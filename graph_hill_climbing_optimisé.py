import numpy as np
import matplotlib.pyplot as plt
from hill_climbing import hill_climbing_optimise
from substitution import file_to_str, normaliser_dico, dico_n_grammes


def evaluer_evolution_hill_climbing(message, nbPermutation_total, dico_ref, n, max_stagnation, repetitions, extraction_points):
    """Lance plusieurs répétitions du hill climbing amélioré, renvoie un tableau des scores moyens et extrait la valeur du score aux itérations d'intérêt"""
    all_extracted = []
    for rep in range(repetitions):
        _, _, history = hill_climbing_optimise(message, nbPermutation_total, dico_ref, n, max_stagnation)
        # Extraction
        extracted = [history[iter_idx - 1] for iter_idx in extraction_points if iter_idx <= len(history)]
        all_extracted.append(extracted)

    all_extracted = np.array(all_extracted)  # Forme (repetitions, nombre d'extraction_points)
    avg_scores = np.median(all_extracted, axis=0)
    return extraction_points, avg_scores


def evaluer_diff_stagnation_et_n(taille, message, nbPermutation_total, dico_ref, n_values, stagnation_values,
                                 repetitions, extraction_points):
    """Teste différentes valeurs de max_stagnation et différentes tailles des n-grammes puis trace un graphique."""
    for n in n_values:
        plt.figure(figsize=(10, 6))
        for max_stagnation in stagnation_values:
            print(f"\nTest pour n = {n} et max_stagnation = {max_stagnation}")
            iters, avg_scores = evaluer_evolution_hill_climbing(message, nbPermutation_total, dico_ref, n,
                                                                max_stagnation, repetitions, extraction_points)
            plt.plot(iters, avg_scores, label=f"Stagnation = {max_stagnation}")

            # Recherche du minimum de la courbe
            avg_scores_array = np.array(avg_scores)
            min_index = np.argmin(avg_scores_array)
            min_iteration = iters[min_index]
            min_score = avg_scores_array[min_index]

            # Marquer le minimum par un symbole "X" en noir
            plt.plot(min_iteration, min_score, marker='X', markersize=10, linestyle='None', color='black')

        plt.xlabel("Nombre d'itérations")
        plt.ylabel("Score moyen")
        plt.title(f"Evolution du score moyen (texte {taille}, n = {n})")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        filename = f"graphe_hill_climbing_taille{taille}_n{n}.png"
        plt.savefig(filename)
        plt.close()
        print(f"Graphique sauvegardé sous {filename}")


if __name__ == "__main__":
    # Chargement du texte chiffré et du texte de référence
    textes_chiffres = {
        110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
        509: file_to_str("chiffres/chiffre_germinal_22_509_1"),
        1150: file_to_str("chiffres/chiffre_germinal_58_1150_2")
    }
    texte_ref = file_to_str("germinal_nettoye")

    # Paramètres d'évaluation
    nbPermutation_total = 6000  # Nombre total d'itérations pour Hill Climbing
    repetitions = 100  # Nombre de répétitions pour chaque configuration
    extraction_points = list(range(5, nbPermutation_total + 1, 5))  #Points d'extraction pour le score moyen
    n_values = [4]
    stagnation_values = [50, 100, 150, 200]

    # Par exemple, on effectue les tests pour le texte de taille 509
    taille = 509
    message = textes_chiffres[taille]

    # Pour chaque valeur de n, on construit le dictionnaire de référence approprié
    for n in n_values:
        dico_ngrams_ref = normaliser_dico(dico_n_grammes(texte_ref, n))
        # On teste différentes valeurs de max_stagnation pour l'algorithme
        evaluer_diff_stagnation_et_n(taille, message, nbPermutation_total, dico_ngrams_ref, [n], stagnation_values,
                                     repetitions, extraction_points)