from hill_climbing import *
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def evaluer_moyenne_scores(textes_chiffres, dico_ref, nb_permutations_list, n, repetitions=25, max_stagnation=200):
    """Évalue le score moyen du Hill Climbing et affiche un graphe par taille de texte."""
    
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
                texte_dechiffre, score_init = hill_climbing(
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
              # Tracer le graphique pour cette taille de texte
        plt.figure(figsize=(10, 6))
        plt.plot(nb_permutations_list, moyennes_scores, marker='o', color='tab:blue')
        plt.xlabel("Nombre de permutations")
        plt.ylabel("Score moyen")
        plt.title(f"Score moyen - {taille} caractères (n = {n}, {repetitions} rép., stagnation max = {max_stagnation})")
        plt.grid(True)
        plt.tight_layout()
        filename = f"graphe_scoremoyen_n{n}_taille{taille}_stagn{max_stagnation}.png"
        plt.savefig(filename)
        plt.show()


    return resultats


# Charger les textes chiffrés
textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    509: file_to_str("chiffres/chiffre_germinal_22_509_1"),
    1150: file_to_str("chiffres/chiffre_germinal_58_1150_2")
}

# Charger le texte de référence
texte_ref = file_to_str("germinal_nettoye")

# Paramètres à ajuster
n_gramme_choisi = 4  # Tu peux mettre 2, 3, ou 4 par exemple
repetitions = 200
nb_permutations_list = list(range(200, 3001, 100))  # De 200 à 2000 par pas de 100
max_stagnation = 150

# Dictionnaire des fréquences pour le n-gramme choisi
dico_ngrams_ref = {n_gramme_choisi: normaliser_dico(dico_n_grammes(texte_ref, n_gramme_choisi))}

# Lancer l'expérimentation
resultats = evaluer_moyenne_scores(
    textes_chiffres,
    dico_ngrams_ref,
    nb_permutations_list,
    n_gramme_choisi,
    repetitions,
    max_stagnation
)

# Afficher le tableau final
df = pd.DataFrame(resultats)
print(df)
