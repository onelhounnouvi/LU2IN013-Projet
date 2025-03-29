from recuit_simule import *

corpus_ref = file_to_str("germinal_nettoye")
dico_ngrams = normaliser_dico(dico_n_grammes(corpus_ref, 4))

a_dechiffrer = file_to_str("chiffres/chiffre_germinal_52_1199_1")
texte = recuit_simule(a_dechiffrer, 10000, dico_ngrams, 4, 0.01)

str_to_file(texte, "resultat")