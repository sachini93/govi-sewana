from django.urls import path, include
from . import views

urlpatterns=[
    path('api-auth/', include('rest_framework.urls')),
    path('', views.index, name='index'),
    path('home.html', views.home, name='home'),
    path('Harvest.html', views.harvest, name='harvest'),
    path('demand.html', views.demand, name='demand'),
    path('Distribution.html', views.distribution, name='distribution'),
    path('about.html', views.aboutUs, name='aboutUs'),
    path('contact.html', views.contactUs, name='contactUs'),
    path('login.html', views.login, name='login'),
    path('register.html', views.register, name='register'),
    path('data.html', views.data, name='data'),
    path('dataHarvest', views.dataHarvest, name='dataHarvest'),
    path('dataDemand', views.dataDemand, name='dataDemand'),
    path('error-dataHarvest', views.error1, name='error1'),
    path('error-dataDemand', views.error2, name='error2'),
    path('runDemandPrediction', views.runDemand, name='runDemand'),
    path('runHarvestPrediction', views.runHarvest, name='runHarvest'),
    path('runDistribution', views.runDistrubution, name='runDistrubution'),
    # path('addParameter_demand.html', views.addParameter_demand, name='addParameter_demand'),
    # path('addParameter_harvest', views.addParameter_harvest, name='addParameter_harvest'),

    # path('/contact/thanks/', views.index, name='index'),
    # # path('chart.html', views.chart1, name='chart1'),
    # path('chart/data', ListUsers.as_view(), name='chart2')
]

