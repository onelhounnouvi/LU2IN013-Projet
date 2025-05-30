from hill_climbing import *
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def evaluer_moyenne_scores(
    textes_chiffres, 
    texte_ref, 
    nb_permutations_list, 
    n_gramme, 
    repetitions=25, 
    stagnations_testees=[200]
):
    """Évalue les scores moyens du Hill Climbing pour différentes stagnations et affiche un graphe unique par taille de texte."""
    
    # Préparer le dictionnaire de fréquence pour le n-gramme choisi
    dico_ngrams_ref = {n_gramme: normaliser_dico(dico_n_grammes(texte_ref, n_gramme))}

    resultats = []

    for taille, message_chiffre in textes_chiffres.items():
        print(f"\n=== TEST SUR UN TEXTE DE {taille} CARACTÈRES | n-gramme = {n_gramme} ===")

        plt.figure(figsize=(10, 6))

        for max_stagnation in stagnations_testees:
            moyennes_scores = []

            print(f"--- Stagnation max = {max_stagnation} ---")
            for nb_permutations in nb_permutations_list:
                print(f" -> {nb_permutations} permutations ({repetitions} répétitions)...")

                scores_repetition = []
                temps_repetition = []

                for _ in range(repetitions):
                    start_time = time.time()
                    texte_dechiffre, score_init = hill_climbing(
                        message_chiffre,
                        nb_permutations,
                        dico_ngrams_ref[n_gramme],
                        n_gramme,
                        max_stagnation=max_stagnation
                    )
                    elapsed_time = time.time() - start_time

                    score_final = score(dico_ngrams_ref[n_gramme], texte_dechiffre, n_gramme)
                    scores_repetition.append(score_final)
                    temps_repetition.append(elapsed_time)

                moyenne_score = np.mean(scores_repetition)
                ecart_type_score = np.std(scores_repetition)
                moyenne_temps = np.mean(temps_repetition)

                moyennes_scores.append(moyenne_score)

                resultats.append({
                    "Taille Texte": taille,
                    "n-gramme": n_gramme,
                    "Permutations": nb_permutations,
                    "Score Moyen": round(moyenne_score, 2),
                    "Écart-type": round(ecart_type_score, 2),
                    "Temps Moyen (s)": round(moyenne_temps, 2),
                    "Stagnation Max": max_stagnation
                })

                print(f"    > Moyenne : {moyenne_score:.2f} | Écart-type : {ecart_type_score:.2f} | Temps moyen : {moyenne_temps:.2f}s")

            # Tracer la courbe pour cette valeur de stagnation
            plt.plot(nb_permutations_list, moyennes_scores, marker='o', label=f"Stagnation max = {max_stagnation}")
            
        # Graphique global pour cette taille de texte
        min_perm = min(nb_permutations_list)
        max_perm = max(nb_permutations_list)

        plt.xlabel("Nombre de permutations")
        plt.ylabel("Score moyen")
        plt.title(
            f"Hill Climbing – Score moyen pour {taille} caractères | n-gramme = {n_gramme} | "
            f"{repetitions} répétitions"
        )
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        filename = f"hillclimb_n{n_gramme}_taille{taille}_perm{min_perm}-{max_perm}.png"
        plt.savefig(filename)
        plt.show()


    return resultats


# --- Chargement des données ---
textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    509: file_to_str("chiffres/chiffre_germinal_22_509_1"),
    1150: file_to_str("chiffres/chiffre_germinal_58_1150_2")
}

texte_ref = file_to_str("germinal_nettoye")

# --- Paramètres ---
n_gramme_choisi = 4
repetitions = 200
nb_permutations_list = list(range(100, 2001, 100))  # exemple réduit
stagnations_testees = [150,200, 250, 300]

# --- Exécution ---
resultats = evaluer_moyenne_scores(
    textes_chiffres,
    texte_ref,
    nb_permutations_list,
    n_gramme_choisi,
    repetitions,
    stagnations_testees
)

# --- Affichage final ---
df = pd.DataFrame(resultats)
print(df)
