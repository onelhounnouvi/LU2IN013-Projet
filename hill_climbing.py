from substitution import *


def hill_climbing(message, nbPermutations, dico_ref, n, max_stagnation):
    """Applique l'algorithme du Hill Climbing pour cryptanalyser le texte chiffré
    et s'arrête dès que le nombre maximal d'itérations sans amélioration est atteint."""

    dico_courant = dico_permutation_alea()  # Génère une permutation aléatoire
    message_courant = dechiffrer(message, dico_courant)
    score_courant = score(dico_ref, message_courant, n)  # Score initial avec les n-grammes
    stagnation = 0

    for _ in range(nbPermutations):
        dico_voisin = modifier_cle(dico_courant)  # Modifie légèrement la clé
        message_voisin = dechiffrer(message, dico_voisin)
        score_voisin = score(dico_ref, message_voisin, n)

        if score_voisin < score_courant:  # On cherche à MINIMISER
            message_courant = message_voisin
            dico_courant = dico_voisin
            score_courant = score_voisin
            stagnation = 0  # Réinitialisation du compteur en cas d'amélioration
        else:
            stagnation += 1

        if stagnation == max_stagnation:
            print(f"Arrêt du hill climbing après {stagnation} itérations sans amélioration.")
            print(f"Meilleur score trouvé : {score_courant}")
            return message_courant, score_courant

    print(f"Meilleur score trouvé : {score_courant}")
    return message_courant, score_courant


def hill_climbing_ameliore(message, nbPermutations, dico_ref, n, max_stagnation):
    """Applique une version améliorée du Hill Climbing pour cryptanalyser le texte chiffré."""

    # Initialisation de l'état courant
    dico_courant = dico_permutation_alea()
    message_courant = dechiffrer(message, dico_courant)
    score_courant = score(dico_ref, message_courant, n)

    # Sauvegarde de la meilleure solution trouvée jusqu'à présent
    meilleur_dico = dico_courant
    meilleur_message = message_courant
    meilleur_score = score_courant

    stagnation = 0
    score_history = []  # Contiendra le score courant à chaque itération

    for _ in range(nbPermutations):
        new_dico = modifier_cle(dico_courant)
        new_message = dechiffrer(message, new_dico)
        new_score = score(dico_ref, new_message, n)

        if new_score < score_courant:  # Minimisation
            dico_courant = new_dico
            message_courant = new_message
            score_courant = new_score
            stagnation = 0

            # Mise à jour de la meilleure solution globale si nécessaire
            if new_score < meilleur_score:
                meilleur_dico = new_dico
                meilleur_message = new_message
                meilleur_score = new_score
        else:
            stagnation += 1

        score_history.append(score_courant)

        if stagnation == max_stagnation:  # Réinitialisation en cas de stagnation trop longue
            print(f"Réinitialisation après {stagnation} itérations.")
            dico_courant = dico_permutation_alea()
            message_courant = dechiffrer(message, dico_courant)
            score_courant = score(dico_ref, message_courant, n)
            stagnation = 0

    print(f"Meilleur score trouvé : {meilleur_score}")
    return meilleur_message, meilleur_score, score_history

"""corpus_ref = file_to_str("germinal_nettoye")
dico_ngrams = normaliser_dico(dico_n_grammes(corpus_ref, 4))

a_dechiffrer = file_to_str("chiffres/chiffre_germinal_22_509_1")
texte, scoref, _ = hill_climbing_ameliore(a_dechiffrer, 5000, dico_ngrams, 4, 50)

str_to_file(texte, "resultat")"""