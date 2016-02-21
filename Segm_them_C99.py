#!/usr/bin/env python
# coding: utf-8

"""
	Projet segmentation thématique ; Jan, Fev 2016
	D. Dufresne;
	
	# almost finished, need debugging and tests with authentic texts
"""
import random, string;
def random_char(y):
       return ''.join(random.choice(string.ascii_lowercase) for x in range(y))
       
def genere_corpus(nbPhrase, taillePhrase ): #taillePhrase: (a,b) avec a < b
	corpus=[];
	if taillePhrase[0] >taillePhrase[1]:
		return corpus;
	for a in range (nbPhrase):
		mot=[];
		for a in range (taillePhrase[0]+random.randint(0,taillePhrase[1]-taillePhrase[0])):
			mot.append(random_char(longueur_mots));
		corpus.append(mot);
	return corpus;
	


#calcule les occurences phrase par phrase!
def genere_frequences(corpus):
	## On suppose ici que la fréquence d'un mot dans une phrase est juste:
	# card(mot dans phrase) / card ( phrase)
	corpus_freqs=[];
	for a in corpus:
		freq=dict();
		for u in a:
			if u in freq:
				freq[u]+=1;
			else:
				freq[u]=1;
		corpus_freqs.append(freq);
	return corpus_freqs;

## calcule les occurences sur l'ensemble du corpus !
def genere_Totalfreq(corpus):
	## On suppose ici que la fréquence d'un mot dans une phrase est juste:
	# card(mot dans phrase) / card ( phrase)
	corpus_freqs=[];
	freq=dict();
	for a in corpus:
		for u in a:
			if u in freq:
				freq[u]+=1;
			else:
				freq[u]=1;
	return freq;
				

from math import sqrt;
def calcule_sim ( freq_x,freq_y):	
	numerator=0;
	denom_x=0;
	denom_y=0;
	for a in freq_x:
		if a in freq_y:
			numerator += freq_x[a]*freq_y[a];
		denom_x+=freq_x[a]**2;
	for b in freq_y:
		denom_y+=freq_y[b]**2;	
	return numerator /  ( sqrt ( denom_x*denom_y));

def create_similarity_matrix(frequencies):
	taille=len(frequencies);
	MATRICE=[ [0]*taille for a in range(taille)];
	
	for a in range(taille):
		for b in range(0,a+1):
			sin=calcule_sim(frequencies[a],frequencies[b]);
			MATRICE[a][b]=sin;
			MATRICE[b][a]=sin;
	return MATRICE;
	
	
	
	# rank = #(elem with lower value) / #(elem checked)
	# #(elem checked) = nb d'elem du carré -1 !!
def calcule_rang(similarity_matrix,plage,position):
	taille=len(similarity_matrix);
	numerator=0;
	## au fond, le denom est identique sur toute la matrice, est_ce utile ?
	val=similarity_matrix[position[0]][position[1]];

	X=(max(0,position[0]-plage),min(taille,position[0]+plage+1));
	Y=(max(0,position[1]-plage),min(taille,position[1]+plage+1));

	denom=(X[1]-X[0])*(Y[1]-Y[0])-1;
	for a in range(X[0],X[1]):
		for b in range(Y[0],Y[1]):			
			if similarity_matrix[a][b] < val:
				numerator+=1;

	return float(numerator)/denom;

# si matrice ranking est symétrique, algo simplifiable en complexité !
def genere_ranking(similarity_matrix,window_size):
	taille=len(similarity_matrix);
	MATRICE=[ [0]*taille for a in range(taille)];
	
	plage=window_size//2;
	for ligne in range(0,taille):		
		for colonne in range(0,taille):
			truc=calcule_rang(similarity_matrix,plage,(ligne,colonne));
			MATRICE[ligne][colonne]=truc;	
	return MATRICE;
		



#  algo de calcul récursif proposé dans Papier #améliorable en espace ... avec Objet !
def calcule_S_i_j(ranking_matrice):
	taille=len(ranking_matrice);
	MATRICE=[ [0]*taille for a in range(taille)];
	
	# 1ere étape:
	for i in range(0,taille):
		MATRICE[i][i]=ranking_matrice[i][i];
	#2eme étape:
	for i in range(0,taille-1):
		val=2*ranking_matrice[i+1][i] +MATRICE[i][i]+MATRICE[i+1][i+1];
		MATRICE[i+1][i]=val;
		MATRICE[i][i+1]=val;
	#3eme étape:
	for j in range(2,taille):
		for i in range(0,taille-j):
			val=2*ranking_matrice[i+j][i]+MATRICE[i+j-1][i]+MATRICE[i+j][i+1]-MATRICE[i+j-1][i+1];
			MATRICE[i][i+j]=val;
			MATRICE[i+j][i]=val;
	return MATRICE;

