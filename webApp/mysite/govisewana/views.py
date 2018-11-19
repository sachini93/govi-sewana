from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import random
import datetime
import time
import csv
from .Forms import HarvestForm, DemandForm
from govisewana.models import snipet_Harvest
from pandas import read_csv

from govisewana.predictions import predictions
from govisewana.distribution import distributions

from django.template.loader import render_to_string
import random

# Create your views here.
def index(request):
    # return HttpResponse("<h1>Hi</h1>")
    return render(request,'govisewana/login.html')

def home(request):
    return render(request, 'govisewana/home.html')

def harvest(request):
    return render(request, 'govisewana/Harvest.html')

def demand(request):
    return render(request, 'govisewana/demand.html')

def distribution(request):
    return render(request, 'govisewana/Distribution.html')

def aboutUs(request):
    return render(request, 'govisewana/about.html')

def contactUs(request):
    return render(request, 'govisewana/contact.html')

def login(request):
    return render(request, 'govisewana/login.html')

def register(request):
    return render(request, 'govisewana/register.html')

def data(request):
    return render(request, 'govisewana/data.html')

def error1(request):
    return render(request, 'govisewana/error1.html')

def error2(request):
    return render(request, 'govisewana/error2.html')

def dataHarvest(request):
    product=random.randint(25000,40000)
    if request.method == 'POST':
        form = HarvestForm(request.POST)
        
        if form.is_valid():
            #append data to list
            newHarvest=[]
            newHarvest.append(1)
            newHarvest.append(request.POST['district'])
            newHarvest.append(request.POST['season'])
            newHarvest.append(request.POST['year'])
            newHarvest.append(request.POST['area'])                     
            newHarvest.append(request.POST['rainfall'])
            # newHarvest.append(product)

            print(newHarvest)
            newHarvest.extend([product])
           
            #write to csv
            with open('data/harvest_raw.csv',"a") as output:
                writer = csv.writer(output,lineterminator = '\n')
                writer.writerow(newHarvest)

            return HttpResponseRedirect('runHarvestPrediction')

        else:
            form = HarvestForm()
            return HttpResponseRedirect('error-dataHarvest')

    return render(request, 'govisewana/data_Harvest.html', {'form': HarvestForm})
    
def dataDemand(request):
    consumption=random.randint(150,170)
    if request.method == 'POST':
        form = DemandForm(request.POST)
        print (form.errors)
       
        if form.is_valid():
            #append data to list
            newDemand=[]
            newDemand.append(request.POST['year'])
            newDemand.append(request.POST['population'])
            newDemand.append(request.POST['income'])
            newDemand.append(request.POST['substitute'])            
            
            print(newDemand)
            newDemand.extend([consumption])

            #write to csv
            with open('data/demand_raw.csv',"a") as output:
                writer = csv.writer(output,lineterminator = '\n')
                writer.writerow(newDemand)
               
            return HttpResponseRedirect('runDemandPrediction')

        else:
            form = DemandForm()
            print ("form is not valid")
            return HttpResponseRedirect('error-dataDemand')

    return render(request, 'govisewana/data_Demand.html', {'form': DemandForm})

def runDemand(request):
    #prediction function
    amount = predictions.demandPrediction()
    return render(request, 'govisewana/demand.html', {'predictedAmount': amount})


def runHarvest(request):
    #prediction function
    amount = predictions.harvestPrediction()
    return render(request, 'govisewana/Harvest.html', {'predictedAmount': amount})

def runDistrubution(request):
    #call ILS function
    solution,consumer,demand,fitnesScore_ILS = distributions.distribution_ILS()

    #call GA function
    fitnesScore_GA,List_GA,dem,sup = distributions.distribution_GA()

    #---------------------------ILS------------------------------------
    #get all consumers for ILS
    consumer_ILS=[]
    print(consumer)
    for i in consumer:
        consumer_ILS.append(i)

    # print("ILS- solution")
    # print(solution)

    #get all solutions for ILS
    solution_ILS=[]
    for dis in consumer:
        solution_ILS.append(solution[dis])

    #get all demands for ILS
    demand_ILS=[]
    for i in demand:
        demand_ILS.append(i)


    #---------------------------------GA------------------------------------
        
    #get all demand for GA
    demand_GA=[]
    for dis in List_GA:
        demand_GA.append(dem[dis])

    #get all solution for GA
    solution_GA=[]
    for dis in List_GA:
        solution_GA.append(sup[dis])

    # print(demand_GA)
    # print(fitnesScore_GA)
    # print(List_GA,solution_GA)
    # print("final sol")
    # print(sup)


    return render(request, 'govisewana/Distribution.html', {'solution_ILS': solution_ILS,'consumer_ILS': consumer_ILS,'demand_ILS': demand_ILS,'fitnesScore_ILS': fitnesScore_ILS,'List_GA':List_GA,'demand_GA':demand_GA,'solution_GA':solution_GA,'fitnesScore_GA':fitnesScore_GA})


# def addParameter_demand():



        