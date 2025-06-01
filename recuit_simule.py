from substitution import *

def calculer_temperature_initiale(message, dico_ref, n):
    """Calcule la température initiale en effectuant 100 essais pour estimer la variation moyenne du score."""
    res = dechiffrer(message, dico_permutation_alea())
    score_courant = score(dico_ref, res, n)
    deltas = []
    for i in range(100):
        new_res = dechiffrer(message, dico_permutation_alea())
        new_score = score(dico_ref, new_res, n)
        deltas.append(abs(new_score - score_courant))
        score_courant = new_score
    T_initial = 10 * (sum(deltas) / len(deltas))
    return T_initial

def recuit_simule(message, nbPermutations, dico_ref, n, cool_ratio, cool_time, T_init):
    """Applique l'algorithme du recuit simulé pour cryptanalyser le texte chiffré"""
    dico_perm = dico_permutation_alea()  #Génère une permutation aléatoire
    res = dechiffrer(message, dico_perm)
    score_courant = score(dico_ref, res, n)

    meilleur_dico = dico_perm
    meilleur_message = res
    meilleur_score = score_courant
    T = T_init
    print(f"Température initiale : {T:.2f}")
    score_history = []  #Contiendra le score courant à chaque itération

    for i in range(nbPermutations):
        dico_voisin = modifier_cle(dico_perm)  #Choisir au hasard une clé voisine
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

        score_history.append(score_courant)
        if i != 0 and i%cool_time == 0:
            print(f"Refroidissement apres {cool_time} iterations")
            T *= cool_ratio    #Abaissement de la température (Refroidissement)

    print(f"Meilleur score trouve : {meilleur_score}")
    return meilleur_message, meilleur_score, score_history

"""corpus_ref = file_to_str("germinal_nettoye")
dico_ngrams = normaliser_dico(dico_n_grammes(corpus_ref, 4))

a_dechiffrer = file_to_str("chiffres/chiffre_germinal_22_509_1")
#a_dechiffrer = file_to_str("chiffres/chiffre_germinal_20_110_1")
texte, scoref, score_tab = recuit_simule(a_dechiffrer, 6000, dico_ngrams, 4, 0.6, 200, calculer_temperature_initiale(a_dechiffrer, dico_ngrams, 4))

str_to_file(texte, "resultat")"""