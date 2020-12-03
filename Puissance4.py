from math import inf as infinity
import random as rd
import time

#on defini les valeur des joueurs
IA = 1
Adversaire = 2

#affiche le Puissance_4 en remplacant les couleurs par des signes
#Valeur d'entrée: Puissance_4 = matrice remplie
def Affichage(Puissance_4): #ok#
    for i in range(len(Puissance_4)):
        for j in range(len(Puissance_4[i])):
            if Puissance_4[i][j] == 1:
                print("O", '|',end=' ') 
            elif Puissance_4[i][j] == 2:
                print("X", '|',end=' ') 
            else:
                print(" ", '|',end=' ') 
        print("")
        
    #Affichage numéro de la colonne    
    for j in range(len(Puissance_4[i])):
        if (j+1<9):
            print(j+1, ':',end=' ')
        else:
            print(j+1, ':',end='')
            
    print("")
    print("")

#Creation du Puissance_4 "vide" => rempli de 0
#Variable de sortie: tab = la matrice crée, remplie de 0
def CreationPuissance_4(): 
    tab = []
    nbColonne = 12
    nbLigne = 6
    for i in range(int(nbLigne)):
        tab2 =[]
        for j in range(int(nbColonne)):
            tab2.append(0)
        tab.append(tab2) 
    return tab

#Ensemble de cases possibles 
#Valeur d'entrée: matrice = matrice de jeu remplie
#Variable de sortie: possibilites = liste de tableau qui regroupe toute les cases qui peuvente etre jouées
def Possibilites(matrice): #ok#
    possibilites = []
    for colonne in range(len(matrice[0])) :
        for ligne in range(len(matrice)-1,-1,-1):
            if (matrice[ligne][colonne] == 0):
                possibilites.append([ligne,colonne])
                break
 
    return possibilites

#Ensemble de cases possibles dans un perimetre REDUIT ! (ici fixé à 11)
#Valeurs d'entrée: matrice = matrice de jeu remplie
#                  dernierCoup = colonne dans laquelle le joueur précédent a mis son piont
#Variable de sortie: possibilitesReduite = liste de tableau qui regroupe toute les cases qui peuvente etre jouées dans un périmetre reduit
def PossibilitesReduite(matrice, dernierCoup):
    possibilites = Possibilites(matrice)
    possibilitesReduites = []
    
    #En fonction de si on joue au milieu ou pas on prend plus ou moins de case autour
    if dernierCoup>3 and dernierCoup<8 :         #colonne de 4 à 7 parmi entre 0 et 11
        # nombre impaire ici : colonne prise en compte : celle du dernier joueur et les (casesAutour-1)/2 à droite/gauche
        casesAutour = 9  # en profondeur 5 : environ 9,3 seconde à jouer quand regarde 9 cases (sans les prints)
    elif dernierCoup>1 and dernierCoup<10 :      #colonne 2,3 et 8,9
        casesAutour = 11 
    else:                                        #colonne 0,1 et 10,11
        casesAutour = 15 # regarde que les 7 de droite ou gauche car sur coté               
        
    
    caseMin = dernierCoup - (casesAutour-1)/2
    caseMax = dernierCoup + (casesAutour-1)/2
    #Quand l'adversaire à joué au milieu : regarde presque tout le plateau
    #Quand l'adversaire a jouer en 0, regarde de 0 à 6 seulement
    #fonctionne assez bien pour pronfondeur = 4. mettre 9 ou 7 ou 5 si profondeur = 5 
    for case in possibilites:
        if case[1] >= caseMin and case[1] <= caseMax:
            possibilitesReduites.append(case)
    
    return possibilitesReduites


#Nombre de cases vides
#Valeurs d'entrée: matrice = matrice de jeu remplie
#Valeur de sortie = nombre de cases de la matrice vide
def CasesVides(matrice): 
    casesvides = []
    for colonne in range(len(matrice[0])):
        for ligne in range(len(matrice)):
            if (matrice[ligne][colonne] == 0):
                casesvides.append([ligne,colonne])
                
    return len(casesvides)


#MINMAX :
#Valeurs d'entrée: matrice = matrice de jeu remplie
                 # profondeur => nombre de coup que l'IA prévoit. Constante initialisé dans tour IA : à tester avec 4 ou 5 
                 # joueur = IA (toujours)
                 # RepColonne : L'endroit ou à jouer le dernier joueur
