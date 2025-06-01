import numpy as np
import matplotlib.pyplot as plt
from recuit_simule import *

def evaluer_evolution(message, nbPermutation_total, dico_ref, n, cool_ratio, cool_time, repetitions, extraction_points):
    """Lance plusieurs répétitions du recuit simulé, renvoie un tableau des scores moyens et extrait la valeur du score aux itérations d'intérêt"""

    T_initial = calculer_temperature_initiale(message, dico_ref, n)
    print(f"Température initiale : {T_initial:.2f}")
    all_extracted = []

    for rep in range(repetitions):
        _, _, history = recuit_simule(message, nbPermutation_total, dico_ref, n, cool_ratio, cool_time, T_initial)
        # Extraire les valeurs aux itérations souhaitées (attention à l'indexation : itération 1500 -> index 1499)
        extracted = [history[iter_idx - 1] for iter_idx in extraction_points if iter_idx <= len(history)]
        all_extracted.append(extracted)

    all_extracted = np.array(all_extracted)  # Forme (repetitions, nombre d'extraction_points)
    avg_scores = np.mean(all_extracted, axis=0)
    return extraction_points, avg_scores


def evaluer_diff_cool_ratios(taille, message, nbPermutation_total, dico_ref, n, cool_ratios, repetitions, cool_time,
                             extraction_points):
    """Teste plusieurs valeurs de cool_ratio pour un même message et trace un graphique"""
    results = {}
    for cr in cool_ratios:
        print(f"\nTest pour cool_ratio = {cr}")
        iters, avg_scores = evaluer_evolution(message, nbPermutation_total, dico_ref, n, cr, cool_time, repetitions,
                                              extraction_points)
        results[cr] = avg_scores

    # Tracé des courbes pour chaque cool_ratio
    plt.figure(figsize=(10, 6))
    for cr, avg_scores in results.items():
        plt.plot(iters, avg_scores, marker = 'o', label=f"cool_ratio = {cr}")
    plt.xlabel("Nombre d'itérations")
    plt.ylabel("Score moyen")
    plt.title(f"Évolution du score moyen en fonction des itérations. Texte de taille {taille}.\nRefroidissement toutes les 1000 itérations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Sauvegarde automatique dans un fichier
    filename = f"graphe_recuit_{taille}_cool_ratios.png"
    plt.savefig(filename)
    plt.close()  # Ferme la figure pour éviter de saturer la mémoire

    print(f"Graphique sauvegardé sous {filename}")
    return results

"""Programme principal"""
# Chargement du texte chiffré et du texte de référence (par exemple, un texte de 500 caractères)
textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    509: file_to_str("chiffres/chiffre_germinal_22_509_1"),
    1150: file_to_str("chiffres/chiffre_germinal_58_1150_2")
}

texte_ref = file_to_str("germinal_nettoye")
n = 4  #Taille des n-grammes
dico_ngrams_ref = normaliser_dico(dico_n_grammes(texte_ref, n))

# Paramètres d'évaluation
nbPermutation_total = 6000  # Exécuter chaque simulation sur 6000 itérations
extraction_points = list(range(200, nbPermutation_total + 1, 200))
cool_ratios = [0.75, 0.6, 0.45, 0.3, 0.15]  # Valeurs testées
repetitions = 100  # Nombre de répétitions pour chaque configuration
cool_time = 1000  # Nombre d'itérations entre chaque refroidissement

# Lancer l'évaluation pour comparer les courbes pour différents cool_ratios
for taille, message_chiffre in textes_chiffres.items():
    results = evaluer_diff_cool_ratios(taille, message_chiffre, nbPermutation_total, dico_ngrams_ref, n, cool_ratios,
                                       repetitions, cool_time, extraction_points)