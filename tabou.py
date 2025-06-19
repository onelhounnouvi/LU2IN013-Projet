from collections import deque
from substitution import *

def recherche_tabou(message, nb_iter, dico_ref, n, tabu_size=100):
    """Applique la recherche tabou pour décrypter un message chiffré et retourne l'historique des scores."""

    dico_courant = dico_permutation_alea()
    message_courant = dechiffrer(message, dico_courant)
    score_courant = score(dico_ref, message_courant, n)

    meilleur_dico = dico_courant
    meilleur_message = message_courant
    meilleur_score = score_courant

    liste_tabou = deque(maxlen=tabu_size)
    score_history = [score_courant]  # Ajout du score initial

    for _ in range(nb_iter):
        voisins = []
        for _ in range(100):  # Taille de l’échantillon
            voisin, mouvement = modifier_cle_et_mouvement(dico_courant)
            texte_voisin = dechiffrer(message, voisin)
            score_voisin = score(dico_ref, texte_voisin, n)
            voisins.append((score_voisin, voisin, texte_voisin, mouvement))

        voisins.sort(key=lambda x: x[0])  # tri croissant

        for score_voisin, voisin, texte_voisin, mouvement in voisins:
            mouvement_canonique = tuple(sorted(mouvement))
            if mouvement_canonique not in liste_tabou or score_voisin < meilleur_score:
                dico_courant = voisin
                message_courant = texte_voisin
                score_courant = score_voisin
                liste_tabou.append(mouvement_canonique)
                break


        if score_courant < meilleur_score:
            meilleur_dico = dico_courant
            meilleur_message = message_courant
            meilleur_score = score_courant

        score_history.append(score_courant)
        
    print(f"Meilleur score trouve : {meilleur_score}")
    return meilleur_message, meilleur_score, score_history


corpus_ref = file_to_str("germinal_nettoye")
dico_ngrams = normaliser_dico(dico_n_grammes(corpus_ref, 2))

textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    205: file_to_str("chiffres/chiffre_germinal_5_205_1"),
    318: file_to_str("chiffres/chiffre_germinal_3_318_1"),
    509: file_to_str("chiffres/chiffre_germinal_22_509_1")
}
for texte in textes_chiffres.values():
    message,_ , _ = recherche_tabou(texte, 100, dico_ngrams, 2,1000000)
    print(message)
    
    #Bonne valeur : taille tabou = 220, nb_iter = 310
    #taille_tabou = 370, nb_tier = 460