#Valeur de sortie: meuilleur : [ligne,colonne,scoreMinmax] : endroit ou il va jouer
def MinMax (matrice, profondeur, joueur, RepColonne): # pour profondeur = 4 ou 5 presque OK
    
    #Initialisation meilleur à - inf car on veut le score le plus grand possible.
    #ligne et colonne à -1 car non derteminé
    meilleur = [-1, -1, -infinity] 
    #Meilleur score opti aussi, de la meme manière 
    meilleurScoreOpti  = [-1, -1, -infinity] 

    # Compte le nombre de tour de la boucle for si le meuilleur score ne change pas = chaque position selon minmax on le meme score
    compteur = 0
    
    #On veut savoir le meuilleur coup à jouer.
    #On va parcourir toutes les case ou l'on peut jouer (ici case réduite pour gagner du temps de calcul)
    #Pour chaque case on va chercher à attricbuer un score pour ce coup joué
    CasesPossibilitesReduite=PossibilitesReduite(matrice, RepColonne) #Initialisation pour le pas avoir à calculer à chaque for
    
    for case in CasesPossibilitesReduite:
        #Parcours des (9 ou 11) cases ou il peut jouer
        
        #Initialisation : x=ligne, y=colonne => prenne les valeures (à chaque tour de for) de la cases étudiés
        x, y = case[0], case[1]     # x=ligne, y=colonne => prenne les valeures (à chaque tour de for) de la cases étudié
        matrice[x][y] = IA          #joueur=IA. On met le pion dans la matrice "comme si on jouait la"

        scoreIA=0

        #CALCUL DU SCORE : nous allons pour chaque case possible, attribué un score pour savoir ou joué.
        #Nous avons deux fonctions différentes : une minmax et une score opti.
        #Score optimisé : renvoie le nombre de puissance 4 possibles si on joue ici (en prenant en compte les pions déjà placé) (voir fonction pour plus de détail)
        scoreOptimise = OptimisationPossibilites(matrice, joueur, x, y)
        
        #Score MinMax : Fonction min max récursif (voir fonction pour plus de détail)
        scoreCoup = MinMaxParCoup(matrice, profondeur-1, Adversaire,0 , RepColonne) #profondeur = 3
        
        matrice[x][y] = 0           #On enleve le pion (placé pour le teste) de la matrice.
          
        #CHOIX DU SCORE:
        
        #Elagage alpha beta s'il gagne au prochain coup : arrete de regarder les autres possibilités
        if (scoreCoup == 500000): #dépend de certain paramètre de calcule de score
            meilleur = [x,y,scoreCoup]  
            break
        
        #CHOIX entre optimisé et minmaxCoup
        #Si score optimisé est meilleur que score minmaxParCoup:
        if scoreOptimise > abs(scoreCoup):
            scoreIA=scoreOptimise
        else:
            scoreIA=scoreCoup 
            
        #Définition du meilleur score pour ce coup
        score = [x,y,scoreIA]     
        
        #CHOIX MEILLEUR
        #Change meilleur score si existe un autre score mieux :
        if score[2] > meilleur[2]:
            meilleur = score  #  fonction max_value
        #Compte le nombre de meilleur score identiques : permet de palier au blocage 
        #(lorsque l'adversaire à plusieurs 2 pions alignés, ca fait le meme score partout si l'IA n'en a pas)                 
        elif score[2] == meilleur[2] or scoreCoup == -500000:
           compteur=compteur+1
        
        if scoreOptimise > meilleurScoreOpti[2] and scoreCoup != -500000: #ne joue pas ici si ca fait gagné l'adversaire
            meilleurScoreOpti = [x,y,scoreOptimise]
        
        #Remplace le score meilleur Score (qui est identique en toute case) par score optimisé
        if compteur == (len(CasesPossibilitesReduite)-1) :
            meilleur = meilleurScoreOpti
            #scorefin = OptimisationPossibilites(matrice, joueur)
            #Trouver un autre meilleur
            
    
    #Renvoie le meilleur coup :[ligne,colonne,score ]
    return meilleur
    
