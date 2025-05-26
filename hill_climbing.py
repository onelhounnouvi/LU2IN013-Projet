from substitution import *

def hill_climbing(message, nbPermutations, dico_ref, n, max_stagnation):
    """Applique l'algorithme du Hill Climbing pour cryptanalyser le texte chiffré"""
    dico_perm = dico_permutation_alea()  # Génère une permutation aléatoire
    res = dechiffrer(message, dico_perm)
    scoreInit = score(dico_ref, res, n)  # Score initial avec les n-grammes
    stagnation = 0

    for _ in range(nbPermutations):
        new_dico_perm = permutation_alea(dico_perm)  # Applique la permutation
        new_message = dechiffrer(message, new_dico_perm)
        new_score = score(dico_ref, new_message, n)  # Score du message déchiffré
        if new_score < scoreInit:  # On cherche à MINIMISER le score
            res = new_message
            dico_perm = new_dico_perm
            scoreInit = new_score
            stagnation = 0
        else:
            stagnation += 1
        if stagnation == max_stagnation:
            return res, scoreInit
    return res, scoreInit


"""
corpus_ref = file_to_str("germinal_nettoye")
dico_ngrams = normaliser_dico(dico_n_grammes(corpus_ref, 4))

a_dechiffrer = file_to_str("chiffres/chiffre_germinal_52_1199_1")
print(hill_climbing(a_dechiffrer, 2000, dico_ngrams, 4, 200))
"""
