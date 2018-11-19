from django.db import models

districts = (
        ('Anuradapura', 'Anuradapura'),
        ## current data set for anuradhapura
        # ('Kurunegala', 'Kurunegala'),
        # ('Gampaha', 'Gampaha'),
        # ('Matara', 'Matara'),
        # ('Polonnaruwa', 'Polonnaruwa'),
)

season=(
    ('Yala-Season','Yala-Season'),
    ('Maha-Season','Maha-Season'),
)

month=(
    (1,"January"),
    (2,"February"),
    (3,"March"),
    (4,"April"),
    (5,"May"),
    (6,"June"),
    (7,"July"),
    (8,"August"),
    (9,"September"),
    (10,"October"),
    (11,"November"),
    (12,"December")        
)

class snipet_Harvest(models.Model):
    year=models.CharField(max_length=4)
    # month=models.IntegerField(choices=month)
    districts = models.CharField(max_length=50, choices=districts)
    season = models.CharField(max_length=50,choices=season)
    area = models.CharField(max_length=50)
    rainfall = models.CharField(max_length=50)


class snipet_Demand(models.Model):
    year=models.CharField(max_length=4)
    # month=models.IntegerField(choices=month)
    population = models.CharField(max_length=50)
    substitute = models.CharField(max_length=50)
    income = models.CharField(max_length=50)


