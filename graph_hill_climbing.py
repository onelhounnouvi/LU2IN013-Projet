from hill_climbing import *
import time
import matplotlib.pyplot as plt
import pandas as pd

def evaluer_hill_climbing_scores(textes_chiffres, dico_ref, nb_permutations_list, n_gramme_list):
    """Évalue l'efficacité du Hill Climbing en fonction du score final."""
    
    resultats = []
    
    for taille, message_chiffre in textes_chiffres.items():
        print(f"\n--- TEST SUR UN TEXTE DE {taille} CARACTÈRES ---")
        
        for n in n_gramme_list:
            scores = []  # Liste pour suivre l'évolution du score
            
            for nb_permutations in nb_permutations_list:
                print(f"Test avec {nb_permutations} permutations et n-grammes de taille {n}...")

                # Exécution du Hill Climbing
                start_time = time.time()
                texte_dechiffre,score_init = hill_climbing(message_chiffre, nb_permutations, dico_ref[n], n)
                elapsed_time = time.time() - start_time
                
                # Calcul du score final
                score_final = score(dico_ref[n], texte_dechiffre, n)
                scores.append(score_final)
                
                # Stocker les résultats
                resultats.append({
                    "Taille Texte": taille,
                    "n-gramme": n,
                    "Permutations": nb_permutations,
                    "Score Final": round(score_final, 2),
                    "Temps (s)": round(elapsed_time, 2)
                })
                
                print(f" -> Score Final : {score_final:.2f} | Temps : {elapsed_time:.2f}s")
            
            # Affichage du graphe d'évolution du score
            plt.plot(nb_permutations_list, scores, label=f"n={n}")
        
        # Tracer le graphique pour cette taille de texte
        plt.xlabel("Nombre de permutations")
        plt.ylabel("Score final")
        plt.title(f"Évolution du score pour un texte de {taille} caractères")
        plt.legend()
        plt.show()
    
    return resultats

# Charger les textes chiffrés
textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    509: file_to_str("chiffres/chiffre_germinal_22_509_1"),
    1150: file_to_str("chiffres/chiffre_germinal_58_1150_2")
}

# Charger le texte de référence (ex. : corpus nettoyé)
texte_ref = file_to_str("germinal_nettoye")

# Construire les dictionnaires de fréquences des n-grammes
n_gramme_list = [2, 3, 4]
dico_ngrams_ref = {n: normaliser_dico(dico_n_grammes(texte_ref, n)) for n in n_gramme_list}

# Tester différentes valeurs de permutations
nb_permutations_list = [200*i for i in range (1,40)]

# Lancer l'expérimentation
resultats = evaluer_hill_climbing_scores(textes_chiffres, dico_ngrams_ref, nb_permutations_list, n_gramme_list)

# Afficher les résultats sous forme de tableau
df = pd.DataFrame(resultats)
print(df)