#Fonction min max. Fonction recursive
#Valeurs d'entrée: matrice = matrice de jeu remplie
#                  profondeur = nombre de coup qu'il reste a étudier
#                  joueur = joueur qui est en train de jouer (IA ou Adversaire)
#                  scoreInitial = 0 au début puis prend les valeur de scorConserve pour conserver le score
#                  repColonne = colonne du dernier jeton joué par l'adversaire  
#Valeur de sortie = scorefin pour le coup                 
def MinMaxParCoup(matrice, profondeur, joueur, scoreInitial, RepColonne): 
        
    #CAS ou la partie est finie: Si profondeur=profondeurINITIALE-1 : c'est que l'IA peut gagné au prochain tour et renvoie direct a minmax
                               # Sinon : Revoie a lui-même le score fin  
    if (Fin(matrice)) :
        #Calcule le score final de l'IA : 1,-1 ou 0
        scorefin = ScoreMinMax(matrice) 
        poidScore = 1
        
        #CAS:
        #Quand il perd, suite à un coup suposé de l'Adversaire:
        if (scorefin<0):                                # quand profondeurInitiale = 5, ic: profondeur =3 ou 1
            
            #Fonction pour calculer le poid du score selon la profondeur
            #Profondeur + 2 car plus de poids que pour >0
            for i in range (0,profondeur+3):
                poidScore = poidScore*10
                
            poidScore = poidScore*(profondeur+3)
            #Exemple: if profondeur=2 +2=4 => i=0,1,2,3 => poidScore=-2000
            #et : if profondeur = 0 +2=2 => i=0,1,2 => poidScore=-200 
            scorefin = scorefin * poidScore
            
        #Quand il gagne suite à un coup suposé de lui:
        else:                                           #p=2 : 3*3=9
            #Fonction pour calculer le poid du score selon la profondeur
            # Profondeur + 1 car si profondeur = 0 ca deviendrait 0...
            for i in range (0,profondeur+2):
                poidScore = poidScore*10
            #Exemple: if profondeur = 2 +1=3 => i=0,1 => poidScore=3000
            #if profondeur = 4 +1=5 => i=0,1,2,3,4 => poidScore=500 000
            poidScore = poidScore*(profondeur+2)
            
            scorefin = scorefin * poidScore
            
        #Return le scorefinal multiplié (pour accorder plus de poid selon si c'est un futur plus ou moins proche)
        return scorefin
    
    #Quand personne à gagné mais qu'il n'y a pu de profondeur (ne regarde pas plus dans le "futur")
    
    elif (profondeur == 0):
        scorefin = 0
        return scorefin
    
    #Quand personne gagne et qu'il reste de la profondeur : continue à regader le prochain cas : 

    #Mise à jour scoreConservé (utile lorsque on rappel la fonction)
    scoreConserve = scoreInitial
    
    #On veut savoir le MEILLEUR Score du COUP JOUE DANS MINMAX qui a appelé la fonction (coup de l'IA imaginé  déjà joué)
    #On va parcourir toutes les case ou l'on peut jouer (ici case réduite pour gagner du temps de calcule)
    #Pour chaque cases ou va chercher joué tout les coup suivnat (jusqu'à la profondeur)
    #On va ensuite attribuer un score global de tout ses chemins qui soient le plus conséquent
    
    #Initialisation pdes nouveaux cas possible (selon les cas joué)
    CasesPossibilitesReduite=PossibilitesReduite(matrice, RepColonne) 
    for case in CasesPossibilitesReduite:
        
        x, y = case[0], case[1]
        matrice[x][y] = joueur      #Démard par l'adversaire car joue après l'ia qui à joué dans minmax
    
    
        #RECURSIVITE : rappel de la fonction MinMaxParCoup selon qui joue : change le joueur et diminue la profondeur
        #En fonction du joueur qui à joué
        #Va regardé le coup suivant possible (selon CasesPossibilitesReduite)
        if (joueur == IA):    
            scoreFinalIA = MinMaxParCoup(matrice, profondeur-1, Adversaire, scoreConserve, RepColonne) 
            
        else:
            scoreFinalIA = MinMaxParCoup(matrice, profondeur-1, IA, scoreConserve, RepColonne)  

        #CALCUL SCORE :
        # Valleur absolue car on veut savoir si l'adversaire peut gagné dans un futur proche et donc évité cette situation.
        # C'est dans min max qu'on choisira un chemine à score "positif" plutot qu'un "négatif"
        if (abs(scoreConserve) < abs(scoreFinalIA) or scoreConserve == abs(scoreFinalIA)):
            scoreConserve = scoreFinalIA
            
        matrice[x][y] = 0
                
        #Elagage alpha-Beta : si l'adversaire gagne IMMEDIATEMENT au coup d'après si l'IA joue ici, pas besoin de regarder les autres chemins : l'adversaire va choisir cet emplacement
        #Marche PAs assez (sort de la boucle for mais pas de la récursivité)
        #4 : a changer si on change la profondeurInitial dans TourIA !! 
        if (scoreConserve==-500000): 
            break

    # Renvoie le meilleur score pour le coup initial au min max
    # OU : renvoie a scoreFinalIA en cas de récursivité
    return scoreConserve



