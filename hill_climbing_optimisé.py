from substitution import *

def hill_climbing_optimise(message, nbPermutations, dico_ref, n):
    """Applique l'algorithme du Hill Climbing pour cryptanalyser le texte chiffré"""
    dico_perm = dico_permutation_alea()  #Génère une permutation aléatoire
    res = dechiffrer(message, dico_perm)
    scoreInit = score(dico_ref, res, n)  #Score initial avec les n-grammes
    meilleur_dico = dico_perm  # Initialisation de la meilleure clé
    meilleur_message = res  # Initialisation du meilleur dictionnaire (message déchiffré)
    meilleur_score = scoreInit  # Initialisation du meilleur score
    stagnation = 0
    max_stagnation = 200

    for _ in range(nbPermutations):
        new_dico_perm = permutation_alea(dico_perm)  #Applique la permutation
        new_message = dechiffrer(message, new_dico_perm)
        new_score = score(dico_ref, new_message, n)  # Score du message déchiffré
        if new_score < scoreInit:  # On cherche à MINIMISER le score
            res = new_message
            dico_perm = new_dico_perm
            scoreInit = new_score

            # Mise à jour du meilleur score et de la meilleure clé uniquement si c'est un meilleur score
            if new_score < meilleur_score:
                meilleur_dico = dico_perm
                meilleur_message = new_message
                meilleur_score = new_score
                stagnation = 0
        else:
            stagnation += 1
        if stagnation == max_stagnation:  # Réinitialisation après un certain nombre d'itérations
            dico_perm = dico_permutation_alea()
            res = dechiffrer(message, dico_perm)
            scoreInit = score(dico_ref, res, n)
            stagnation = 0

    print(f"Meilleur score trouve : {meilleur_score}")
    return meilleur_message, meilleur_score

"""corpus_ref = file_to_str("germinal_nettoye")
dico_ngrams = normaliser_dico(dico_n_grammes(corpus_ref, 4))

a_dechiffrer = file_to_str("chiffres/chiffre_germinal_52_1199_1")
print(hill_climbing_optimise(a_dechiffrer, 10000, dico_ngrams, 4))

str_to_file(texte, "resultat")
"""