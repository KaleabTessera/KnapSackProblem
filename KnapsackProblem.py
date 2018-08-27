# -*- coding: utf-8 -*-
import numpy as np
def calculateScore(v,w,n):
    score = np.array([])
    for i in range(n):
        score = np.append(score,round((v[i]/w[i]),3)) 
    scoreIndexs = np.argsort(-score)
    
    return scoreIndexs

def linearKnapSack(v,w,n,W,shouldPrint=False):
    sumItemsInKnapsack = 0
        
    scoreIndexs =  calculateScore(v,w,n)
    indexofElementsInKnapsack = np.zeros(n).astype(int)
    
    for i in range(n):
       indexOfLargestElement = scoreIndexs[i]
       if((sumItemsInKnapsack+w[indexOfLargestElement]) <= W ):
           indexofElementsInKnapsack[indexOfLargestElement] = 1 
           sumItemsInKnapsack += w[indexOfLargestElement]
           if(shouldPrint):
               print("Adding (",v[indexOfLargestElement],",",w[indexOfLargestElement], ") to the knapsack")    
    
    if(shouldPrint):
        print("***************************")
        print("Arrays: ")
        print("v_i = {0}".format(v))
        print("w_i = {0}".format(w))
        print("x_i = {0}".format(indexofElementsInKnapsack))
        
    return indexofElementsInKnapsack

    
def findSubsets(allSubsets,subset,currentIndex,k):      
    if(len(subset) == currentIndex):
        return allSubsets
    
    newSet = []
    for i in range(0,len(allSubsets)):
      if(len(allSubsets[i]) < k):
        newSet = allSubsets[i].copy()
        newSet.append(subset[currentIndex])
        allSubsets.append(newSet)
        
    findSubsets(allSubsets, subset, currentIndex+1,k)

def isLargerThanCapicity(chosenW,W):
      sumWeights = np.sum(chosenW)
      if(sumWeights > W):
          return True
      else:
          return False
        
def finaAllSubsets(array, subsetSize,k):
    allSubsets = [[]]
    findSubsets(allSubsets,array,0,k)
    returnSet = []
    for sets in allSubsets:
        if(len(sets) == subsetSize):
            returnSet.append(sets)      
    return returnSet

def PTAS(v,w,n,W,minSizeSubset,k,shouldPrint=False):
    allSubsets = [[]]
    indexOfSet = []
    for i in range(0,28):
        indexOfSet.append(i)
        
    allSubsets = finaAllSubsets(indexOfSet,minSizeSubset,k)
    allSubsetsNumpy = np.array(allSubsets)
    highestProfit = 0
    bestSetIndex = []
    bestLinearIndex = []
    for sets in allSubsetsNumpy:
        chosenV = np.take(v,sets)
        chosenW = np.take(w,sets)  
        if(isLargerThanCapicity(chosenW,W) == False):
            otherV = np.take(v,list(set(indexOfSet) - set(sets)))
            otherW = np.take(w,list(set(indexOfSet) - set(sets)))
            sumProfitPTAS = np.sum(chosenV)
            sumWeights = np.sum(chosenW)
            remainingW = W - sumWeights
            indexofElementsInKnapsack = linearKnapSack(otherV,otherW,len(otherV) ,remainingW)
            totalProfit = sumProfitPTAS + np.sum(otherV[indexofElementsInKnapsack==1])
            if(shouldPrint):
                print("Weight - PTAS: ",sumWeights)
                print("Profit - PTAS: ",sumProfitPTAS)
                print("Total Profit: ",totalProfit)
                print("***************************")
                
            if(totalProfit >highestProfit ):
                highestProfit = totalProfit
                bestSetIndex = sets
                bestLinearIndex = indexofElementsInKnapsack
                bestOtherV = otherV
                bestOtherW = otherW
    
    bestLinearIndexValues = np.where(bestLinearIndex==1)
    print("Best Indexs for PTAS:",bestSetIndex)  
    print("Selected v - PTAS:",np.take(v,bestSetIndex))  
    print("Selected v - Linear:",np.take(bestOtherV,bestLinearIndexValues)[0])  
    print("Selected v - all:",np.concatenate([np.take(v,bestSetIndex),np.take(bestOtherV,bestLinearIndexValues)[0]]))
    print("Selected w - all",np.concatenate([np.take(w,bestSetIndex),np.take(bestOtherW,bestLinearIndexValues)[0]]))
    print("Total Weight - all",np.sum(np.concatenate([np.take(w,bestSetIndex),np.take(bestOtherW,bestLinearIndexValues)[0]])))
    print("Best Profit - all",highestProfit)                                                          