#Donne le resultat de la partie et le gagnant
#Valeurs d'entrée : matrice = matrice du jeu remplie
#Valeur de sortie : dis (en cas de fin de partie immaginé) si l'IA gagne ou perd ou match null
def ScoreMinMax (matrice): 
    finJeu, gagnant = Gagnant(matrice)
    if (finJeu == True):
        if gagnant == IA:
            return  1                   
        elif gagnant == Adversaire:
            return  -1                  
        elif gagnant == "nul":
            return 0
    else :
        return 0
    

#modification de la matrice quand un joueur joue
#Valeurs d'entrée : matrice = matrice du jeu remplie
#                   ligne = ligne du piont joué
#                   colonne = colonne du piont joué
#                   joueur = joueur qui a joué le piont
#Valeur de sortie : matrice = matrice du jeu avec un nouveau jeton joué
def Modification (matrice, ligne, colonne, joueur):
    matrice[ligne][colonne] = joueur
    return matrice


#fait jouer l'IA 
#Valeurs d'entrée : matrice = matrice du jeu remplie
#                   repColonne = colonne du dernier jeton joué par l'adversaire
#Valeur de sortie : matrice = matrice du jeu modifié avec le jeton joué par l'IA   
def TourIA(matrice, repColonne):
    
    temps = time.perf_counter()
    tempstotal = 0
    casesvides = CasesVides(matrice)
    
    #Choix heuristique :
    profondeur = 4
    
    #Début de partie : cas 1er coup de l'IA :
    # Si l'IA commence : position au hasard au centre
    if (casesvides == 72):             
        ligne = 5                   
        colonne = rd.randint(5,6) #joue aléatoirement une des cases du milieu = plus de chance de gagné 
    #Si l'IA joue en 2e : Joue près de l'adversaire
    elif (casesvides == 71):            
        ligne = 5                   
        if repColonne==0:
            colonne = repColonne+1
        elif repColonne == 11:
            colonne = repColonne-1
        else :
            colonne = rd.choice([repColonne-1,repColonne+1])    #se met a droite au a gauche de la ou a joué l'adversaire
        
        
    #Reste de la partie:
    #Appel a MinMax
    else:           
        #Renvoie l'endoit ou l'IA doit jouer
        case = MinMax(matrice, profondeur, IA, repColonne)
        ligne, colonne = case[0], case[1]

    #L'IA joue à lendroit indiqué/choisi
        
    #Cas : IA a perdu dans tous les cas, selon elle (pour pas qu'elle ne joue pas du tout)   
    if (colonne==-1):
        CasesPossibilites=Possibilites(matrice)
        index = rd.randint(0,len(CasesPossibilites))
        colonne = CasesPossibilites[index][1]
        ligne = CasesPossibilites[index][0]
        
        
    matrice = Modification(matrice, ligne, colonne, IA)
    
    print("L'IA a joué en : ", colonne+1, " en ", round(time.perf_counter()-temps,2),"secondes")
    return matrice 
    

