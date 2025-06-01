import numpy as np
from matplotlib import pyplot as plt
from hill_climbing import hill_climbing_ameliore
from recuit_simule import recuit_simule, calculer_temperature_initiale
from substitution import dico_n_grammes, file_to_str, normaliser_dico


def ngram_similarite(dict1, dict2):
    """Calcule la similarité entre deux textes à partir de leurs dictionnaires de n-grammes.
    Utilise la somme des minima sur la somme des maxima (indice Jaccard)"""

    # Ensemble de tous les n-grammes présents dans au moins l'un des deux dictionnaires
    all_ngrams = set(dict1.keys()) | set(dict2.keys())
    somme_min = 0
    somme_max = 0

    for gram in all_ngrams:
        freq1 = dict1.get(gram, 0)
        freq2 = dict2.get(gram, 0)
        somme_min += min(freq1, freq2)
        somme_max += max(freq1, freq2)

    if somme_max == 0:
        return 1.0  #Si les deux textes sont vides, on définit la similarité à 1.

    return somme_min / somme_max


def evaluer_taux_reussite_recuit(message, texte_clair, nbPermutations, dico_ref, n, cool_ratio, cool_time, repetitions, seuil):
    """Retourne le taux de réussite (en %) du recuit simulé en comparant le texte déchiffré au texte clair"""
    succes = 0
    dico_text_ref = dico_n_grammes(texte_clair, n)
    for rep in range(repetitions):
        T_initial = calculer_temperature_initiale(message, dico_ref, n)
        texte_dechiffre, _ , _ = recuit_simule(message, nbPermutations, dico_ref, n, cool_ratio, cool_time, T_initial)

        # Calculer le ratio de similarité entre le texte déchiffré et le texte clair
        dico_text = dico_n_grammes(texte_dechiffre, n)
        ratio = ngram_similarite(dico_text, dico_text_ref)
        if ratio >= seuil:
            succes += 1
    return (succes / repetitions) * 100

def evaluer_taux_reussite_hillClimbing(message, texte_clair, nbPermutations, dico_ref, n, max_stagnation, repetitions, seuil):
    """Retourne le taux de réussite (en %) du hill Climbing en comparant le texte déchiffré au texte clair"""
    succes = 0
    dico_text_ref = dico_n_grammes(texte_clair, n)
    for rep in range(repetitions):
        texte_dechiffre, _, _ = hill_climbing_ameliore(message, nbPermutations, dico_ref, n, max_stagnation)

        # Calculer le ratio de similarité entre le texte déchiffré et le texte clair
        dico_text = dico_n_grammes(texte_dechiffre, n)
        ratio = ngram_similarite(dico_text, dico_text_ref)
        if ratio >= seuil:
            succes += 1
    return (succes / repetitions) * 100

textes_chiffres = {
    110: file_to_str("chiffres/chiffre_germinal_20_110_1"),
    201: file_to_str("chiffres/chiffre_germinal_6_201_1"),
    401: file_to_str("chiffres/chiffre_germinal_1_401_1"),
    509: file_to_str("chiffres/chiffre_germinal_22_509_1"),
    707: file_to_str("chiffres/chiffre_germinal_10_707_3"),
    1150: file_to_str("chiffres/chiffre_germinal_58_1150_2")
}

