import itertools
import random
# import googlemaps
import csv

class distributions:
    #################################### distribution ILS ###############################################

    def distribution_ILS():
        # gmaps = googlemaps.Client(key="")

        # Geocoding an address
        # geocode_result = gmaps.distance_matrix('Anuradhapura', 'Gampaha')
        # print(geocode_result)


        def getDemandList(demand, randomchoice):
            temp = []
            for item in randomchoice:
                temp.append(demand[item])
            return temp


        def getSupplyList(supply, district, randomChoice):
            temp = []
            for item in randomChoice:
                temp.append(supply[district[item]])
            return temp


        def getValuesDict(randomDict, randomDemand):
            temp = {}
            for key in randomDemand.keys():
                pass

        
        #get best solution(calculate fitness value)
        def getBestSolution(randomChoiceDict, randomChoiceDemand, districtDict):
            print("*****************************************************************************************")
            solutions = []
            # print(f'randomChoiceDict : {randomChoiceDict}')
            # print(f"randomChoiceDemand : {randomChoiceDemand}")
            # print(f"districtDict : {districtDict}")
            # print(f"list(randomChoiceDemand.values()) : {list(randomChoiceDemand.values())}")
            # print(f"list(randomChoiceDict.values()) : {list(randomChoiceDict.values())}")
            maxValue = getProducerList(list(randomChoiceDemand.values()), list(randomChoiceDict.values()))
            # print(f"maxValue : {maxValue}")

            # demandTempList = []
            # for key in randomChoiceDemand.keys():
            #     demandTempList.append(randomChoiceDict[districtDict[key]])

            demandTempDict = dict(zip(list(randomChoiceDemand.keys()), list(randomChoiceDict.values())))
            solutions.append(demandTempDict)
            # print(f"solutions : {solutions}")

            #local search
            if len(randomChoiceDict) > 1:
                for x in range(2, len(randomChoiceDict) + 1):
                    # print(f"x : {x}")
                    for item in list(itertools.permutations(list(randomChoiceDemand.keys()), x)):
                        # print(f"item : {item}")
                        tempValues = list(item)
                        tempDict = dict(zip(list(randomChoiceDemand.keys()), list(randomChoiceDict.values())))
                        # print(f"tempDict : {tempDict}")
                        # print(f"tempValues : {tempValues}")
                        # print(f"randomChoiceDemand : {randomChoiceDemand}")
                        # print(f"randomChoiceDict : {randomChoiceDict}")
                        for key in tempValues[:-1]:
                            # print(f"key : {key}")
                            tempDict[tempValues[-1]] = tempDict[tempValues[-1]] + tempDict[key]
                            tempDict[key] = 0
                        # print(f"final -----------------------------> {tempDict}")
                        getValue = getProducerList(list(randomChoiceDemand.values()), list(tempDict.values()))
                        # print(f"getValue : {getValue}")
                        if (maxValue == getValue):
                            solutions.append(tempDict)
                        if (maxValue < getValue):
                            maxValue = getValue
                            solutions.clear()
                            solutions.append(tempDict)

            # print(f"solutions : {solutions}")
            randomSolution = random.choice(solutions)

            # for cons in consumer:
            #     # print(f"\t\t\t\t {cons}", end='')

            # # print("\nDemand", end='')

            # for dem in demand:
            #     # print(f"\t\t\t\t {dem}", end='')

            # # print(f"\nSolution", end='')

            # for cons in consumer:
            #     # print(f"\t\t\t\t {randomSolution[cons]}", end='')

            # # print(f"\nFitness Value : {maxValue}")
            return randomSolution,maxValue

        #compare demand and supply
        def getProducerList(demand, randomChoiceSupply):
            # print("=============================================")
            # print(f"demand : {demand}")
            # print(f"randomChoiceSupply : {randomChoiceSupply}")
            temp = 0.0
            for x in range(len(supply)):
                if (demand[x] == randomChoiceSupply[x]):
                    temp = temp + 1
                if (demand[x] < randomChoiceSupply[x]):
                    temp = temp + 0.5
                if (demand[x] > randomChoiceSupply[x]):
                    temp = temp + 0
            # print(f"temp : {temp}")
            # print("=============================================")
            return temp


        # def getproducermoisture(moisture):
        #     initMmistureValue, temp = 13, 0.0
        #     for item in moisture:
        #         if (item == initMmistureValue):
        #             temp = temp + 1.0
        #         if (item < initMmistureValue):
        #             temp = temp + 0.5
        #         if (item > initMmistureValue):
        #             temp = temp + 0.0
        #     return temp


        # details according to district(read from csv file)
        producer, consumer, supply, demand = [], [], [], []
        csvCount = 0
        with open('data/db_ILS.csv', mode='r') as db:
            for row in csv.reader(db):
                if csvCount != 0 and row != []:
                    producer.append(row[1])
                    supply.append(float(row[2]))
                    consumer.append(row[3])
                    demand.append(float(row[4]))
                csvCount += 1

        conSupDict = dict(zip(producer, supply))
        conDemDict = dict(zip(consumer, demand))
        districtDict = dict(zip(consumer, producer))
        # print(f"conSupDict : {conSupDict}")
        # print(f"conDemDict : {conDemDict}")
        # print(f"districtDict : {districtDict}")

        # get all the possibilities from the consumer list
        allPossibilities = [list(row) for row in itertools.permutations(consumer)]
        # print(f"allPossibilities : {allPossibilities}")

        # select one random choice from the all possibilities
        randomChoice = random.choice(allPossibilities)
        # print(f"randomChoice : {randomChoice}")

        # get supply for randomly choice district
        randomChoiceSupply = getSupplyList(conSupDict, districtDict, randomChoice)
        # print(f"randomChoiceSupply : {randomChoiceSupply}")

        # get demand for randomly chice districts
        randomChoiceDemand = getDemandList(conDemDict, randomChoice)
        # print(f"randomChoiceDemand : {randomChoiceDemand}")

        producer.clear()
        for key in randomChoice:
            producer.append(districtDict[key])

        randomChoiceDict = dict(zip(producer, randomChoiceSupply))
        # print(f"randomChoiceDict : {randomChoiceDict}")

        randomChoiceDemandDict = dict(zip(randomChoice, randomChoiceDemand))
        # print(f"randomChoiceDemandDict : {randomChoiceDemandDict}")

        randomSolution,maxValue = getBestSolution(randomChoiceDict, randomChoiceDemandDict, districtDict)
        
        return randomSolution,consumer,demand,maxValue


    #################################### distribution GA ###############################################
    def distribution_GA():

        def getDemandSupplylist(condemdic, randomchoice):
            temp = []
            for item in randomchoice:
                temp.append(condemdic[item])
            return temp


        def getBestFits(solutions):
            firstFit, firstFitValue, secondFit, secondFitValue, count = [], 0.0, [], 0.0, 0
            for c in solutions:
                if count == 0:
                    firstFit, firstFitValue = c["district"], c["maxValue"]
                elif firstFitValue < c["maxValue"]:
                    secondFit, secondFitValue, firstFit, firstFitValue = firstFit, firstFitValue, c["district"], c["maxValue"]
                elif secondFitValue < c["maxValue"]:
                    secondFitValue, secondFit = c["maxValue"], c["district"]
                count = count + 1
            return firstFit, firstFitValue, secondFit, secondFitValue

            

        def crossOver(ffSupply, ffDemand, ff, sfSupply, sfDemand, sf):
            tempFFSupply= ffSupply[:dividePoint] + sfSupply[dividePoint:]
            tempFFDemand = ffDemand[:dividePoint] + sfDemand[dividePoint:]
            tempFF = ff[:dividePoint] + sf[dividePoint:]
            tempSFSupply = sfSupply[:dividePoint] + ffSupply[dividePoint:]
            tempSFDemand = sfDemand[:dividePoint] + ffDemand[dividePoint:]
            tempSF = sf[:dividePoint] + ff[dividePoint:]
            return tempFFSupply, tempFFDemand, tempFF, tempSFSupply, tempSFDemand, tempSF


        def getBestSolutions(randomchoicedict, randomChoiceDemand):
            maxValue = getProducerList(randomChoiceDemand, list(randomchoicedict.values()))
            solutions.append({"district": list(randomChoiceDict.keys()), "maxValue": maxValue})
            


        def finalSolution(solution, ffValue, ffList, conSupDict, conDemDict):
            for sol in solution:
                if sol["maxValue"] > ffValue:
                    ffValue = sol["maxValue"]
                    ffList = sol["district"]
            print(" ")
            print("First Fitness Value : " + str(ffValue))
            print("First Fitness Disctricts : ")
            print(list(distr for distr in ffList))
            print("Supply : ")
            print(list(conSupDict[distr] for distr in ffList))
            print("Demand : ")
            print(list(conDemDict[distr] for distr in ffList))
            return ffValue,ffList


        def getProducerList(randomDemandValue, randomchoice):
            temp = 0.0
            for x in range(len(randomchoice)):
                if (randomDemandValue[x] == randomchoice[x]):
                    temp = temp + 1.0
                if (randomDemandValue[x] > randomchoice[x]):
                    temp = temp + 0.0
                if (randomDemandValue[x] < randomchoice[x]):
                    temp = temp + 0.5
            return temp
                

        # details according to district
        producer, consumer, supply, demand = [], [], [], []
        csvCount = 0
        with open('data/db_GA.csv', mode='r') as db:
            for row in csv.reader(db):
                if csvCount != 0:
                    producer.append(row[1])
                    supply.append(float(row[2]))
                    consumer.append(row[3])
                    demand.append(float(row[4]))
                csvCount += 1

        conSupDict = dict(zip(consumer, supply))
        conDemDict = dict(zip(consumer, demand))
        proSupDict = dict(zip(producer,supply))
        #print("Producer and Supply")
        #print(proSupDict)
        #print("Consumers and demand")
        #print(conDemDict)
        solutions = []
        dividePoint = 1

        # get all the possibilities from the consumer list
        allPossibilities = [list(row) for row in itertools.permutations(consumer)]
        #print(" ")
        #print("allPossibilities")
        #print(" ")
        #print(allPossibilities)
        #print(" ")
        #print("oneByOnePosibilities")
        #print(" ")
        for oneByOnePosibilities in allPossibilities:
            #print(oneByOnePosibilities)
            #print(oneByOnePosibilities)
            randomChoiceSupply = getDemandSupplylist(conSupDict, oneByOnePosibilities)
            randomChoiceDemand = getDemandSupplylist(conDemDict, oneByOnePosibilities)
            randomChoiceDict = dict(zip(oneByOnePosibilities, randomChoiceSupply))
            getBestSolutions(randomChoiceDict, randomChoiceDemand)
            

        firstFit, firstFitValue, secondFit, secondFitValue = getBestFits(solutions)
        #print(" ")
        #print("Solutions with fitness value")
        #for sol in solutions:
            #print(sol)

        solutions.clear()
        firstFitSupply, firstFitDemand = getDemandSupplylist(conSupDict, firstFit), getDemandSupplylist(conDemDict, firstFit)
        secondFitSupply, secondFitDemand = getDemandSupplylist(conSupDict, secondFit), getDemandSupplylist(conDemDict, secondFit)
        fFSupply, fFDemand, fF, sFSupply, sFDemand, sF = crossOver(firstFitSupply, firstFitDemand, firstFit, secondFitSupply, secondFitDemand, secondFit)
        firstDict, secondDict = dict(zip(fF, fFSupply)), dict(zip(sF, sFSupply))
        getBestSolutions(firstDict, firstFitDemand)
        getBestSolutions(secondDict, secondFitDemand)
        maxValue,List_GA = finalSolution(solutions, firstFitValue, firstFit, conSupDict, conDemDict)

        return maxValue,List_GA,conDemDict,conSupDict

