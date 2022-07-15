from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    
    class Meta:
        model = User
        fields= ('username','first_name','last_name','password1','password2')   

    def __init__(self,*args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'