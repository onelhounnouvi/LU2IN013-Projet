from substitution import file_to_str, normaliser_dico, dico_n_grammes, score
from recuit_simule import recuit_simule
import time
import matplotlib.pyplot as plt


def evaluer_recuit_simule_scores(textes_chiffres, dico_ref, nb_permutations_list, n_gramme_list, cool_ratio_list):
    """Évalue l'efficacité du recuit simulé en fonction du score final, du nombre de permutations,
    de la taille des n-grammes et du coefficient de refroidissement."""

    resultats = []

    for taille, message_chiffre in textes_chiffres.items():
        print(f"\n--- TEST SUR UN TEXTE DE {taille} CARACTÈRES ---")

        for n in n_gramme_list:
            for cool_ratio in cool_ratio_list:
                scores = []  # Pour suivre l'évolution du score final selon le nombre de permutations
                for nb_permutations in nb_permutations_list:
                    print(
                        f"Test avec {nb_permutations} permutations, n-gramme de taille {n} et cool_ratio={cool_ratio}...")

                    start_time = time.time()
                    texte_dechiffre, score_final = recuit_simule(message_chiffre, nb_permutations, dico_ref[n], n, cool_ratio)
                    elapsed_time = time.time() - start_time

                    scores.append(score_final)

                    resultats.append({
                        "Taille Texte": taille,
                        "n-gramme": n,
                        "Permutations": nb_permutations,
                        "Cool_ratio": cool_ratio,
                        "Score Final": round(score_final, 2),
                        "Temps (s)": round(elapsed_time, 2)
                    })

                    print(f" -> Score Final : {score_final:.2f} | Temps : {elapsed_time:.2f}s")

                # Affichage de l'évolution du score pour la configuration (n, cool_ratio)
                plt.plot(nb_permutations_list, scores, label=f"n={n}, cool_ratio={cool_ratio}")

            plt.xlabel("Nombre de permutations")
            plt.ylabel("Score Final")
            plt.title(f"Évolution du score pour un texte de {taille} caractères (n={n})")
            plt.legend()
            plt.show()

    return resultats


# Chargement des textes chiffrés
textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    509: file_to_str("chiffres/chiffre_germinal_22_509_1"),
    1150: file_to_str("chiffres/chiffre_germinal_58_1150_2")
}

# Chargement du texte de référence
texte_ref = file_to_str("germinal_nettoye")

# Construction des dictionnaires de fréquences des n-grammes pour les tailles voulues
n_gramme_list = [2, 3, 4]
dico_ngrams_ref = {n: normaliser_dico(dico_n_grammes(texte_ref, n)) for n in n_gramme_list}

# Définition de la liste des nombres de permutations à tester
nb_permutations_list = [250 * i for i in range(1, 121)]

# Définition de plusieurs valeurs pour le coefficient de refroidissement
cool_ratio_list = [0.9, 0.7, 0.5, 0.09]

# Lancement de l'expérimentation
resultats_recuit = evaluer_recuit_simule_scores(textes_chiffres, dico_ngrams_ref, nb_permutations_list, n_gramme_list,
                                                cool_ratio_list)
