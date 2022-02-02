from django import forms
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.forms.models import ModelForm
from .models import *
from django.http import request
'''class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["first_name","last_name","email"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control col-lg-3"}),
            "last_name":forms.TextInput(attrs={"class":"form-control col-lg-3"}),
            "email":forms.TextInput(attrs={"class":"form-control col-lg-3"}),
        }
'''

        
class ProForm(forms.ModelForm):
    class Meta:
        model=CastomUser
        fields=["Image","Numer","Father_name","Class_Roll","Bed_Number","Blood_Group","Address","Parents_number","Date_of_Birth","Gender","Emediate_Gauedion_Numer"]
        widgets={
            "Image":forms.FileInput(attrs={"class":"form-control"}),
            "Numer":forms.TextInput(attrs={"class":"form-control"}),
            "Father_name":forms.TextInput(attrs={"class":"form-control"}),
            "Class_Roll":forms.TextInput(attrs={"class":"form-control"}),
            "Bed_Number":forms.TextInput(attrs={"class":"form-control"}),
            "Blood_Group":forms.Select(attrs={"class":"form-control"}),
            "Address":forms.TextInput(attrs={"class":"form-control"}),
            "Parents_number":forms.TextInput(attrs={"class":"form-control"}),
            "Date_of_Birth":forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            "Gender":forms.Select(attrs={"class":"form-control"}),
            "Emediate_Gauedion_Numer":forms.TextInput(attrs={"class":"form-control"}),
        }

class Avalavel(forms.ModelForm):
    class Meta:
        model=Afternoon_Meal
        fields=["Available"]
class AllUser(forms.ModelForm):
    class Meta:
        model=CastomUser
        fields=["StudentName","Hostel","Numer","Room_Number","Father_name","Father_profession","Class_Roll","Bed_Number","Blood_Group",'Address','Parents_number','Date_of_Birth','Gender','Emediate_Gauedion_Numer','permission',"Leave"]
        widgets={
            "StudentName":forms.TextInput(attrs={"class":"form-control"}),
            "Hostel":forms.TextInput(attrs={"class":"form-control"}),
            #"Image":forms.TextInput(attrs={"class":"form-control",'type':"file"}),
            "Numer":forms.TextInput(attrs={"class":"form-control"}),
            "Room_Number":forms.TextInput(attrs={"class":"form-control"}),
            "Father_name":forms.TextInput(attrs={"class":"form-control"}),
            "Father_profession":forms.TextInput(attrs={"class":"form-control"}),
            "Class_Roll":forms.DateInput(attrs={'class':'form-control'}),
            "Bed_Number":forms.TextInput(attrs={"class":"form-control"}),
            "Blood_Group":forms.Select(attrs={"class":"form-control"}),
            "Address":forms.TextInput(attrs={"class":"form-control"}),
            "Parents_number":forms.TextInput(attrs={"class":"form-control"}),
            "Date_of_Birth":forms.TextInput(attrs={"class":"form-control"}),
            "Gender":forms.Select(attrs={"class":"form-control"}),
            "Emediate_Gauedion_Numer":forms.TextInput(attrs={"class":"form-control"}),
        }
class Hostel(forms.ModelForm):
    class Meta:
        model=CastomUser
        fields=["Leave"]
        widgets={
        }