def _getAij( i , j):
	val=j-i+1;
	return val*val;

# return mean, std deviation (root of variance);
def statistics (ElemList):
	_mean=0;
	for i in ElemList:
		_mean+= i;
	_mean = float(_mean)/ len(ElemList);
	
	_variance=0;
	for i in ElemList:
		deviation= i-_mean;
		_variance+= deviation * deviation;
	return _mean, _variance**0.5;	
	
	
def calcule_density (ListofCouples, dictionnaire_Sij):
	numerator=0;
	denominator=0;
	for a in ListofCouples:
		numerator += dictionnaire_Sij[a[0]][a[1]];
		denominator += _getAij( a[0] , a[1]);
	return float(numerator)/denominator;

def find_best_cut ( ensemble_B, dictionnaire_Sij, old_density):
	taille=len(dictionnaire_Sij);
	maxdensity=old_density;
	listSij=[dictionnaire_Sij[a[0]][a[1]] for a in ensemble_B];
	listAij=[_getAij( a[0] , a[1]) for a in ensemble_B];
	
	Bsegment_ind=-1;
	bestcutindice=-1;
	for indice in range(len(ensemble_B)):
		start=ensemble_B[indice][0];
		end=ensemble_B[indice][1];
		sum_Sij= sum(listSij) - listSij[indice];
		sum_Aij= sum(listAij) - listAij[indice];
		
		for cut_ind in range(start, end+1):
			numerator=  ( sum_Sij  + dictionnaire_Sij[start][indice]+dictionnaire_Sij[indice+1][end] ) 
			denom= ( sum_Aij  +_getAij(start,indice) + _getAij(indice+1, end) );
			if numerator/denom > maxdensity:
				maxdensity=numerator/denom;
				Bsegment_ind,bestcutindice= indice, cut_ind;
				
	if Bsegment_ind <0 and bestcutindice <0 :
		print(Bsegment_ind,bestcutindice, '-->', ensemble_B );
		return ensemble_B, maxdensity;
	else:
		cutted=ensemble_B[Bsegment_ind];
		print(Bsegment_ind,bestcutindice, ' OK');
		newEnsB = [ ensemble_B[item] for item in range(0,Bsegment_ind)];
		newEnsB+= [(cutted[0],bestcutindice),(bestcutindice+1,cutted[1])];
		newEnsB+= [ ensemble_B[item] for item in range(Bsegment_ind+1,len(ensemble_B))];
		return newEnsB,maxdensity;


import time;
## B = ensemble de tuple ordonné : [(0,taille-1)] puis après subdivisions [...] ----> [(0,a),(a+1,b),(b+1,c),...,(z+1,taille-1)]
# D --> donné par formule !
def boucle_de_maximisation(ensemble_B, dictionnaire_Sij):
	
	print(ensemble_B);
	c=1.2;
	boolean1= True;
	densities=[calcule_density (ensemble_B, dictionnaire_Sij)];
	print('\t--> '+repr(densities[0]));
	delta_densities=[];
	oldEns_B=ensemble_B;
	while boolean1:
		newBestEnsenble_B, newDensity=find_best_cut ( oldEns_B, dictionnaire_Sij, densities[len(densities)-1]);
		print(newBestEnsenble_B);
		print('\t--> '+repr(newDensity));
		time.sleep(1);
		densities.append(newDensity);
		oldEns_B=newBestEnsenble_B;
		newDelta_D=	newDensity-densities[len(densities)-1];
		delta_densities.append(newDelta_D);
		mean,std_dev= statistics (delta_densities);
		
		boolean1= newDelta_D >= mean + c* std_dev;
	return oldEns_B;
	
############################
#### TEST : 

longueur_mots=2;
nb_phrases=100;
taille_phrases=(15,20); # (b,c) : b à c mots par phrase;
window_size=7; #must be impair !
print ('### Debut du test ###');
print('## Création du corpus');

test=genere_corpus(nb_phrases,taille_phrases); # generation aleatoire de simuli phrases ...
test_freqs=genere_frequences(test); # Calcul des frequences dans chaque mot
total_freq=genere_Totalfreq(test); # Calcul des frequences globales
sim_matrX=create_similarity_matrix(test_freqs); # Creation de la matrice de similarité , formule dans l'article
rank_mat=genere_ranking(sim_matrX,window_size); # Generation des rangs sur la matrice, ( dependant de "window size")
S=calcule_S_i_j(rank_mat);	# Pre computation , permet d'améliorer le temps global de l'algo ....
#for a in S:
#	print S;

RESULTAT=boucle_de_maximisation([(0,nb_phrases-1)], S); # methode de clustering, de l'algo !
print('Resultat is:');
#print(RESULTAT);
