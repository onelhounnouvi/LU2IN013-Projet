import time
import numpy as np
from matplotlib import pyplot as plt
from hill_climbing import *
from recuit_simule import *
from substitution import *
from tabou import *

def mesurer_temps_moyen_recuit(message, nbPermutations, dico_ref, n, cool_ratio, cool_time, repetitions):
    total_time = 0
    for _ in range(repetitions):
        debut = time.time()
        T_initial = calculer_temperature_initiale(message, dico_ref, n)
        recuit_simule(message, nbPermutations, dico_ref, n, cool_ratio, cool_time, T_initial)
        fin = time.time()
        total_time += (fin - debut)
    return total_time / repetitions

def mesurer_temps_moyen_hillClimbing(message, nbPermutations, dico_ref, n, max_stagnation, repetitions):
    total_time = 0
    for _ in range(repetitions):
        debut = time.time()
        hill_climbing(message, nbPermutations, dico_ref, n, max_stagnation)
        fin = time.time()
        total_time += (fin - debut)
    return total_time / repetitions

def mesurer_temps_moyen_hillClimbing_opti(message, nbPermutations, dico_ref, n, max_stagnation, repetitions):
    total_time = 0
    for _ in range(repetitions):
        debut = time.time()
        hill_climbing_optimise(message, nbPermutations, dico_ref, n, max_stagnation)
        fin = time.time()
        total_time += (fin - debut)
    return total_time / repetitions

def mesurer_temps_moyen_tabou(message, nb_iter, dico_ref, n, tabu_size, repetitions):
    total_time = 0
    for _ in range(repetitions):
        debut = time.time()
        recherche_tabou(message, nb_iter, dico_ref, n, tabu_size)
        fin = time.time()
        total_time += (fin - debut)
    return total_time / repetitions

# Paramètres pour le calcul des temps (on met moins de répétitions pour que ce soit rapide)

textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    205: file_to_str("chiffres/chiffre_germinal_5_205_1"),
    318: file_to_str("chiffres/chiffre_germinal_3_318_1"),
    509: file_to_str("chiffres/chiffre_germinal_22_509_1")
}

repetitions_temps = 10
nbPerm = 8000
n_gramme = 3
cool_ratio = 0.3
cool_time = 1000
max_stagnations_opti = 300
max_stagnations_classique = 400
tabu_size = 220
nb_iter = 310
corpus_ref = file_to_str("germinal_nettoye")
dico_ngrams = normaliser_dico(dico_n_grammes(corpus_ref, n_gramme))

# Listes pour stocker les temps moyens par longueur
temps_recuit_moyen = []
temps_hill_moyen = []
temps_hill_opti_moyen = []
temps_tabou_moyen = []

# Pour chaque texte chiffré, on mesure les temps moyens
for l in sorted(textes_chiffres.keys()):
    message_chiffre = textes_chiffres[l]

    t_recuit = mesurer_temps_moyen_recuit(
        message_chiffre, nbPerm, dico_ngrams, n_gramme,
        cool_ratio, cool_time, repetitions_temps
    )
    t_hill = mesurer_temps_moyen_hillClimbing(
        message_chiffre, nbPerm, dico_ngrams, n_gramme,
        max_stagnations_classique, repetitions_temps
    )
    t_hill_opti = mesurer_temps_moyen_hillClimbing_opti(
        message_chiffre, nbPerm, dico_ngrams, n_gramme,
        max_stagnations_opti, repetitions_temps
    )
    t_tabou = mesurer_temps_moyen_tabou(
        message_chiffre, nb_iter, dico_ngrams, n_gramme,
        tabu_size, repetitions_temps
    )

    temps_recuit_moyen.append(t_recuit)
    temps_hill_moyen.append(t_hill)
    temps_hill_opti_moyen.append(t_hill_opti)
    temps_tabou_moyen.append(t_tabou)

# --- Tracé graphique ---

x = np.arange(len(textes_chiffres))
width = 0.15

plt.figure(figsize=(12, 6))
plt.bar(x - 1.5 * width, temps_hill_moyen, width, label="Hill Climbing")
plt.bar(x - 0.5 * width, temps_hill_opti_moyen, width, label="Hill Climbing optimisé")
plt.bar(x + 0.5 * width, temps_recuit_moyen, width, label="Recuit simulé")
plt.bar(x + 1.5 * width, temps_tabou_moyen, width, label="Recherche Tabou")
plt.xticks(x, sorted(textes_chiffres.keys()))
plt.xlabel("Longueur du texte chiffré")
plt.ylabel("Temps moyen d'exécution (secondes)")
plt.title(f"Temps moyen d'exécution des métaheuristiques par longueur de texte(n-gramme = {n_gramme})")
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("temps_moyen_execution_metas.png")
plt.show()
