import numpy as np
from matplotlib import pyplot as plt
from hill_climbing import *
from recuit_simule import *
from substitution import *
from tabou import *

def ngram_similarite(dict1, dict2):
    all_ngrams = set(dict1.keys()) | set(dict2.keys())
    somme_min = 0
    somme_max = 0
    for gram in all_ngrams:
        freq1 = dict1.get(gram, 0)
        freq2 = dict2.get(gram, 0)
        somme_min += min(freq1, freq2)
        somme_max += max(freq1, freq2)
    return 1.0 if somme_max == 0 else somme_min / somme_max

def caractere_similarite(texte1, texte2):
    longueur = min(len(texte1), len(texte2))
    if longueur == 0:
        return 1.0
    nb_identiques = sum(1 for a, b in zip(texte1[:longueur], texte2[:longueur]) if a == b)
    return nb_identiques / longueur

def similarite_mixte(texte1, texte2, dict1, dict2, alpha=0.5):
    sim_c = caractere_similarite(texte1, texte2)
    sim_n = ngram_similarite(dict1, dict2)
    return alpha * sim_c + (1 - alpha) * sim_n

def evaluer_taux_reussite_recuit(message, texte_clair, nbPermutations, dico_ref, n, cool_ratio, cool_time, repetitions, seuil, alpha=0.4):
    succes = 0
    ref_ngrams = dico_n_grammes(texte_clair, n)
    for _ in range(repetitions):
        T_initial = calculer_temperature_initiale(message, dico_ref, n)
        texte_dechiffre, _, _ = recuit_simule(message, nbPermutations, dico_ref, n, cool_ratio, cool_time, T_initial)
        test_ngrams = dico_n_grammes(texte_dechiffre, n)
        ratio = similarite_mixte(texte_dechiffre, texte_clair, test_ngrams, ref_ngrams, alpha)
        if ratio >= seuil:
            succes += 1
    return (succes / repetitions) * 100

def evaluer_taux_reussite_hillClimbing(message, texte_clair, nbPermutations, dico_ref, n, max_stagnation, repetitions, seuil, alpha=0.4):
    succes = 0
    ref_ngrams = dico_n_grammes(texte_clair, n)
    for _ in range(repetitions):
        texte_dechiffre, _, _ = hill_climbing(message, nbPermutations, dico_ref, n, max_stagnation)
        test_ngrams = dico_n_grammes(texte_dechiffre, n)
        ratio = similarite_mixte(texte_dechiffre, texte_clair, test_ngrams, ref_ngrams, alpha)
        if ratio >= seuil:
            succes += 1
    return (succes / repetitions) * 100

def evaluer_taux_reussite_hillClimbing_opti(message, texte_clair, nbPermutations, dico_ref, n, max_stagnation, repetitions, seuil, alpha=0.4):
    succes = 0
    ref_ngrams = dico_n_grammes(texte_clair, n)
    for _ in range(repetitions):
        texte_dechiffre, _, _ = hill_climbing_optimise(message, nbPermutations, dico_ref, n, max_stagnation)
        test_ngrams = dico_n_grammes(texte_dechiffre, n)
        ratio = similarite_mixte(texte_dechiffre, texte_clair, test_ngrams, ref_ngrams, alpha)
        if ratio >= seuil:
            succes += 1
    return (succes / repetitions) * 100

def evaluer_taux_reussite_tabou(message, texte_clair, nb_iter, dico_ref, n, repetitions, tabu_size, seuil, alpha=0.4):
    succes = 0
    ref_ngrams = dico_n_grammes(texte_clair, n)
    for _ in range(repetitions):
        texte_dechiffre, _, _ = recherche_tabou(message, nb_iter, dico_ref, n, tabu_size)
        test_ngrams = dico_n_grammes(texte_dechiffre, n)
        ratio = similarite_mixte(texte_dechiffre, texte_clair, test_ngrams, ref_ngrams, alpha)
        if ratio >= seuil:
            succes += 1
    return (succes / repetitions) * 100

# Chargement des textes
textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    205: file_to_str("chiffres/chiffre_germinal_5_205_1"),
    318: file_to_str("chiffres/chiffre_germinal_3_318_1"),
    509: file_to_str("chiffres/chiffre_germinal_22_509_1")
}

