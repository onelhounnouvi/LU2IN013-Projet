**Résumé**  
Implémentation et comparaison de metaheuristiques pour la cryptanalyse de chiffrements par substitution monoalphabétique. Pour les détails méthodologiques et les résultats expérimentaux, lire `rapport.pdf`.

---

## Organisation du dépôt
- `substitution.py` : fonctions utilitaires de base (génération, gestion de clés,...) 
- `hill_climbing.py` : implémentation du hill climbing (avec variantes optimisées).  
- `recuit_simule.py` : implémentation du recuit simulé (avec cooling, température initiale, etc.).  
- `tabou.py` : recherche tabou.  
- `Visualisation/Utilitaires/graph_*.py` : scripts pour tracer et sauvegarder les courbes et figures du rapport.  
- `Visualisation/Utilitaires/chiffres.tgz` : archive contenant les fichiers chiffrés de test (voir commande ci-dessous).  
- `Visualisation/germinal_nettoye` : corpus de référence utilisé pour construire les n-grammes.  
- `rapport.pdf` : documentation complète du projet (méthodes, réglages expérimentaux, résultats) — **lire d’abord**.

---

## Instructions 
- Cloner le dépôt
- Extraire le fichier `chiffres.gz` dans un dossier chiffres de sorte que tous les fichiers chiffrés soient accessibles sous `Visualisation/Utilitaires/chiffres/`