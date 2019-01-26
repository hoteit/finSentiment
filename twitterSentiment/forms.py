__author__ = 'tarek'
from django import forms
from django.forms import ModelForm
from twitterSentiment.models import TwitterText

class CompaniesImport(forms.Form):
	companiesList = forms.CharField( widget=forms.Textarea(attrs={'rows': 20, 'cols': 30}))

CHOICES = (('0', 'very negative',), ('1', 'negative'), ('2', 'neutral'), ('3', 'positive'), ('4', 'very positive'))

class TrainingDatumForm(ModelForm):
	class Meta:
		model = TwitterText
		fields = ('twitter_sentiment',)
		widgets = {
			'twitter_sentiment': forms.RadioSelect(choices=CHOICES),
		}




