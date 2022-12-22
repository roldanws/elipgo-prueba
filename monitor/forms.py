from django import forms
from .models import Camera

class CameraForm(forms.ModelForm):

    class Meta:
        model = Camera
        fields = ['usuario', 'password', 'ip', 'puerto']
        widgets = {
            'usuario': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usuario'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
            'ip': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Url  '}),
            'puerto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Puerto  '}),
        }
        labels = {
            'usuario':'', 'ip':'', 'password': '','puerto':'',
        }