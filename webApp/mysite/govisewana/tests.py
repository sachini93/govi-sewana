from django.test import TestCase

# Create your tests here.

from govisewana.models import snipet_Harvest,snipet_Demand

#Test case for testing the data entry forms
class AddDataFormTestCase(TestCase):
    #initialize testing data
    def setUp(self):
        snipet_Harvest.objects.create(year="2018", districts="ANURADHAPURA",season="Yala",area="40000",rainfall="35")
        snipet_Demand.objects.create(year="2018", population="35000",substitute="4",income="29000")

    #testcase for check year is in a valid range
    def test_year_is_continues(self):
        """ year enterd is a valid year """
        harvestYear = snipet_Harvest.objects.get(year="2018")
        demandYear = snipet_Demand.objects.get(year="2018")

        self.assertTrue(1989 <= int(harvestYear.year) <= 2020)
        self.assertTrue(1989 <= int(demandYear.year) <= 2020)

    #testcase for check district is valid
    def test_districts_enterd_are_valid(self):
        """ district enterd is a valid district """
        districtHarvest = snipet_Harvest.objects.get(year="2018")
        # districtDemand = snipet_Demand.objects.get(district="Colombo")

        suppliers=["ANURADHAPURA","POLONNARUWA","KURUNAGALA"]
        self.assertTrue(districtHarvest.districts in suppliers)

    #testcase for check area is valid
    def test_area_enterd_is_valid(self):
        """ area enterd is a valid """
        areaHarvest = snipet_Harvest.objects.get(year="2018")

        self.assertTrue(0 <= int(areaHarvest.area))

    #testcase for check rainfall is valid
    def test_rainfall_enterd_is_valid(self):
        """ rainfall enterd is a valid """
        rainfallHarvest = snipet_Harvest.objects.get(year="2018")

        self.assertTrue(0 <= int(rainfallHarvest.rainfall))

    #testcase for check population is valid
    def test_population_enterd_is_valid(self):
        """ population enterd is a valid """
        popDemand = snipet_Demand.objects.get(year="2018")

        self.assertTrue(0 <= int(popDemand.population))

    #testcase for check substitute amount is valid
    def test_substitute_enterd_is_valid(self):
        """ substitute enterd is a valid """
        subDemand = snipet_Demand.objects.get(year="2018")

        self.assertTrue(0 <= int(subDemand.substitute))

    #testcase for check income is valid
    def test_income_enterd_is_valid(self):
        """ income enterd is a valid """
        incomeDemand = snipet_Demand.objects.get(year="2018")

        self.assertTrue(0 <= int(incomeDemand.income))
 
        