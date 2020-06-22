from django import forms
from django.contrib.auth.models import User
from cp_app.models import UserProfileInfo,Problem,Comment

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('first_name','last_name','username','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('text',)

        
# class SearchForm(forms.Form):
#     tag = forms.CharField(required=False,widget=forms.TextInput(attrs={'autocomplete': 'off'}) )
#     rating =forms.IntegerField(required=False,widget=forms.TextInput(attrs={'autocomplete': 'off'}))
#     author = forms.CharField(required=False,widget=forms.TextInput(attrs={'autocomplete': 'off'}) )
#     problem_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'autocomplete': 'off'}) )
