from hill_climbing_optimisé import *
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def evaluer_moyenne_scores_optimise(textes_chiffres, dico_ref, nb_permutations_list, n, repetitions=25, max_stagnation=200):
    """Évalue le score moyen du Hill Climbing optimisé et affiche un graphe par taille de texte."""
    
    resultats = []

    for taille, message_chiffre in textes_chiffres.items():
        print(f"\n--- TEST SUR UN TEXTE DE {taille} CARACTÈRES | n-gramme = {n} ---")
        
        moyennes_scores = []

        for nb_permutations in nb_permutations_list:
            print(f" -> Test avec {nb_permutations} permutations ({repetitions} répétitions)...")
            
            scores_repetition = []
            temps_repetition = []

            for _ in range(repetitions):
                start_time = time.time()
                texte_dechiffre, _ = hill_climbing_optimise(
                    message_chiffre,
                    nb_permutations,
                    dico_ref[n],
                    n,
                    max_stagnation=max_stagnation
                )
                elapsed_time = time.time() - start_time

                score_final = score(dico_ref[n], texte_dechiffre, n)
                scores_repetition.append(score_final)
                temps_repetition.append(elapsed_time)
            
            moyenne_score = np.mean(scores_repetition)
            ecart_type_score = np.std(scores_repetition)
            moyenne_temps = np.mean(temps_repetition)

            moyennes_scores.append(moyenne_score)

            resultats.append({
                "Taille Texte": taille,
                "n-gramme": n,
                "Permutations": nb_permutations,
                "Score Moyen": round(moyenne_score, 2),
                "Écart-type": round(ecart_type_score, 2),
                "Temps Moyen (s)": round(moyenne_temps, 2),
                "Stagnation Max": max_stagnation
            })

            print(f"    > Moyenne : {moyenne_score:.2f} | Écart-type : {ecart_type_score:.2f} | Temps moyen : {moyenne_temps:.2f}s")

        # Tracer le graphique pour cette taille de texte
        plt.figure(figsize=(10, 6))
        plt.plot(nb_permutations_list, moyennes_scores, marker='o', color='tab:green')
        plt.xlabel("Nombre de permutations")
        plt.ylabel("Score moyen")
        plt.title(f"Score moyen (Optimisé) - {taille} caractères (n = {n}, {repetitions} rép., stagnation max = {max_stagnation})")
        plt.grid(True)
        plt.tight_layout()
        filename = f"graphe_scoremoyen_optimise_n{n}_taille{taille}_stagn{max_stagnation}.png"
        plt.savefig(filename)
        plt.show()

    return resultats

# Paramètres
n_gramme_choisi = 4
repetitions = 200
nb_permutations_list = list(range(200, 2001, 100))
max_stagnation = 150

# Texte et dictionnaires
texte_ref = file_to_str("germinal_nettoye")
dico_ngrams_ref = {n_gramme_choisi: normaliser_dico(dico_n_grammes(texte_ref, n_gramme_choisi))}
textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    509: file_to_str("chiffres/chiffre_germinal_22_509_1"),
    1150: file_to_str("chiffres/chiffre_germinal_58_1150_2")
}

# Lancer les tests
resultats_optimise = evaluer_moyenne_scores_optimise(
    textes_chiffres,
    dico_ngrams_ref,
    nb_permutations_list,
    n_gramme_choisi,
    repetitions,
    max_stagnation
)

# Affichage final
df_optimise = pd.DataFrame(resultats_optimise)
print(df_optimise)