#fait jouer l'adversaire (= le joueur humain)
#Valeurs d'entrée : matrice = matrice du jeu remplie
#Valeur de sortie : matrice = matrice du jeu modifié avec le jeton joué par le joueur 
#                   reponseColonne = colonne dans laquelle le joueur a joué
def TourAdversaire(matrice): 

    if (Fin(matrice)):
        return matrice
    
    caseChoisie = False
    while caseChoisie == False:   
        Colonne = input('Quelle colonne voulez-vous modifier?')
        reponseColonne = int(Colonne)-1 
        compteur=0
        if (reponseColonne<=len(matrice[0])-1 and reponseColonne>-1):
            for i in range(5,-1,-1):
                if (matrice[i][reponseColonne]== 0):
                    matrice[i][reponseColonne] = Adversaire
                    caseChoisie = True
                    break;
                else:
                    compteur=compteur+1
                    if(compteur==len(matrice)):
                        print('La colonne est déjà remplie, choississez une autre case')
                        caseChoisie = False
                        break;
        else:
            print("La case n'existe pas , choississez une autre case")
            caseChoisie = False     
            
    return (matrice, reponseColonne)


#calcul le nombre de possibilité de puissance 4 que permet un nouveau jeton (placé dans la case x, y )
#Variables d'entrée: matrice = matrice du jeu remplie
#                    joueur = le joueur qui est en train de jouer (IA ou Adversaire)
#                    x = ligne du nouveau jeton
#                    y = colonne du nouveau jeton
#Variable de sortie: compteurG = nombre de possibilité d'aligné 4 pionts pour le joueur
def OptimisationPossibilites(matrice, joueur, x,y): 
    
    nbligne = len(matrice)
    nbcolonne = len(matrice[0])
    compteurG = 0
    #l est une matrice, il faut créer une variable int qui soit comparable à x. Pour etudier qu ela ligne du nouveau jeton
    ligne =0
    #test lignes   
    for l in matrice:
        if (ligne == x ):
            compteurL = 0
            zero = 3 #on ne contabilise les puissances 4 qui comptent au maximum 3zéros
            valeur = [-1,-1,-1,-1]
            aligné = 0 #compte le nombre de jeton compris dans le puissance 4
            #la variable zero permet de ne pas compter les possibilités consitituées uniquement de case vide. 
            #Il doit y avoir au moins un piont pour etre comptabilisé
            for c in range(len(l)):
                if (l[c]!= joueur and l[c]!=0):
                    compteurL = 0
                    #on remet le compteur a 0 car il y a un piont adverse
                    valeur[3]=-1
                    aligné=0 #le nombre de jetons alignés retombe a 0
                elif l[c]==0 and zero != 0:
                    compteurL = compteurL+1
                    zero = zero-1
                    valeur[3]=0
                elif l[c] == joueur:
                    compteurL = compteurL+1
                    zero = 3
                    aligné = aligné+1 #un jeton de plus aligné
                    valeur[3]=joueur
                if (compteurL >= 4):
                    compteurL = compteurL-1 
                    if(c>=y and c<=y+3):
                        compteurG = compteurG+ 10**aligné
                    if valeur[0] == joueur:
                        aligné = aligné-1                 
                valeur[0],valeur[1],valeur[2] = valeur[1],valeur[2],valeur[3]

        ligne = ligne+1
        
    #test colonnes     
    for c in range(nbcolonne) :
        if (c == y):
            compteurC = 0
            zero = 3
            valeur = [-1,-1,-1,-1] #tableau des 4 dernieres valeur parcourues
            aligné = 0 #compte le nombre de jeton compris dans le puissance 4
            for l in range (nbligne-1,-1,-1):
                if (matrice [l][c] != joueur and matrice [l][c]!=0) :
                    compteurC = 0
                    valeur[3]=-1
                    aligné = 0 #le nombre de jetons alignés retombe a 0
                elif (matrice [l][c]==0 and zero != 0):
                    compteurC = compteurC+1
                    zero = zero-1
                    valeur[3]=0
                elif (matrice [l][c] == joueur):
                    compteurC = compteurC+1
                    aligné = aligné+1 #un jeton de plus aligné
                    zero = 3
                    valeur[3]=joueur
            if (compteurC >= 4):
                compteurC = compteurC-1 
                compteurG = compteurG+ 10**aligné

    #test diagonales 
    #matrice de 6 cases:
    compteurG = OptimisationDiagonale(matrice, joueur, 0, 7,5,-1, compteurG, nbcolonne, x,y)
                
    #diagonales de 5 cases:
    compteurG = OptimisationDiagonale(matrice, joueur, 7, 8,5,0, compteurG, nbcolonne,x,y)
    compteurG = OptimisationDiagonale(matrice, joueur, 0, 1,4,-1, compteurG, nbcolonne,x,y)
            
    #diagonales de 4 cases:
    compteurG = OptimisationDiagonale(matrice, joueur, 8, 9,5,1, compteurG, nbcolonne,x,y)    
    compteurG = OptimisationDiagonale(matrice, joueur, 0, 1,3,-1, compteurG, nbcolonne,x,y)

    return compteurG

