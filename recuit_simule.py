from substitution import *

def recuit_simule(message, nbPermutations, dico_ref, n, cool_ratio):
    """Applique l'algorithme du recuit simulé pour cryptanalyser le texte chiffré"""
    dico_perm = dico_permutation_alea()  #Génère une permutation aléatoire
    res = dechiffrer(message, dico_perm)
    score_courant = score(dico_ref, res, n)

    meilleur_dico = dico_perm
    meilleur_message = res
    meilleur_score = score_courant

    deltas = []
    for i in range(100):
        new_dico_perm = dico_permutation_alea()  #Génère une permutation aléatoire
        new_res = dechiffrer(message, new_dico_perm)
        new_score = score(dico_ref, new_res, n)
        deltas.append(abs(new_score - score_courant))
    T = 10 * (sum(deltas) / len(deltas))          #Initialisation de la "température"

    max_it = 2000

    for i in range(nbPermutations):
        dico_voisin = permutation_alea(dico_perm)  #Choisir au hasard une clé voisine
        message_voisin = dechiffrer(message, dico_voisin)
        score_voisin = score(dico_ref, message_voisin, n)
        delta = score_voisin - score_courant
        if delta < 0 or random.random() < math.exp(-delta/T):
            dico_perm = dico_voisin
            res = message_voisin
            score_courant = score_voisin
            if score_courant < meilleur_score:  # Mise à jour du meilleur score
                meilleur_score = score_courant
                meilleur_dico = dico_perm
                meilleur_message = res

        if i != 0 and i%max_it == 0:
            print(f"Refroidissement apres {max_it} iterations")
            T *= cool_ratio    # Abaissement progressif de la température (Refroidissement)

    print(f"Meilleur score trouve : {meilleur_score}")
    return meilleur_message