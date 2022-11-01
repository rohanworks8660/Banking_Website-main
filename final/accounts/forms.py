from django import forms
from django.forms import ModelForm


class NewForm(ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    fathers_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    mothers_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    gender = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    state = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    dob = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email_address = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(
        widget=forms.TextInput( attrs={'class': 'form-control'}))


class Ourform(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    first_nae = forms.CharField(label='First name', max_length=100)
    lat_name = forms.CharField(label='Last name', max_length=100)
    firs_name = forms.CharField(label='First name', max_length=100)
    last_nme = forms.CharField(label='Last name', max_length=100)
    frst_name = forms.CharField(label='First name', max_length=100)
    last_nam = forms.CharField(label='Last name', max_length=100)
    fist_name = forms.CharField(label='First name', max_length=100)
    last_ne = forms.CharField(label='Last name', max_length=100)
