import numpy as np
import matplotlib.pyplot as plt
import random as rd

def readFile():
    txtFile = open("liste_francais.txt","r")
    contents = txtFile.read().splitlines()
    txtFile.close()
    dataBase = np.array([x for x in contents])    
    return dataBase

def tetaSetup(k):
    tetaArray = []
    for i in range (k):
        tetaArray.append(rd.uniform(0.4,0.6))
    return tetaArray

def hash(word,teta,N):
    
    # Encodage du mot
    
    codedWord = ""
    
    for lettre in word :
        asciiLetter = ord(lettre)
        binaryLetter = bin(asciiLetter)[2:]
        codedWord += binaryLetter
    
    codedWord = int(codedWord,2)    
    
    # Hashage du mot
    
    r = codedWord*teta
    
    hashedWord = int((r%1)*N)
    
    return hashedWord

def test(word,tetaArray,N,bloomFilter):
    
    
    for teta in tetaArray :
        codedWord = ""
        
        for lettre in word :
            asciiLetter = ord(lettre)
            binaryLetter = bin(asciiLetter)[2:]
            codedWord += binaryLetter
        
        codedWord = int(codedWord,2)    
        
        # Hashage du mot
        
        r = codedWord*teta
        
        hashedWord = int((r%1)*N)
        
        if(bloomFilter[hashedWord]==0):
            return 0
    
    return 1

def bloomFilterFunction(n):
    
    liste_francais = readFile()
    hashFunctionAmount = n
    tetaArray = tetaSetup(hashFunctionAmount)
    N = 15000
    bloomFilter = [0 for i in range(N)]
    
    for i in range(10000,11000):
        for teta in tetaArray :        
            bloomFilter[hash(liste_francais[i],teta,N)] = 1
            
    fauxPositifs = 0
    for j in range(1000,2000):
        fauxPositifs += test(liste_francais[j],tetaArray,N,bloomFilter)
    
    #tauxFauxPositifs = fauxPositifs * 100 /
    return fauxPositifs
    
def main():
    
    for i in range (0,100):
        fauxPositifsAmount = []
        tetas = np.arange(2,9)
        for hashNumber in range (2,9):
            fauxPositifsAmount.append(bloomFilterFunction(hashNumber))
            
        plt.plot(tetas,fauxPositifsAmount)
    
    plt.xlabel("Nombre de fonctions de hashage")
    plt.ylabel("Nombre de faux positifs")
    plt.title("Faux positifs en fonction de nombre de tetas")
    plt.show()
    
    
main()