#compte le nombre de possibilité de faire un puissance 4 en diagonale
#Valeurs d'entrée : matrice = matrice du jeu remplie
#                   joueur = le joueur qui est en train de jouer (IA ou Adversaire)
#                   startd = premiere valeur prise pas d
#                   endd = derniere valeur prise pas d + 1
#                   startt = premiere valeur prise pas t
#                   endt = dernier valeur prise pas t -1
#                   compteurG = nombre de possibilités deja comptabilisées
#                   nbcolonne = nombre de colonne de la matrice
#                    x = ligne du nouveau jeton
#                    y = colonne du nouveau jeton
#Variable de sortie: compteurG = nombre de possibilité d'aligné 4 pionts pour le joueur
def OptimisationDiagonale(matrice, joueur, startd, endd,startt,endt, compteurG, nbcolonne,x,y):
 for d in range (startd, endd, 1): 
    compteurA = 0
    compteurB = 0
    zero1 = 3
    zero2 = 3
    valeur1 = [-1,-1,-1,-1] #tableau des 4 dernieres valeur parcourues
    valeur2 = [-1,-1,-1,-1]
    aligné1 = 0
    aligné2 = 0 #compte le nombre de jeton compris dans le puissance 4
    #les variable diag1 et diag2 permette de savoir si le nouveau jeton appartient a la diagnonale
    diag1 = False
    diag2 = False
    h = nbcolonne - 1 -d
    for t in range(startt,endt,-1):
        #diaonales 1 
        #on verifie si une des case de la diagonale est celle que l'on etudie
        if (t == x and d==y ):
            diag1 = True
        if (matrice[t][d] != joueur and matrice [t][d]!=0): 
            compteurA = 0
            valeur1[3]=-1
            aligné1 = 0 #le nombre de jetons alignés retombe a 0
        elif (matrice [t][d]==0 and zero1 != 0):
            compteurA = compteurA +1
            zero1 = zero1-1
            valeur1[3]=0
        elif(matrice[t][d] == joueur):
            compteurA = compteurA +1
            aligné1 = aligné1+1
            zero1 = 3
            valeur1[3]=joueur
        if (compteurA >= 4 and diag1==True and y<=d<=y+3):
            compteurA = compteurA-1 
            compteurG = compteurG+ 10**aligné1
            if valeur1[0] == joueur:
                aligné1 = aligné1-1                 
        valeur1[0],valeur1[1],valeur1[2] = valeur1[1],valeur1[2],valeur1[3]
        
        #diagonales 2
        #on verifie si une des case de la diagonale est celle que l'on etudie
        if (t == x and h==y ):
            diag2 = True
        if (matrice[t][h] != joueur and matrice [t][h]!=0):
            compteurB = 0
            valeur2[3]=-1
            aligné2 = 0 #le nombre de jetons alignés retombe a 0
        elif (matrice [t][h]==0  and zero2 != 0):
            compteurB = compteurB +1
            zero2 = zero2-1
            valeur2[3]=0
        elif(matrice[t][h] == joueur):
            compteurB = compteurB +1
            aligné2 = aligné2+1
            zero2 = 3
            valeur2[3]=joueur
        if (compteurB >= 4 and diag2==True and y-3<=h<=y):
            compteurB = compteurB-1 
            compteurG = compteurG+ 10**aligné2
            if valeur2[0] == joueur:
                aligné2 = aligné2-1                 
        valeur2[0],valeur2[1],valeur2[2] = valeur2[1],valeur2[2],valeur2[3]
        h = h-1
        d=d+1

 return compteurG

