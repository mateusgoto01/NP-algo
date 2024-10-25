import sys, os, time
# pour lire un dictionnaire d'un fichier
import ast
# pour faire la statistique
import statistics, numpy
# pour verifier si une solution online traite toutes les tâches
import collections
# pour utiliser random, si besoin est
import random
import math

############ Student module ############

# ---------------------------------------------------------------------------- #
# --------------------- Constantes et variables globales --------------------- #
# ---------------------------------------------------------------------------- #

TRANSATION_CLOSED = -float('inf')
global m, M, longueur

# -------------------------------------------------------------- #
# --- Fonctions utilitaires - n'y touchez pas, les enfants ! --- #
# -------------------------------------------------------------- #

def verify_solution(taux_achat, trades_done, max_trade_bound):
# la dernière transation doit être fermée le dernier jour au plus tard, indiqué par le prix d'achar positif
    if taux_achat>0:
        raise ValueError("Il faut fermer (c.-a-d. vendre) la dernière transaction le dernier jour au plus tard")
    if trades_done > max_trade_bound:
        raise ValueError("Trop de transations effectués ; violation de la limite autorisée")

def mon_algo_est_deterministe():
    # par défaut l'algo est considéré comme déterministe
    # changez response = False dans le cas contraire
    response = True #False #True 
    return response 

# Utilisez OBLIGATOIREMENT cette fonction pour VENDRE !!!
def vente(taux, taux_achat, trades_done, sol_online):
    if taux_achat==TRANSATION_CLOSED:
        raise ValueError("Aucune transaction en cours, la vente est impossible")
    trades_done += 1
    sol_online = sol_online*(taux/taux_achat) 
    taux_achat = TRANSATION_CLOSED
    return sol_online, taux_achat, trades_done

# Utilisez OBLIGATOIREMENT cette fonction pour ACHETER !!!
def achat(taux, taux_achat, trades_done, max_trade_bound, sol_online):
    if taux_achat>0:
        raise ValueError("Aucun capital disponible, l'achat est impossible")
    if trades_done < max_trade_bound:  
        taux_achat = taux
    return taux_achat

##############################################################
# La fonction à completer pour la compétition
##############################################################
##############################################################
# Les variables m, M, longeur, max_trade_bound et la constante TRANSATION_CLOSED sont globales
##############################################################  

# le passage entre modules exige de passer m, M et longueur comme paramètres
def two_way_trading_online(m, M, longueur, sol_online, day, trades_done, max_trade_bound, taux_achat, taux):

    ###################################################################################
    # Complétez cette fonction : soit vous achetez (à condition que vous ayez du capital),
    # soit vous vendez (à condition que vous ayez des actions), soit vous ne faites rien.
    ###################################################################################
    # ATTENTION :
    # Pour l'achat et la vente, utilisez les fonctions achat et vente définies plus haut !!!
    # EXPLICATION :
    # Si vous achetez, la variable taux_achat devient positive, égale à la valeur de la variable taux (prix de l'action).
    # Si vous vendez, la variable taux_achat devient négative, égale à la valeur de la constante TRANSACTION_CLOSED.
    # La vente clôt la transaction, le nombre de trades effectués, trades_done, est incrémenté.
    # Les fonctions achat et vente tiennent compte de ces contraintes !
    # ###################################################################################
    M1_3 = M**(0.5 / 3)  # Threshold for buying
    M2_3 = M**(1.5 / 3)  # Threshold for selling
    stop_loss_threshold = 0.8 * taux_achat  # 20% loss limit
        
    # Define K and adjust strategy
    if trades_done <= max_trade_bound:
        if max_trade_bound == 1:
            # For k = 1: Monitor trend, aim for the highest selling point within the range
            if taux_achat == TRANSATION_CLOSED and taux == 1:
                taux_achat = achat(taux, taux_achat, trades_done, max_trade_bound, sol_online)
            elif taux_achat > 0 and taux >= 1.45*M2_3:
                sol_online, taux_achat, trades_done = vente(taux, taux_achat, trades_done, sol_online)

        elif max_trade_bound > 2 and longueur >= 1:
            # For larger k and long range: Buy and sell on small price increases, avoiding bad conditions
            if taux_achat == TRANSATION_CLOSED and (taux <= M1_3):
                taux_achat = achat(taux, taux_achat, trades_done, max_trade_bound, sol_online)
            elif taux_achat > 0 and taux >= taux_achat*1.3:
                sol_online, taux_achat, trades_done = vente(taux, taux_achat, trades_done, sol_online)
            elif taux_achat > 0 and day >= longueur * 0.75 and taux >= M2_3:
                sol_online, taux_achat, trades_done = vente(taux, taux_achat, trades_done, sol_online)

        else:
            # For small k and long range: Use the current strategy
            if taux_achat == TRANSATION_CLOSED and (taux <= M1_3):
                taux_achat = achat(taux, taux_achat, trades_done, max_trade_bound, sol_online)
            elif taux_achat > 0 and taux >= M2_3:
                sol_online, taux_achat, trades_done = vente(taux, taux_achat, trades_done, sol_online)

        if day == longueur - 1 and taux_achat != TRANSATION_CLOSED:
            sol_online, taux_achat, trades_done = vente(taux, taux_achat, trades_done, sol_online)
    return sol_online, taux_achat, trades_done

    


