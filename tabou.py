from collections import deque
from substitution import *

def recherche_tabou(message, nb_iter, dico_ref, n):
    """Applique la recherche tabou pour décrypter un message chiffré et retourne l'historique des scores."""

    dico_courant = dico_permutation_alea()
    message_courant = dechiffrer(message, dico_courant)
    score_courant = score(dico_ref, message_courant, n)

    meilleur_dico = dico_courant
    meilleur_message = message_courant
    meilleur_score = score_courant

    liste_tabou = deque(maxlen=1000000)
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
            mouvement_inv = (mouvement[1], mouvement[0])
            if (mouvement not in liste_tabou and mouvement_inv not in liste_tabou) or score_voisin < meilleur_score:
                dico_courant = voisin
                message_courant = texte_voisin
                score_courant = score_voisin
                liste_tabou.append(mouvement)
                break

        if score_courant < meilleur_score:
            meilleur_dico = dico_courant
            meilleur_message = message_courant
            meilleur_score = score_courant

        score_history.append(score_courant)
        
    #print(f"Meilleur score trouve : {score_courant}")
    return meilleur_message, meilleur_score, score_history, meilleur_dico