#Permet de savoir si la partie est finie  
#Valeurs d'entrée : matrice = matrice du jeu remplie
#Valeurs de sortie: fin = booléen pour savoir si la partie est finie
#                   retourne egalement le joueur gagnant : IA = 1 Adversaire = 2 match nul = "nul" si la partie n'est pas finie = -1
def Gagnant (matrice): 
    
    nbligne = len(matrice)
    nbcolonne = len(matrice[0])
    fin = False
    
    #test lignes   
    for l in matrice:
        compteurL = 0
        for c in range(len(l)-1):
            if (l[c]!=l[c+1]):
                compteurL = 0
            elif (l[c]==l[c+1] and l[c]!=0):
                compteurL = compteurL+1
            if (compteurL == 3):
                fin = True
                return (fin, l[c])
            
    #test colonnes     
    for c in range(nbcolonne) :
        compteurC = 0
        for l in range (nbligne-1):
            if (matrice [l][c] != matrice[l+1][c]) :
                compteurC = 0
            elif (matrice [l][c] == matrice[l+1][c]and matrice [l][c]!=0) :
                compteurC = compteurC+1
            if (compteurC == 3):
                fin = True
                return (fin,matrice[l][c])
        
        
    #test diagonales
    
    #diagonales de 6 cases
    for d in range (7): #il y a 6 diagonales a tester
        compteurA = 0
        compteurB = 0
        h = nbcolonne - 1 -d 
        for t in range(5):#diagonale de 6 cases (avec +1 = 6)
            #diaonales 1
            if (matrice[t][d] != matrice[t+1][d+1]):
                compteurA = 0
            elif (matrice[t][d] == matrice[t+1][d+1] and matrice [t][d]!=0):
                compteurA = compteurA +1
            if (compteurA == 3):
                fin = True
                return (fin, matrice[t][d])
            #diagonales 2
            if (matrice[t][h] != matrice[t+1][h-1]):
                compteurB = 0
            elif (matrice[t][h] == matrice[t+1][h-1] and matrice [t][h]!=0):
                compteurB = compteurB +1
            if (compteurB == 3):
                fin = True
                return (fin, matrice[t][h])
            h = h-1
            d=d+1
            
    #diagonales de 5 CASES
    compteurA = 0
    compteurB = 0
    d=7
    h = nbcolonne - 1 - d 
    for t in range(4):#diagonale de 5 cases (avec +1 = 5)
            #diaonales 1
        if (matrice[t][d] != matrice[t+1][d+1]):
               compteurA = 0
        elif (matrice[t][d] == matrice[t+1][d+1] and matrice [t][d]!=0):
            compteurA = compteurA +1
        if (compteurA == 3):
            fin = True
            return (fin, matrice[t][d])
        #diagonales 2
        if (matrice[t][h] != matrice[t+1][h-1]):
               compteurB = 0
        elif (matrice[t][h] == matrice[t+1][h-1] and matrice [t][h]!=0):
            compteurB = compteurB +1
            if (compteurB == 3):
               fin = True
               return (fin, matrice[t][h])
        h = h-1
        d=d+1
    
    compteurA = 0
    compteurB = 0
    d=0
    h = nbcolonne - 1 - d 
    for t in range(1,5):#diagonale de 5 cases (avec +1 = 6)
            #diaonales 1
        if (matrice[t][d] != matrice[t+1][d+1]):
               compteurA = 0
        elif (matrice[t][d] == matrice[t+1][d+1] and matrice [t][d]!=0):
            compteurA = compteurA +1
        if (compteurA == 3):
            fin = True
            return (fin, matrice[t][d])
        #diagonales 2
        if (matrice[t][h] != matrice[t+1][h-1]):
               compteurB = 0
        elif (matrice[t][h] == matrice[t+1][h-1] and matrice [t][h]!=0):
            compteurB = compteurB +1
            if (compteurB == 3):
               fin = True
               return (fin, matrice[t][h])
        h = h-1
        d=d+1
            
    #diagonales de 4 CASES
    compteurA = 0
    compteurB = 0
    d=8
    h = nbcolonne - 1 - d 
    for t in range(3):#diagonale de 4 cases (avec +1 = 4)
            #diaonales 1
        if (matrice[t][d] != matrice[t+1][d+1]):
               compteurA = 0
        elif (matrice[t][d] == matrice[t+1][d+1] and matrice [t][d]!=0):
            compteurA = compteurA +1
        if (compteurA == 3):
            fin = True
            return (fin, matrice[t][d])
        #diagonales 2
        if (matrice[t][h] != matrice[t+1][h-1]):
               compteurB = 0
        elif (matrice[t][h] == matrice[t+1][h-1] and matrice [t][h]!=0):
            compteurB = compteurB +1
            if (compteurB == 3):
               fin = True
               return (fin, matrice[t][h])
        h = h-1
        d=d+1
    
    compteurA = 0
    compteurB = 0
    d=0
    h = nbcolonne - 1 - d 
    for t in range(2,5):#diagonale de 3 cases (avec +1 = 4)
        #diaonales 1
        if (matrice[t][d] != matrice[t+1][d+1]):
            compteurA = 0
        elif (matrice[t][d] == matrice[t+1][d+1] and matrice [t][d]!=0):
            compteurA = compteurA +1
        if (compteurA == 3):
            fin = True
            return (fin, matrice[t][d])
        #diagonales 2
        if (matrice[t][h] != matrice[t+1][h-1]):
               compteurB = 0
        elif (matrice[t][h] == matrice[t+1][h-1] and matrice [t][h]!=0):
            compteurB = compteurB +1
            if (compteurB == 3):
               fin = True
               return (fin, matrice[t][h])
        h = h-1
        d=d+1
    
    #test si il y a 42 jetons, la matrice est donc pleine mais il n'y a pas de gagnant
    #match nul
    if (CasesVides(matrice) == 30  and fin == False):
        fin = True
        return (fin, "nul")        
    
    #si la partie n'est pas finie
    if (fin == False):
        return (fin, -1)


    
