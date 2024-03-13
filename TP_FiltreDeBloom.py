import numpy as np
import matplotlib.pyplot as plt
import random as rd

# Cette fonction lit un fichier texte contenant une liste de mots français, puis retourne une liste contenant ces mots.
def lireFichier(): 
    File = open("liste_francais.txt","r")
    données = File.read().splitlines()
    ens_données = np.array([x for x in données]) 

    File.close() 
    return ens_données


# Cette fonction réalise le hachage d'un mot.
# Les paramètres teta sont utilisés pour créer un résultat unique pour chaque mot.
# Le résultat est ensuite réduit à une valeur dans la plage [0, N-1].
def hashage(mot, teta, N):
    
    # Encodage du mot
    motCrypté = ""
    
    for lettre in mot:
        lettre = ord(lettre)
        lettre_binaire = bin(lettre)[2:] #pour passer en binaire
        motCrypté += lettre_binaire
    
    motCrypté = int(motCrypté, 2)    
    
    # Hashage du mot
    r = motCrypté * teta
    motCrypté = int((r % 1) * N)
    
    return motCrypté


# Cette fonction initialise un tableau contenant les valeurs de teta générées aléatoirement dans l'intervalle [0.4, 0.6].
def F_teta(k):
    liste_teta = []
    for i in range (k):
        liste_teta.append(rd.uniform(0.4,0.6))
    return liste_teta


# Cette fonction teste si un mot est potentiellement présent dans un filtre de Bloom.
# Elle prend en compte plusieurs paramètres : le mot à tester, un tableau de paramètres teta, la taille du filtre de Bloom (N), et le filtre de Bloom lui-même.
# Elle retourne 0 si le mot n'est pas présent (selon le test probabiliste), sinon elle retourne 1.
def test_presence(mot, liste_teta, N, Filtre_Bloom):
    for teta in liste_teta:
        motCrypté = ""
        
        for lettre in mot:
            lettre = ord(lettre)
            lettre_binaire = bin(lettre)[2:]
            motCrypté += lettre_binaire
        
        motCrypté = int(motCrypté, 2)    
        
        # Hashage du mot
        r = motCrypté * teta
        motCrypté = int((r % 1) * N)
        
        if Filtre_Bloom[motCrypté] == 0:
            return 0
    
    return 1


#Finalement la focntion principale du filtre de bloom qui utise les fonctions précédentes et qui retourne le nomb re de faux positifs

def Filtre_Bloom_Fonction(n): 
    
    liste_francais = lireFichier()
    N = 10000
    fauxPositifs = 0
    NbFonctionHashage = n
    liste_teta = F_teta(NbFonctionHashage)
    
    Filtre_Bloom_liste = []
    Filtre_Bloom_liste.extend([0]*N)
    
    for i in range(10000,11000):
        for teta in liste_teta :        
            Filtre_Bloom_liste[hashage(liste_francais[i],teta,N)] = 1
            
    
    for i in range(1000,2000):
        fauxPositifs += test_presence(liste_francais[i],liste_teta,N,Filtre_Bloom_liste)
    return fauxPositifs
    

#main qui permet l'affichage du graphique grace a matplotlib pour se rendre compte du nombres de faux positifs en fonction de teta 
def main():
    
    for i in range (0,100):
        Nb_Faux_Positifs = []
        tetas = np.arange(2,9)
        for motCrypté in range (2,9):
            Nb_Faux_Positifs.append(Filtre_Bloom_Fonction(motCrypté))
            
            
        plt.plot(tetas,Nb_Faux_Positifs)
    
    plt.xlabel("Nombre fonctions de hashage")
    plt.ylabel("Nombre de faux positifs")
    plt.title("Faux positifs en fonction de teta")
    plt.show()
    
    
main()