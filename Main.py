#!python
#cython: language_level=3

import random
import copy
import datetime
import timeit
import random

import threading

class beautifulSlideShowUpdate:
    initialSolution = []
    initialFitness = 0
    outputSolution = []
    outputFitness = 0
    inputForm  = []
    fileName = ""
    totalPhoto = 0
    actualSolution = []
    actualFitness = 0
    tabu_list = {}
    execution = True
    def __init__(self,_fileName):
        self.initialSolution = []
        self.inputForm = []
        self.fileName = _fileName
        self.totalPhoto = 0
        self.actualFitness = 0
        self.initialFitness = 0
        self.actualSolution = []
        self.initializeInputForm()
        self.generateInitialSolution()
        self.execution = True

    def outputToFile(self):
        file = open("d_results_"+str(datetime.datetime.now())+".out","w+")
        file.write(str(len(self.actualSolution))+"\n")
        for i in range(0,len(self.actualSolution),1):
            if isinstance(self.actualSolution[i], int):
                file.write(str(self.actualSolution[i])+"\n")
            else:
                file.write(str(self.actualSolution[i][0]) +" "+str(self.actualSolution[i][1])+"\n")
        file.close()

    def initializeInputForm(self):
        file = open(self.fileName, 'r')
        self.totalPhoto = int(file.readline())
        fileRows = filter(None,file.read().split('\n'))
        for row in fileRows:
            element = row.split(' ')
            self.inputForm.append([element[0],element[1],element[2:]])

    def generateInitialSolution(self):
        self.initialSolution = random.sample(range(0, self.totalPhoto), self.totalPhoto)
        self.portProccessingSortArray2()
        self.postProcessingInitialSolutionVerticalPhoto()
        self.portProccessingSortArray2()
        #self.postProccesingInitialSolutionToFindBestEverScore()
        #threading.Timer(300, self.stop_execution).start()
        self.postProcessingInitialSolutionHorizontalPhoto()
        #b = len(self.getPhotoTags(self.initialSolution[0]))
        #a = len(self.getPhotoTags(self.initialSolution[39999]))
        #print(a)
        #self.postProccesingInitialSolution()
        self.calculateInitialFitnes()
        self.setActualSolution(self.initialSolution,self.initialFitness)
    def stop_execution(self):
        self.execution = False

    def portProccessingSortArray(self):
        self.initialSolution.sort(key=lambda x: self.sortSecond(x), reverse=False)

    def portProccessingSortArray2(self):
        self.initialSolution.sort(key=lambda x: self.sortSecond(x), reverse=True)

    def sortSecond(self,val):
       return len(self.getPhotoTags(val))

    def postProccesingInitialSolutionToFindBestEverScore(self):
        for i in range(0,len(self.initialSolution)-1,1):
            print(i)
            if self.checkIfPhotosHasTagsInCommon(self.initialSolution[i],self.initialSolution[i+1]):
                continue
            else:
                tmp = self.findNextHorizontalPhotoThatHasTagsInCommon(i)
                if tmp != -1:
                    self.initialSolution[i+1],self.initialSolution[tmp] = self.initialSolution[tmp],self.initialSolution[i+1]
                else:
                    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<    ",i,"    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def findNextHorizontalPhotoThatHasTagsInCommon(self,position):
        for i in range(position+1,len(self.initialSolution),1):
            if self.checkIfPhotosHasTagsInCommon(self.initialSolution[position],self.initialSolution[i]):
                return i
        return -1

    def checkIfPhotosHasTagsInCommon(self,photo_1,photo_2):
        tagsPhoto_1 = self.getPhotoTags(photo_1)
        tagsPhoto_2 = self.getPhotoTags(photo_2)
        return not set(tagsPhoto_1).isdisjoint(tagsPhoto_2)

    def postProccesingInitialSolutionOldOne(self):
        for i in range(0,len(self.initialSolution),1):
            if len(self.initialSolution) > i:
                if self.getPhotoPosition(self.initialSolution[i]) == 'V':
                    photoToCombine = self.findNextVerticalPhoto(i)
                    if photoToCombine == None:
                        continue
                    self.initialSolution[i] = [self.initialSolution[i],photoToCombine]
                    self.initialSolution.remove(photoToCombine)
                if self.getPhotoPosition(self.initialSolution[i]) == 'H':
                    scoreBetweenSlides = self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[i]),self.getPhotoTags(self.initialSolution[i+1]))
                    a = i+1
                    while scoreBetweenSlides == 0  and a < 59000:
                        self.initialSolution[i+1],self.initialSolution[a+1] = self.initialSolution[a+1],self.initialSolution[i+1]
                        scoreBetweenSlides = self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[i]),
                                                                             self.getPhotoTags(self.initialSolution[i+1]))
                        a = a + 1
                    #photoPositionToSwap = self.findNextHorizontalPhoto(i)
                    #if photoPositionToSwap != None:
                    #    self.initialSolution[i+1],self.initialSolution[photoPositionToSwap] = self.initialSolution[photoPositionToSwap] ,self.initialSolution[i+1]
            else:
                break


    def postProcessingInitialSolutionHorizontalPhoto(self):
        for i in range(0,len(self.initialSolution)-1,1):
            if not self.execution:
                break
            print(i)
            photo1Tags = self.getPhotoTags(self.initialSolution[i])
            #scoreBetweenSlides = self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[i]),self.getPhotoTags(self.initialSolution[i+1]))
            scoreBetweenSlides = self.getMinimumBetweenTwoPhotos(photo1Tags,self.getPhotoTags(self.initialSolution[i+1]))
            bestScore = self.getBestScore(i)
            a = copy.copy(i) + 1
            tmpBest = copy.copy(scoreBetweenSlides)
            tmpPosition = copy.copy(i)+ 1
            while scoreBetweenSlides <  bestScore  and a < len(self.initialSolution)-1:
                a = a + 1
                scoreBetweenSlides = self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[i]),self.getPhotoTags(self.initialSolution[a]))
                if scoreBetweenSlides > tmpBest:
                    tmpBest = copy.copy(scoreBetweenSlides)
                    tmpPosition = copy.copy(a)

            if a > i + 1 and a < len(self.initialSolution)-1:
                print("Best score: ",bestScore ,"  FOUND ....",scoreBetweenSlides)
                self.initialSolution[i + 1], self.initialSolution[a] = self.initialSolution[a],self.initialSolution[i + 1]
                continue
            elif a >= len(self.initialSolution)-1:
                print("Best score: ",bestScore ,"  FOUND ....",tmpBest)
                self.initialSolution[i + 1], self.initialSolution[tmpPosition] = self.initialSolution[tmpPosition],self.initialSolution[i + 1]


    def getBestScore(self,i):
        #if i < 50:
        #    return 17
        #elif i < 100:
        #    return 16
        #elif i<200:
        #    return 15
        #elif i < 300:
        #    return 14
        #elif i< 1500:
        #    return 12
        if i< 10000:
            return 10
        elif i < 15000:
            return 9
        elif i < 20000:
            return 8
        elif i < 25000:
            return 7
        elif i< 30000:
            return 6
        elif i< 35000:
            return 5
        elif i< 40000:
            return 4
        elif i < 45000:
            return 3
        else:
            return 2

    def getBestScore2(self,i):
        if i < 180:
            return 13
        elif i < 270:
            return 12
        elif i < 950:
            return 11
        elif i < 1900:
            return 10
        elif i < 14000:
            return 10
        elif i < 18000:
            return 9
        elif i < 23000:
            return 8
        elif i < 28000:
            return 7
        elif i < 34000:
            return 6
        else:
            return 5

    def postProcessingInitialSolutionVerticalPhoto(self):
        try:
            for i in range(0,len(self.initialSolution),1):
                if self.getPhotoPosition(self.initialSolution[i]) == 'V':
                    photoToCombine = self.findNextVerticalPhoto(i)
                    if photoToCombine == None:
                        photoToCombine = self.findNextVerticalPhotoRandom(i)
                    self.initialSolution[i] = [self.initialSolution[i],photoToCombine]
                    self.initialSolution.remove(photoToCombine)
        except:
            return

    def getPhotoPosition(self,element):
        #print(element)
        if isinstance(element,int):
            return self.inputForm[element][0]
        return "VV"

    def findNextVerticalPhoto(self,position):
        bestN = 1000
        bestPosition = 0
        try:
            #for i in range(position + 1,len(self.initialSolution), 1):
            for i in range(len(self.initialSolution)-1,position, -1):
                if (self.getPhotoPosition(self.initialSolution[i]) == 'V'):
                    score = self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[i]),
                                                    self.getPhotoTags(self.initialSolution[position]))
                    if score <= bestN:
                        bestPosition = copy.copy(self.initialSolution[i])
                        bestN = copy.copy(score)

                    if score > 0 and i <= len(self.initialSolution):
                        continue
                    return self.initialSolution[i]

            if bestN != 1000:
                return bestPosition
        except:
            return

    def findNextVerticalPhotoRandom(self,position):
        for i in range(position + 1, len(self.initialSolution), 1):
            if (self.getPhotoPosition(self.initialSolution[i]) == 'V'):
                return self.initialSolution[i]

    def findNextHorizontalPhoto(self,position):
        for i in range(position + 1, len(self.initialSolution), 1):
            if len(self.initialSolution) > i:
                if (self.getPhotoPosition(self.initialSolution[i]) == 'H'):
                    return self.initialSolution[i]
            else:
                break
        return None

    def setActualSolution(self,_solution,_fitnes):
        self.actualSolution = copy.copy(_solution)
        self.actualFitness  = copy.copy(_fitnes)

    def calculateInitialFitnes(self):
        for i in range(0,len(self.initialSolution)-1,1):
            count =  self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[i]),self.getPhotoTags(self.initialSolution[i+1]))
            self.initialFitness = self.initialFitness +count
            if count == 0:
                print(i)

    def calculateSolutionfitness(self,solution):
        fitnes = 0
        for i in range(0,len(solution)-1,1):
            fitnes = fitnes + self.getMinimumBetweenTwoPhotos(self.getPhotoTags(solution[i]),self.getPhotoTags(solution[i+1]))
        return fitnes

    def getMinimumBetweenTwoPhotos(self,photo1,photo2):
        countTagsOnlyPhoto1 = self.getTotalDifferentTags(photo1, photo2)
        countTagsOnlyPhoto2 = self.getTotalDifferentTags(photo2, photo1)
        countSameTags = len(photo1) - countTagsOnlyPhoto1
        return min(countTagsOnlyPhoto1, countTagsOnlyPhoto2, countSameTags)

    def getTotalDifferentTags(self,photoTags1,photoTags2):
        return len(set(photoTags1) - set(photoTags2))


    def getPhotoTags(self,position):
        if isinstance(position, int):
            return self.inputForm[position][2]
        else:
            return self.combineTags(self.inputForm[position[0]][2],self.inputForm[position[1]][2])

    def getPhotoTags2(self,position):
        if position >= len(self.actualSolution):
            return  []
        if isinstance(self.actualSolution[position], int):
            if position < 0 or position >= len(self.initialSolution):
                return []
            return self.inputForm[self.actualSolution[position]][2]
        else:
            return self.combineTags(self.inputForm[self.actualSolution[position][0]][2],self.inputForm[self.actualSolution[position][1]][2])

    def combineTags(self,photoTag1,photoTag2):
        return list(set(photoTag1) | set(photoTag2))

    def testFunction(self):
        print(self.actualSolution)
        s = self.calculateSolutionfitness(self.actualSolution)
        print(s)

    def generateNeighborhood(self):
        j = 1
        for j in range(1,2,1):
            for i in range(1,200000,1):
                rndTmp = random.sample(range(500, len(self.actualSolution)), j*2)
                #rndTmp = self.get_two_numbers()
                val = copy.copy(self.actualFitness)
                #tmp = copy.copy(self.actualSolution)
                for s in range(0,len(rndTmp),2):
                    #x,y = self.get_two_numbers()
                    x = rndTmp[s]
                    y = rndTmp[s+1]
                    #tmp[x], tmp[y] = tmp[y], tmp[x]
                    val= self.calculateNeighborhoodFitnessVal(val,x, y)

                    #if (val > self.actualFitness):
                    #    self.actualFitness = copy.copy(val)
                    #    self.actualSolution = copy.copy(tmp)
                    #else:
                    #    if self.helper_get_numbers(x) in self.tabu_list:
                    #        self.tabu_list[self.helper_get_numbers(x)].add(self.helper_get_numbers(y))
                    #    else:
                    #        self.tabu_list[self.helper_get_numbers(x)] = {self.helper_get_numbers(y)}
                if(val >= self.actualFitness):
                    self.actualFitness = copy.copy(val)
                    self.actualSolution[x],self.actualSolution[y] = self.actualSolution[y],self.actualSolution[x]# copy.copy(tmp)

    def get_two_numbers(self):
        rndTmp = random.sample(range(0, len(self.actualSolution)), 2)
        x = rndTmp[0]
        y = rndTmp[1]
        position_x = self.helper_get_numbers(x)
        position_y = self.helper_get_numbers(y)
        tmp_value = 0
        if position_x in self.tabu_list:
            while position_y not in self.tabu_list[position_x] and x != y and  tmp_value < 500:
                y = random.sample(range(0, len(self.actualSolution)), 1)
                position_y = self.helper_get_numbers(y[0])
                tmp_value = tmp_value + 1
        if not isinstance(x,int):
            x = x[0]
        if not isinstance(y,int):
            y = y[0]
        return x,y

    def helper_get_numbers(self,position):
        if isinstance(self.actualSolution[position],int):
            return self.actualSolution[position]
        else:
            return self.actualSolution[position][0]

    def calculateNeighborhoodFitness2(self,x,y):
        return  self.actualFitness  -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[x-1]),self.getPhotoTags(self.initialSolution[x]))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[x]),self.getPhotoTags(self.initialSolution[x+1]))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[y-1]),self.getPhotoTags(self.initialSolution[x]))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[x]),self.getPhotoTags(self.initialSolution[y+1]))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[y-1]),self.getPhotoTags(self.initialSolution[y]))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[y]),self.getPhotoTags(self.initialSolution[y+1]))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[x-1]),self.getPhotoTags(self.initialSolution[y]))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[y]),self.getPhotoTags(self.initialSolution[x+1]))

    def calculateNeighborhoodFitness(self,x,y):
        return  self.actualFitness  -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(x))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(x+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(x))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(y+1))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(y))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y),self.getPhotoTags2(y+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(y))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y),self.getPhotoTags2(x+1))


    def calculateNeighborhoodFitnessVal(self,actualFitnes,x,y):
        return  actualFitnes  -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(x))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(x+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(x))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(y+1))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(y))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y),self.getPhotoTags2(y+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(y))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y),self.getPhotoTags2(x+1))

    def calculateNeighborhoodFitnessValNew(self,x,y):
        return  0  -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(x))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(x+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(x))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(y+1))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(y))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y),self.getPhotoTags2(y+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(x+1))    \




import copy
import datetime
import random

if __name__ == "__main__":
    #file = "/home/blend/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/d_pet_pictures.txt"
    #file = "/home/blend/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/qualification_round_2019.in/c_memorable_moments.txt"
    #file = "/home/blend/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/qualification_round_2019.in/d_pet_pictures.txt"
    #file = "/home/blend/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/qualification_round_2019.in/e_shiny_selfies.txt"
    #file = "/home/blend/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/qualification_round_2019.in/b_lovely_landscapes.txt"

    file = "/home/blend/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/qualification_round_2019.in/d_pet_pictures.txt"
    tmp = beautifulSlideShowUpdate(file)
    print(tmp.initialSolution)
    print(tmp.initialFitness)
    tmp.generateNeighborhood()
    tmp.outputToFile()
    print(tmp.calculateSolutionfitness(tmp.actualSolution))
    print(tmp.actualFitness)

