textes_clairs = {
    110: "ETTOUTLETEMPSQUELESVISITEURSRESTERENTENFACEELLESENDEGOISERENTLESVOILAQUISORTENTDITENFINLALEVAQUEILSFONTLETOUR",
    205: "ETMAHEUSEDESESPERAITENCOREDELAMALCHANCEVOILAQUILPERDAITUNEDESESHERSCHEUSESSANSPOUVOIRLAREMPLACERIMMEDIATEMENTILTRAVAILLAITAUMARCHANDAGEILSETAIENTQUATREHAVEURSASSOCIESDANSSATAILLELUIBACHARIELEVAQUEETCHAVAL ",
    318: "ALZIRELESYEUXGRANDSOUVERTSREGARDAITTOUJOURSLESDEUXMIOCHESLENOREETHENRIAUXBRASLUNDELAUTRENAVAIENTPASREMUERESPIRANTDUMEMEPETITSOUFFLEMALGRELEVACARMECATHERINEDONNEMOILACHANDELLECRIAMAHEUELLEFINISSAITDEBOUTONNERSAVESTEELLEPORTALACHANDELLEDANSLECABINETLAISSANTSESFRERESCHERCHERLEURSVETEMENTSAUPEUDECLARTEQUIVENAITDELAPORTE",
    509: "ELLESENFACHAITMAISNESENALLAITPASCHATOUILLEEAUFONDPARLESGROSMOTSQUILAFAISAIENTCRIERLESMAINSAUVENTREILARRIVAASONSECOURSUNEFEMMEMAIGREDONTLACOLEREBEGAYANTERESSEMBLAITAUNGLOUSSEMENTDEPOULEDAUTRESAULOINSURLESPORTESSEFFAROUCHAIENTDECONFIANCEMAINTENANTLECOLEETAITFERMEETOUTELAMARMAILLETRAINAITCETAITUNGROUILLEMENTDEPETITSETRESPIAULANTSEROULANTSEBATTANTTANDISQUELESPERESQUINETAIENTPASALESTAMINETRESTAIENTPARGROUPESDETROISOUQUATREACCROUPISSURLEURSTALONSCOMMEAUFONDDELAMINEFUMANTDESPIPESAVECDESPAROLESRARESALABRIDUNMUR"
}

# Paramètres d'évaluation
repetitions = 500
nbPerm = 8000
corpus_ref = file_to_str("germinal_nettoye")
n_gramme = 3
dico_ngrams = normaliser_dico(dico_n_grammes(corpus_ref, n_gramme))
cool_ratio = 0.3
cool_time = 1000
max_stagnations_opti = 300
max_stagnations_classique = 400
tabu_size = 460
nb_iter = 370

alpha_mixte = 0.6
seuil_mixte = 0.9

# Initialisation des listes de résultats
rates_recuit_mixte = []
rates_hill_mixte = []
rates_hill_opti_mixte = []
rates_tabou_mixte = []

# Traitement pour chaque longueur
for i, l in enumerate(sorted(textes_chiffres.keys())):
    message_chiffre = textes_chiffres[l]
    texte_clair = textes_clairs[l]

    taux_recuit = evaluer_taux_reussite_recuit(
        message_chiffre, texte_clair, nbPerm, dico_ngrams, n_gramme,
        cool_ratio, cool_time, repetitions, seuil_mixte, alpha=alpha_mixte
    )

    taux_hill = evaluer_taux_reussite_hillClimbing(
        message_chiffre, texte_clair, nbPerm, dico_ngrams, n_gramme,
        max_stagnations_classique, repetitions, seuil_mixte, alpha=alpha_mixte
    )

    taux_hill_opti = evaluer_taux_reussite_hillClimbing_opti(
        message_chiffre, texte_clair, nbPerm, dico_ngrams, n_gramme,
        max_stagnations_opti, repetitions, seuil_mixte, alpha=alpha_mixte
    )

    taux_tabou = evaluer_taux_reussite_tabou(
        message_chiffre, texte_clair, nb_iter, dico_ngrams, n_gramme,
        repetitions, tabu_size, seuil_mixte, alpha=alpha_mixte
    )

    # Stockage des résultats
    rates_recuit_mixte.append(taux_recuit)
    rates_hill_mixte.append(taux_hill)
    rates_hill_opti_mixte.append(taux_hill_opti)
    rates_tabou_mixte.append(taux_tabou)

    if i == 0: 
        seuil_mixte = 0.97

# --- Affichage graphique ---
x = np.arange(len(textes_chiffres))
width = 0.15

plt.figure(figsize=(12, 6))
plt.bar(x - 1.5 * width, rates_hill_mixte, width, label="Hill Climbing")
plt.bar(x - 0.5 * width, rates_hill_opti_mixte, width, label="Hill Climbing optimisé")
plt.bar(x + 0.5 * width, rates_recuit_mixte, width, label="Recuit simulé")
plt.bar(x + 1.5 * width, rates_tabou_mixte, width, label="Recherche Tabou")
plt.xticks(x, sorted(textes_chiffres.keys()))
plt.xlabel("Longueur du texte chiffré")
plt.ylabel("Taux de réussite (%)")
plt.title(f"Taux de réussite (similarité mixte α={alpha_mixte}, n-gramme = {n_gramme})")
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(f"taux_reussite_mixte_ngramme_{n_gramme}.png")
plt.close()