textes_clairs = {
    110: "ETTOUTLETEMPSQUELESVISITEURSRESTERENTENFACEELLESENDEGOISERENTLESVOILAQUISORTENTDITENFINLALEVAQUEILSFONTLETOUR",
    201: "SURLESDALLESDEFONTELESCHARGEURSROULAIENTVIOLEMMENTDESBERLINESPLEINESUNEODEURDECAVESUINTAITDESMURSUNEFRAICHEURSALPETREEOUPASSAIENTDESSOUFFLESCHAUDSVENUSDELECURIEVOISINEQUATREGALERIESSOUVRAIENTLABEANTES",
    401: "CEUXCIDESBATTERIESDECENTCHEMINEESPLANTEESOBLIQUEMENTALIGNAIENTDESRAMPESDEFLAMMESROUGESTANDISQUELESDEUXTOURSPLUSAGAUCHEBRULAIENTTOUTESBLEUESENPLEINCIELCOMMEDESTORCHESGEANTESCETAITDUNETRISTESSEDINCENDIEILNYAVAITDAUTRESLEVERSDASTRESALHORIZONMENACANTQUECESFEUXNOCTURNESDESPAYSDELAHOUILLEETDUFERVOUSETESPEUTETREDELABELGIQUEREPRITDERRIEREETIENNELECHARRETIERQUIETAITREVENUCETTEFOISILNAMENAITQUETROISBERLINES",
    509: "ELLESENFACHAITMAISNESENALLAITPASCHATOUILLEEAUFONDPARLESGROSMOTSQUILAFAISAIENTCRIERLESMAINSAUVENTREILARRIVAASONSECOURSUNEFEMMEMAIGREDONTLACOLEREBEGAYANTERESSEMBLAITAUNGLOUSSEMENTDEPOULEDAUTRESAULOINSURLESPORTESSEFFAROUCHAIENTDECONFIANCEMAINTENANTLECOLEETAITFERMEETOUTELAMARMAILLETRAINAITCETAITUNGROUILLEMENTDEPETITSETRESPIAULANTSEROULANTSEBATTANTTANDISQUELESPERESQUINETAIENTPASALESTAMINETRESTAIENTPARGROUPESDETROISOUQUATREACCROUPISSURLEURSTALONSCOMMEAUFONDDELAMINEFUMANTDESPIPESAVECDESPAROLESRARESALABRIDUNMUR",
    707: "UNEHEUREETDEMIEAHUNEPROPREJOURNEENOUSNAURONSPASCINQUANTESOUSJEMENVAISCAMEDEGOUTEBIENQUILYEUTENCOREUNEDEMIHEUREDETRAVAILILSERHABILLALESAUTRESLIMITERENTLAVUESEULEDELATAILLELESJETAITHORSDEUXCOMMELAHERSCHEUSESETAITREMISEAUROULAGEILSLAPPELERENTENSIRRITANTDESONZELESILECHARBONAVAITDESPIEDSILSORTIRAITTOUTSEULETLESSIXLEURSOUTILSSOUSLEBRASPARTIRENTAYANTAREFAIRELESDEUXKILOMETRESRETOURNANTAUPUITSPARLAROUTEDUMATINDANSLACHEMINEECATHERINEETETIENNESATTARDERENTTANDISQUELESHAVEURSGLISSAIENTJUSQUENBASCETAITUNERENCONTRELAPETITELYDIEARRETEEAUMILIEUDUNEVOIEPOURLESLAISSERPASSERETQUILEURRACONTAITUNEDISPARITIONDELAMOUQUETTEPRISEDUNTELSAIGNEMENTDENEZQUEDEPUISUNEHEUREELLEETAITALLEESETREMPERLAFIGUREQUELQUEPARTONNESAVAITPASOU",
    1150: "DEPUISCINQJOURSQUILSTRAVAILLAIENTLAELLESONGEAITAUXCONTESDONTONAVAITBERCESONENFANCEACESHERSCHEUSESDUTEMPSJADISQUIBRULAIENTSOUSLETARTARETENPUNITIONDECHOSESQUONNOSAITPASREPETERSANSDOUTEELLEETAITTROPGRANDEMAINTENANTPOURCROIREDEPAREILLESBETISESMAISPOURTANTQUAURAITELLEFAITSIBRUSQUEMENTELLEAVAITVUSORTIRDUMURUNEFILLEROUGECOMMEUNPOELEAVECDESYEUXPAREILSADESTISONSCETTEIDEEREDOUBLAITSESSUEURSAURELAISAQUATREVINGTSMETRESDELATAILLEUNEAUTREHERSCHEUSEPRENAITLABERLINEETLAROULAITAQUATREVINGTSMETRESPLUSLOINJUSQUAUPIEDDUPLANINCLINEPOURQUELERECEVEURLEXPEDIATAVECCELLESQUIDESCENDAIENTDESVOIESDENHAUTFICHTRETUTEMETSATONAISEDITCETTEFEMMEUNEMAIGREVEUVEDETRENTEANSQUANDELLEAPERCUTCATHERINEENCHEMISEMOIJENEPEUXPASLESGALIBOTSDUPLANMEMBETENTAVECLEURSSALETESAHBIENREPLIQUALAJEUNEFILLEJEMENMOQUEDESHOMMESJESOUFFRETROPELLEREPARTITPOUSSANTUNEBERLINEVIDELEPISETAITQUEDANSCETTEVOIEDEFONDUNEAUTRECAUSESEJOIGNAITAUVOISINAGEDUTARTARETPOURRENDRELACHALEURINSOUTENABLEONCOTOYAITDANCIENSTRAVAUXUNEGALERIEABANDONNEEDEGASTONMARIETRESPROFONDEOUUNCOUPDEGRISOUDIXANSPLUSTOTAVAITINCENDIELAVEINEQUIBRULAITTOUJOURSDERRIERELECORROILEMURDARGILEBATILAETREPARECONTINUELLEMENTAFINDELIMITERLEDESASTRE",
    }

repetitions = 150
seuil = 0.9  #On considère que l'exécution est réussie si la similarité est >= 90%
nbPerm = 6000
corpus_ref = file_to_str("germinal_nettoye")
n = 4
dico_ngrams = normaliser_dico(dico_n_grammes(corpus_ref, n))
cool_ratio = 0.6
cool_time = 200
max_stagnations = 150

lengths = sorted(textes_chiffres.keys())
rates_recuit = []
rates_hill = []

for l in lengths:
    message_chiffre = textes_chiffres[l]
    texte_clair = textes_clairs[l]

    # Évaluer pour le recuit simulé
    rate_recuit = evaluer_taux_reussite_recuit(message_chiffre, texte_clair, nbPerm, dico_ngrams, n, cool_ratio,
            cool_time, repetitions, seuil
    )
    # Évaluer pour le hill climbing
    rate_hill = evaluer_taux_reussite_hillClimbing(
        message_chiffre, texte_clair, nbPerm, dico_ngrams, n, max_stagnations, repetitions, seuil)

    rates_recuit.append(rate_recuit)
    rates_hill.append(rate_hill)

#Affichage sous forme d'histogramme

x = np.arange(len(lengths))
width = 0.35

plt.figure(figsize=(10, 6))
rects1 = plt.bar(x - width / 2, rates_recuit, width, label='Recuit Simulé')
rects2 = plt.bar(x + width / 2, rates_hill, width, label='Hill Climbing')

plt.xlabel("Longueur du texte")
plt.ylabel("Taux de réussite (%)")
plt.title("Taux de réussite en fonction de la longueur du texte")
plt.xticks(x, [str(l) for l in lengths])
plt.legend()


#Ajouter les pourcentages sur chaque barre
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.annotate(f'{height:.1f}%',
                     xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 3),  # Décalage vertical de 3 points
                     textcoords="offset points",
                     ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plt.show()
plt.savefig("reussite")