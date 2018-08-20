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
#     np.concatenate([a,b])
                                                 
            
        
def main():
    n = 28
    v = np.array([2,6,8,7,3,4,6,5,10,9,8,11,12,15,6,8,13,14,15,16,13,14,15,26,13,9,25,26])
    w = np.array([7,3,3,5,4,7,5,4,15,10,17,3,6,11,6,14,4,8,9,10,14,17,9,24,11,17,12,14])
    W = 30
    
#    print("Problem 1 - Greedy Algorithm ",)
#    linearKnapSack(v,w,n,W)
    print("\n \n Problem 2 - Polynomial Time Approximation Algorithm (PTAS) ")
    minSizeSubset = 3
    k = 10
    PTAS(v,w,n,W,minSizeSubset,k)

if __name__ == '__main__':
    main()
    
    
