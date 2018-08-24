# -*- coding: utf-8 -*-
import numpy as np
def printArray(v,w,n):
  print("******Possible Items*******")
  print("{",end="")
  for i in range(n):
      if(i == n-1):
          print("(",v[i],",",w[i],")",end="")        
      else:
          print("(",v[i],",",w[i],"),",end="")
  print("}") 
  print("***************************")

def calculateScore(v,w,n):
    score = np.array([])
    for i in range(n):
        score = np.append(score,round((v[i]/w[i]),3)) 
#    print("Scores: " ,score,"\n")
#    print("Index of elements if they were sorted in descending order:");
    scoreIndexs = np.argsort(-score)
# see   print(scoreIndexs)
#    print("***************************")
    
    return scoreIndexs

def linearKnapSack(v,w,n,W,shouldPrint=False):
    sumItemsInKnapsack = 0
    
    if(shouldPrint):
        printArray(v,w,n)
        
    scoreIndexs =  calculateScore(v,w,n)
    indexofElementsInKnapsack = np.zeros(n)
    
    for i in range(n):
       indexOfLargestElement = scoreIndexs[i]
       if((sumItemsInKnapsack+w[indexOfLargestElement]) <= W ):
           indexofElementsInKnapsack[indexOfLargestElement] = 1 
           sumItemsInKnapsack += w[indexOfLargestElement]
           if(shouldPrint):
               print("Adding (",v[indexOfLargestElement],",",w[indexOfLargestElement], ") to the knapsack")    
    

        
    print("Profit - linear knapsack:" , np.sum(v[indexofElementsInKnapsack==1]))
    print("Weight - linear knapsack:" , np.sum(w[indexofElementsInKnapsack==1]))
    
    if(shouldPrint):
        print("***************************")
        print("Arrays: ")
        print("v_i = {0}".format(v))
        print("w_i = {0}".format(w))
        print("x_i = {0}".format(indexofElementsInKnapsack))
        
    return indexofElementsInKnapsack

    
def findSubsets(allSubsets,subset,currentIndex,minSizeSubset,k):      
    if(len(subset) == currentIndex):
        return allSubsets
    
    newSet = []
    for i in range(0,len(allSubsets)):
      if(len(allSubsets[i]) < k):
        newSet = allSubsets[i].copy()
        newSet.append(subset[currentIndex])
        allSubsets.append(newSet)
#        print(allSubsets)
        
    findSubsets(allSubsets, subset, currentIndex+1,minSizeSubset,k)

def isLargerThanCapicity(chosenW,W):
      sumWeights = np.sum(chosenW)
      if(sumWeights > W):
          return True
      else:
          return False

def PTAS(v,w,n,W,minSizeSubset,k):
    allSubsets = [[]]
    indexOfSet = []
    for i in range(0,28):
        indexOfSet.append(i)
        
    findSubsets(allSubsets,indexOfSet,0,0,k)
    allSubsetsNumpy = np.array(allSubsets)
    highestProfit = 0
    bestSetIndex = []
    bestLinearIndex = []
    for sets in allSubsetsNumpy:
        if(len(sets) >= minSizeSubset):
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
                print("Weight - PTAS: ",sumWeights)
                print("Profit - PTAS: ",sumProfitPTAS)
                print("Total Profit: ",totalProfit)
                print("***************************")
                if(totalProfit >highestProfit ):
                    highestProfit = totalProfit
                    bestSetIndex = sets
                    bestLinearIndex = indexofElementsInKnapsack
    
    bestLinearIndexValues = np.where(bestLinearIndex==1)
    print("HighestProfit",highestProfit)
    print("Best Indexs for PTAS:",bestSetIndex)  
    print("Selected v - PTAS:",np.take(v,bestSetIndex))  
    print("Selected v - Linear:",np.take(otherV,bestLinearIndexValues)[0])  
    print("Selected v - all:",np.concatenate([np.take(v,bestSetIndex),np.take(otherV,bestLinearIndexValues)[0]]))                                                                 

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
    #    print("Problem 1 - Greedy Algorithm ")
    #    linearKnapSack(v,w,n,W)
    
    # =============================================================================
    #     Linear Knapsack Problem - PTAS
    # =============================================================================
    #    print("\n \n Problem 1 - Polynomial Time Approximation Algorithm (PTAS) ")
    #    minSizeSubset = 3
    #    k = 10
    #    PTAS(v,w,n,W,minSizeSubset,k)

import random
 
#def sampleKItems(k)  
def getAllPairsForSample(sampleArrayIndexs):
    allSubsets = [[]]
    subsetOfPairs = []
    subsetSize= 2
    findSubsets(allSubsets,sampleArrayIndexs,0,0,2)
    for sets in allSubsets:
        if(len(sets) == subsetSize):
            subsetOfPairs.append(sets)
            
    print("Pairs: ",subsetOfPairs)
    
def generateRandomNumbers(numRandomNumbers,maxRandomNumber ):
    random.seed(42)
    listRandomIndexs = []
    while len(listRandomIndexs) < numRandomNumbers:
        randomI = random.randint(0,maxRandomNumber-1)
        if randomI not in listRandomIndexs: listRandomIndexs.append(randomI)        
    return listRandomIndexs
    
def problem2():
    # =============================================================================
    #     Problem 2 Quadratic Knapsack Problem
    # =============================================================================
    print("Problem 2 - Quadratic Knapsack Problem ")
    v = [7, 6, 13,16, 5, 10, 9, 23, 18, 12, 9, 22, 17, 32, 8]
    w = [13, 14, 14, 15, 15, 9, 26, 24, 13, 11, 9, 12, 25, 12, 26]
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
#    print(p.reshape(15,15))
    k = 7
    size = 15
    randomNumberIndex = generateRandomNumbers(k,size)
    print("Indexs for sampled items:" ,randomNumberIndex)
    getAllPairsForSample(randomNumberIndex)

def main():
    problem2() 
   
    
   

if __name__ == '__main__':
    main()
    
    
