from django import forms
from django.core.validators import RegexValidator
from govisewana.models import districts,season,month,snipet_Harvest,snipet_Demand


class HarvestForm(forms.ModelForm):
    class Meta:
        model = snipet_Harvest
        fields = ['year','district', 'season', 'area','rainfall']
        # fields = ['year','month','district', 'season', 'area','rainfall']
    
    letters=RegexValidator(r'^[a-zA-Z]*$','Only Letters are allowed')
    numbers=RegexValidator(r'^[\d*\.?\d]*$','Only Numbers are allowed')


    year = forms.CharField(validators=[numbers])  
    # month = forms.ChoiceField(choices=month)  
    district=forms.ChoiceField(choices=districts)
    season = forms.ChoiceField(choices=season)
    area = forms.CharField(max_length=100, validators=[numbers])
    rainfall = forms.CharField(max_length=100, validators=[numbers])
    

    def clean(self):
        cleaned_data = super(HarvestForm, self).clean()        
        year = cleaned_data.get('year')
        # month = cleaned_data.get('month')
        district = cleaned_data.get('district')
        season = cleaned_data.get('season')
        area = cleaned_data.get('area')
        rainfall = cleaned_data.get('rainfall')
        if not district and not season and not area and not rainfall:
            raise forms.ValidationError('Please enter all the feilds!')
            
            print ("form is not valid")
            msg = "form is not valid"
            self.add_error(msg)
       

class DemandForm(forms.ModelForm):

    class Meta:
        model = snipet_Demand
        fields = ['year','population', 'substitute', 'income']
        # fields = ['year','month','population', 'substitute', 'income']

    letters=RegexValidator(r'^[a-zA-Z]*$','Only Letters are allowed')
    numbers=RegexValidator(r'^[\d*\.?\d]*$','Only Numbers are allowed')



    year = forms.CharField(max_length=50, validators=[numbers])  
    # month = forms.ChoiceField(choices=month)
    population = forms.CharField(max_length=100, validators=[numbers])
    substitute = forms.CharField(max_length=100, validators=[numbers])
    income = forms.CharField(max_length=100, validators=[numbers])

    def clean(self):
        cleaned_data = super(DemandForm, self).clean()
        year = cleaned_data.get('year')
        # month = cleaned_data.get('month')
        population = cleaned_data.get('population')
        substitute = cleaned_data.get('substitute')
        income = cleaned_data.get('income')
        if not population and not substitute and not income:
            raise forms.ValidationError('Please enter all the feilds!')