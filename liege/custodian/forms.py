from django import forms
from django.db.models import fields
from custodian.models import *


class UploadDocument(forms.Form):
    datafile = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))
