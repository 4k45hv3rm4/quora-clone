from django import forms
from mysite.models import Question, Answer,Account
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text = 'Required. Add a valid email address')
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'],self.fields['username'],self.fields['password1'],self.fields['password2']):
            field.widget.attrs.update({'class': 'form-control '})


class AccountAuthenticationForm(forms.ModelForm):
    password  = forms.CharField(label= 'Password', widget=forms.PasswordInput)

    class Meta:
        model  =  Account
        fields =  ('email', 'password')
        widgets = {
                   'email':forms.TextInput(attrs={'class':'form-control'}),
                   'password':forms.TextInput(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'],self.fields['password']):
            field.widget.attrs.update({'class': 'form-control '})

    def clean(self):
        if self.is_valid():

            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')

class AccountUpdateform(forms.ModelForm):
    class Meta:
        model  = Account
        fields = ('email', 'username', 'bio', 'profession')
        widgets = {
                   'email':forms.TextInput(attrs={'class':'form-control'}),
                   'bio':forms.TextInput(attrs={'class':'form-control'}),
                   'profession':forms.TextInput(attrs={'class':'form-control'}),
                   'username':forms.TextInput(attrs={'class':'form-control'}),
        }



    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk = self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError("Email '%s' already in use." %email)
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk = self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError("Username '%s' already in use." % username)


class QuestionForm(forms.ModelForm):
    class Meta:

        model = Question
        fields = ['question', 'genre']

class EditQuestionForm(forms.ModelForm):
    class Meta:

        model = Question
        fields = ['question', 'genre']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer',)




# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields= ['bio','profession', ]

