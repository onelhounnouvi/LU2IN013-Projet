import math
import string
import random

alphabet = list(string.ascii_uppercase)

def file_to_str(nom_fichier):
    """Transforme un fichier en une chaine de caractères"""
    with open(nom_fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()
    return contenu

def str_to_file(texte, nom_fichier):
    """Ecris une chaine de caractères dans un fichier"""
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
    for i in range(len(corpus) - n + 1):
        mot = corpus[i:i + n]
        if mot in dico:
            dico[mot] += 1
        else:
            dico[mot] = 1
    return dico

def normaliser_dico(dico_ngrams):
    """Transforme un dictionnaire d'occurrences de n-grammes en un dictionnaire de probabilités. """
    total = sum(dico_ngrams.values())  # Somme totale des occurrences
    return {k: (v / total) for k, v in dico_ngrams.items()}  # Conversion en fréquence

def score(dico_ref, message, n):
    """Calcule le score d'un message basé sur les n-grammes en utilisant sur la log-vraisemblance"""
    dicoM = dico_n_grammes(message, n)  #Extraction des n-grammes du message
    res = 0.0
    for k in dicoM:
        val = dico_ref.get(k, 1e-5) #Fréquence du n-gramme dans le dico de référence normalisé si présent, 1e-5 sinon
        res += math.log(val) #Log
    return -res  #On retourne l'opposé de la somme pour minimiser

def score2(dico_ref, message, n):
    """Calcule le score d'un message basé sur les n-grammes en utilisant sur la formule suivante
                         1
                   -------------
                    1 + |f - r|
    f : fréquence d'un n-gramme dans le message crypté et r : celle dans le dictionnaire de référence
    """
    dicoM = normaliser_dico(dico_n_grammes(message, n))  #Extraction des n-grammes du message sous forme normalisée
    res = 0.0
    for k, val in dicoM.items():
        val_ref = dico_ref.get(k, 1e-5) #Fréquence dans le dico de référence normalisé si présent, 1e-5 sinon
        res += float(1/(1 + math.fabs(val_ref - val)))
    return res

def modifier_cle(dicoP):
    """Modifie légèrement le dico en faisant une permutation aléatoire de deux lettres"""
    new_dicoP = dicoP.copy()
    r1, r2 = random.sample(alphabet, 2)
    new_dicoP[r1], new_dicoP[r2] = new_dicoP[r2], new_dicoP[r1]
    return new_dicoP

def modifier_cle_et_mouvement(dicoP):
    """Fait une permutation aléatoire et retourne aussi le mouvement effectué."""
    new_dicoP = dicoP.copy()
    r1, r2 = random.sample(alphabet, 2)
    new_dicoP[r1], new_dicoP[r2] = new_dicoP[r2], new_dicoP[r1]
    return new_dicoP, (r1, r2)


def dechiffrer(message, key):
    """Déchiffre le message selon le dictionnaire de permutation"""
    res = ""
    key_inverse = {value: clef for clef, value in key.items()}
    for lettre in message:
        if lettre in key_inverse:
            res += key_inverse[lettre]
        else:
            res += lettre  #On garde les caractères non chiffrés (espaces, ponctuation, etc.)
    return res