def problem1():
    # =============================================================================
    #     Problem 1 - Linear Knapsack Problem
    # =============================================================================
    n = 28
    v = np.array([2,6,8,7,3,4,6,5,10,9,8,11,12,15,6,8,13,14,15,16,13,14,15,26,13,9,25,26])
    w = np.array([7,3,3,5,4,7,5,4,15,10,17,3,6,11,6,14,4,8,9,10,14,17,9,24,11,17,12,14])
    W = 30
    
    # =============================================================================
    #     Linear Knapsack Problem - Greedy Algorithm
    # =============================================================================
    print("Problem 1 - Greedy Algorithm ")
    indexofElementsInKnapsack = linearKnapSack(v,w,n,W)
    print("Selected w:",w[indexofElementsInKnapsack==1])  
    print("Selected v:",v[indexofElementsInKnapsack==1])  
    
    # =============================================================================
    #     Linear Knapsack Problem - PTAS
    # =============================================================================
    print("\n \n Problem 1 - Polynomial Time Approximation Algorithm (PTAS) ")
    minSizeSubset = 3
    k = 10
    PTAS(v,w,n,W,minSizeSubset,k)

import random
            
def generateRandomNumbers(numRandomNumbers,maxRandomNumber,randomSeed ):
    random.seed(randomSeed)
    listRandomIndexs = []
    while len(listRandomIndexs) < numRandomNumbers:
        randomI = random.randint(0,maxRandomNumber-1)
        if randomI not in listRandomIndexs: listRandomIndexs.append(randomI)        
    return listRandomIndexs

def sortByEfficiencyFunction(arrayOfPairs,p,w):
    allEfficiencies = np.array([])
    for pair in arrayOfPairs:
        P_ij = p[pair[0]][pair[1]]
        w_i = w[pair[0]]
        w_j = w[pair[1]]
        efficiency = P_ij/(w_i+w_j)
        allEfficiencies = np.append(allEfficiencies,efficiency)
        
    efficiencyIndex = np.argsort(-allEfficiencies)
    return efficiencyIndex

def isAnElementFromPairAlreadySelected(pairToAdd,pairsAlreadyChosen):
    indexFirstElementInPair = pairToAdd[0]
    indexSecondElementInPair = pairToAdd[1]
    
    if (indexFirstElementInPair in pairsAlreadyChosen or indexSecondElementInPair in pairsAlreadyChosen):
        return True
    else:
        return False
    
def allElementsToKnapSack(arrayOfPairs,efficiencyIndexs,v,w,W,p):
    k = len(efficiencyIndexs)
    sumWeightElementsKnapsack = 0
    indexChosenElements = []
    sumProfit = 0
    indexOfSet = []
    for i in range(0,15):
        indexOfSet.append(i)
        
    for i in range(k):
        currentLargestPair = arrayOfPairs[efficiencyIndexs[i]]
        indexFirstElementInPair = currentLargestPair[0]
        indexSecondElementInPair = currentLargestPair[1]
        w_i = w[indexFirstElementInPair]
        w_j = w[indexSecondElementInPair]
        if((sumWeightElementsKnapsack+w_i+w_j) <= W):
            if(isAnElementFromPairAlreadySelected(currentLargestPair,indexChosenElements) == False):
                indexChosenElements.append(indexFirstElementInPair)
                indexChosenElements.append(indexSecondElementInPair)
                otherV = np.take(v,list(set(indexOfSet) - set(currentLargestPair)))
                otherW = np.take(w,list(set(indexOfSet) - set(currentLargestPair)))
                sumWeightElementsKnapsack += (w_i+w_j)
                sumProfit += (v[indexFirstElementInPair] + v[indexSecondElementInPair])
                print("Adding (",currentLargestPair,",",w_i,w_j, ") to the knapsack")   
    
    remainingW = W - sumWeightElementsKnapsack
    
    print("Weight - PAIRS: ",sumWeightElementsKnapsack)
    print("Profit - PAIRS: ",sumProfit)
    
    indexofElementsInKnapsack = linearKnapSack(otherV,otherW,len(otherV) ,remainingW)
    print("Weight - linear knapsack:" , np.sum(otherW[indexofElementsInKnapsack==1]))
    print("Profit - linear knapsack:" , np.sum(otherV[indexofElementsInKnapsack==1]))
    
    print("Selected v - PAIRS:",np.take(v,indexChosenElements))  
    print("Selected v - Linear:",otherV[indexofElementsInKnapsack==1])  
    print("Selected w - PAIRS:",np.take(w,indexChosenElements))  
    print("Selected w - Linear:",otherW[indexofElementsInKnapsack==1]) 
    
    print("Selected v - all:",np.concatenate([np.take(v,indexChosenElements),otherV[indexofElementsInKnapsack==1]]))     
    
    print("Selected w - all: ",np.concatenate([np.take(w,indexChosenElements),otherW[indexofElementsInKnapsack ==1]]))
    print("Total Weight - all: ",np.sum(np.concatenate([np.take(w,indexChosenElements),otherW[indexofElementsInKnapsack ==1]])))
    print("Total Profit - all:",np.sum(np.concatenate([np.take(v,indexChosenElements),otherV[indexofElementsInKnapsack==1]])))
    
    
