import math
import string
import random

alphabet = list(string.ascii_uppercase)

def file_to_str(nom_fichier):
    """Transforme un fichier en une chaine de caractère"""
    with open(nom_fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()
    return contenu

def str_to_file(texte, nom_fichier):
    """Ecris une chaine de caractère dans un fichier"""
    with open(nom_fichier, 'w', encoding='utf-8') as f:
        f.write(texte)

def dico_permutation_alea():
    """Renvoie un dictionnaire avec des permutations générées aléatoirement"""
    lettres_disponibles = alphabet.copy()
    dico = dict()
    i = 0
    while lettres_disponibles:
        lettre = alphabet[i]
        c = random.choice(lettres_disponibles)
        lettres_disponibles.remove(c)
        dico[lettre] = c
        i += 1
    return dico

def dico_n_grammes(corpus, n):
    """Renvoie le dictionnaire contenant le nombre d'occurences des n-grammes"""
    dico = dict()
    for i in range(len(corpus)-n+1):
        mot = corpus[i:i+n]
        if mot in dico:
            dico[mot] += 1
        else:
            dico[mot] = 1
    return dico


def normaliser_dico(dico_ngrams):
    """ Transforme un dictionnaire d'occurences de n-grammes en un dictionnaire de probabilités. """
    total = sum(dico_ngrams.values())  # Somme totale des occurrences
    return {k: (v / total) for k, v in dico_ngrams.items()}  # Conversion en fréquence


def score(dico_ref, message, n_gramme):
    """Calcule le score d'un message en fonction des fréquences des n-grammes dans dico_ref."""
    score_total = 0
    dico_n = dico_n_grammes(message, n_gramme)

    for k, count in dico_n.items():
        val = dico_ref.get(k, 1e-5)  # Vérifie si la clé existe dans dico_freq, sinon prend 1e-5
        score_total += math.log(val) * count # Ajoute la contribution au score total

    return -score_total # On retourne le score négatif pour minimiser dans l'algorithme


def permutation_alea(dicoP):
    """Permute deux lettres aléatoirement de notre dictionnaire"""
    new_dicoP = dicoP.copy()
    r1, r2 = random.sample(alphabet, 2)
    new_dicoP[r1], new_dicoP[r2] = new_dicoP[r2], new_dicoP[r1]
    return new_dicoP


def dechiffrer(message, key):
    """Déchiffre le message selon le dictionnaire de permutation"""
    res = ""
    key_inverse = {value: clef for clef, value in key.items()}
    
    for char in message:
        if char in key_inverse:
            res += key_inverse[char]
        else:
            res += char

    return res


def hill_climbing(message, nbPermutations, dico_ref, n):
    """Applique l'algorithme du Hill Climbing pour décrypter le texte"""
    dico_perm = dico_permutation_alea()  # Génère une permutation aléatoire
    res = dechiffrer(message, dico_perm)
    scoreInit = score(dico_ref, res, n)  # Score initial avec les n-grammes
    meilleur_dico = dico_perm  # Initialisation de la meilleure clé
    meilleur_message = res  # Initialisation du meilleur dictionnaire (message déchiffré)
    meilleur_score = scoreInit  # Initialisation du meilleur score
    stagnation = 0
    max_stagnation = 5000

    for _ in range(nbPermutations):
        new_dico_perm = permutation_alea(dico_perm)  # Applique la permutation
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
        else:
            stagnation += 1
        if stagnation == max_stagnation:  # Réinitialisation après un certain nombre d'itérations
            print(f"Reinitialisation apres {stagnation} iterations")
            dico_perm = dico_permutation_alea()
            res = dechiffrer(message, dico_perm)
            scoreInit = score(dico_ref, res, n)
            stagnation = 0

    print(f"Meilleur score trouve : {meilleur_score}")
    return meilleur_message



n_gramme = 5
Texte_Ref = file_to_str("germinal_nettoye")
dico_ngrams = dico_n_grammes(Texte_Ref, n_gramme)
dico_ngrams = normaliser_dico(dico_ngrams)

message_chiffrer = file_to_str("chiffre_germinal_58_1150_2")
print(hill_climbing(message_chiffrer, 100000, dico_ngrams,n_gramme))

"""
dico_init = dico_permuatation_alea()
print(dico_init)
new_dico = permutation_alea(dico_init)
print(new_dico)
new_alphabet = dechiffrer(string.ascii_uppercase, new_dico)
print(new_alphabet)
"""