#affiche le gagnant si la partie est finie
#Valeurs d'entrée : matrice = matrice du jeu remplie
def ScoreFinal (matrice): 
    finJeu, gagnant = Gagnant(matrice)
    if (finJeu == True):
        if gagnant == Adversaire:
            print ("Le gagnant est le joueur 1 (vous)")
        elif gagnant == IA:
            print ("Le gagnant est le joueur 2 (IA)")
        elif gagnant == "nul":
            print ("Match nul")

#defini si le jeu est fini 
#Valeurs d'entrée : matrice = matrice du jeu remplie
#Valeur de sortie : True si le jeu est fini, False sinon
def Fin(matrice): 
    finJeu, gagnant = Gagnant(matrice)
    if finJeu == True:
        return True
    else:
        return False
    

#Lance le tour du bon joueur
#Valeurs d'entrée : matrice = matrice du jeu remplie
#                   reponseColonne = colonne du dernier jeton joué par l'adversaire
#Valeur de sortie : reponseColonne = colonne du dernier jeton joué par l'adversaire
def Tour(matrice, joueur, reponseColonne): 
    if(joueur == IA):
        print("C'est à l'IA de jouer")
        matrice = TourIA(matrice, reponseColonne) 
        Affichage(matrice)

    else:
        print("C'est à vous de jouer:")
        matrice, reponseColonne = TourAdversaire(matrice) 
        Affichage(matrice)
        
        #Renvoie la ou il a joué pour que l'IA le sache
        return reponseColonne

        
#Lancement de la partie. Permet de lancer le jeu  
def Puissance_4():  
    debut= ' '
    while (debut != 'oui' and debut != 'non'):
        debut = (input('Veux-tu jouer en 1er ? (oui/non):  ')).lower()

    Puissance_4=CreationPuissance_4()
    Affichage(Puissance_4)
    
    if debut == 'oui':
        joueur = Adversaire
        joueur2 = IA
    else :
        joueur = IA
        joueur2 = Adversaire
    
    #Initialisation dernière réponse de l'adversaire (n'a pas encore joué)
    reponseColonne=-1
    
    while (not Fin(Puissance_4)):
        reponseColonne = Tour(Puissance_4, joueur, reponseColonne)
        joueur, joueur2 = joueur2, joueur
        ScoreFinal(Puissance_4)

#Lance le jeu:       
Puissance_4() 

    