def problem2():
    # =============================================================================
    #     Problem 2 Quadratic Knapsack Problem
    # =============================================================================
    print("\n \n Problem 2 - Quadratic Knapsack Problem ")
    v = np.array([7, 6, 13,16, 5, 10, 9, 23, 18, 12, 9, 22, 17, 32, 8])
    w = np.array([13, 14, 14, 15, 15, 9, 26, 24, 13, 11, 9, 12, 25, 12, 26])
    W = 50
    p = np.array([
         7	,12	,7	,6	,13	,8	,11	,7	,15	,23	,14	,15	,17	,9	,15,
         12	,6	,15	,13	,10	,15	,9	,10	,8	,17	,11	,13	,12	,16	,15,
         7	,15	,13	,11	,16	,6	,8	,14	,13	,4	,14	,8	,15	,9	,16,
         6	,13	,11	,16	,10	,13	,14	,14	,17	,15	,14	,6	,24	,13	,4,
         13	,10	,16	,10	,5	,9	,7	,25	,12	,6	,6	,16	,10	,15	,14,
         8	,15	,6	,13	,9	,10	,2	,13	,12	,16	,9	,11	,23	,10	,21,
         11	,9	,8	,14	,7	,2	,9	,8	,18	,4	,13	,14	,14	,17	,15,
         7	,10	,14	,14	,25	,13	,8	,23	,9	,16	,12	,3	,14	,14	,27,
         15	,8	,13	,17	,12	,12	,18	,9	,18	,15	,16	,13	,14	,7	,17,
         23	,17	,4	,15	,6	,16	,4	,16	,15	,12	,28	,5	,19	,6	,18,
         14	,11	,14	,14	,6	,9	,13	,12	,16	,28	,9	,13	,4	,13	,16,
         15	,13	,8	,6	,16	,11	,14	,3	,13	,5	,13	,22	,11	,19	,13,
         17	,12	,15	,24	,10	,23	,14	,14	,14	,19	,4	,11	,17	,15	,12,
         9	,16	,9	,13	,15	,10	,17	,14	,7	,6	,13	,19	,15	,32	,16,
         15	,15	,16	,4	,14	,21	,15	,27	,17	,18	,16	,13	,12	,16	,8
         ])
    p = p.reshape(15,15)
    k = 7
    size = 11
    randomSeed = 100

    randomNumberIndex = generateRandomNumbers(k,size,randomSeed)
    print("Indexs for sampled items:" ,randomNumberIndex)
    arrayOfPairs = finaAllSubsets(randomNumberIndex,2,k)
    print("Pairs: ",arrayOfPairs)
    efficiencyIndexs = sortByEfficiencyFunction(arrayOfPairs,p,w)
    scoreIndex = np.argsort(efficiencyIndexs)
    allElementsToKnapSack(arrayOfPairs,scoreIndex,v,w,W,p)
    
def main():
    problem1()
    problem2() 
   
    
   

if __name__ == '__main__':
    main()
    
    
