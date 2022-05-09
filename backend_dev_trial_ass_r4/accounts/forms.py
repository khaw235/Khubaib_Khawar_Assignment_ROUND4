from dataclasses import field
from tabnanny import verbose
from django import forms
from .models import Sale


class SalesDataForm(forms.Form):
    """
    This class creates a Form for Login of a user.

    '''

    Attributes
    ----------
    email : forms.CharField's Object
        a variable to create an Input Field for Email Address.
    csv : forms.FileField's Object
        a variable to create an Input Field for a File
    fields : a list
        a variable that defied the list containing the names of the 
        fields of this form
    """

    email = forms.CharField(max_length=254)
    csv = forms.FileField()

    fields = ['email', 'csv']