##############################################################
#### LISEZ LE README et NE PAS MODIFIER LE CODE SUIVANT ####
##############################################################
if __name__=="__main__":

    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])
    
    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
        print(input_dir, "doesn't exist")
        exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
        print(output_dir, "doesn't exist")
        exit()       
	
    # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))             
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    # le bloc de lancement dégagé à l'exterieur pour ne pas le répeter pour deterministe/random
    def launching_sequence(max_trade_bound):
        sol_online  = 1 # initialisation de la solution online, on commence ayant un euro
        day = 0 # initialisation du jour
        trades_done = 0 # initialisation du nombre de trades effectués   
        taux_achat = TRANSATION_CLOSED # négatif si rien acheté, positif si l'achat a été fait, il faut vendre
        for taux in sigma:
            # votre algoritme est lancé ici pour une journée day où le taux est taux
            # le passage entre modules exige de passer m, M et longueur comme paramètres
            sol_online, taux_achat, trades_done = two_way_trading_online(m, M, longueur, sol_online, day, trades_done, max_trade_bound, taux_achat, taux)
            if trades_done == max_trade_bound:
                break
            day += 1


        # À la fin de la séquence, vous devrez avoir vendu les actions achetées ;
        # attention à ne pas dépasser la limite de transactions autorisée 
        verify_solution(taux_achat, trades_done, max_trade_bound)
        return sol_online # retour nécessaire pour ingestion

    # Collecte des résultats
    scores = []
    
    for instance_filename in sorted(os.listdir(input_dir)):
        
        # C'est une partie pour inserer dans ingestion.py !!!!!
        # importer l'instance depuis le fichier (attention code non robuste)
        # le code repris de Safouan - refaire pour m'affanchir des numéros explicites
        print("instancia: ", instance_filename)
        instance_file = open(os.path.join(input_dir, instance_filename), "r")
        lines = instance_file.readlines()
        
        m = int(lines[1])
        M = int(lines[4])
        max_trade_bound = int(lines[7])
        longueur = int(lines[10])
        str_lu_sigma = lines[13]
        sigma = ast.literal_eval(str_lu_sigma)
        exact_solution = float(lines[16])

        # lancement conditionelle de votre algorithme
        # N.B. il est lancé par la fonction launching_sequence(max_trade_bound) 
        if mon_algo_est_deterministe():
            print("lancement d'un algo deterministe")  
            solution_online = launching_sequence(max_trade_bound) 
            solution_eleve = solution_online 
        else:
            print("lancement d'un algo randomisé")
            runs = 10
            sample = numpy.empty(runs)
            for r in range(runs):
                solution_online = launching_sequence(max_trade_bound)  
                sample[r] = solution_online
            solution_eleve = numpy.mean(sample)


        best_ratio = solution_eleve/float(exact_solution)
        scores.append(best_ratio)
        # ajout au rapport
        output_file.write(instance_filename + ': score: {}\n'.format(best_ratio))

    output_file.write("Résultat moyen des ratios:" + str(sum(scores)/len(scores)))

    output_file.close()
