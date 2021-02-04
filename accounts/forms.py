from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm, AuthenticationForm, UsernameField, PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
import string
import random
from django.shortcuts import get_object_or_404


def create_username(name):
    name = name.replace(" ", "")
    choices = string.ascii_letters + string.hexdigits
    choice = "".join(random.choice(choices) for _ in range(10))
    username = f'{name}{choice}'
    return username


class SignUpForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('The password and confirm password fields didn’t match.'),
    }

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class':'form-control form-control-solid', 
                'placeholder': 'Email'
                }
            ),
        label="",
        )
    first_name = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-solid', 
                'placeholder': 'Name'
                }
            ),
        label="",
        )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                 'placeholder': 'Password',
                 'class': 'form-control form-control-solid signup-pswrd',
                 },
            ),
        label="",
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password', 
                'placeholder': 'Password Confirm',
                'class': 'form-control form-control-solid signup-pswrd',
                }
            ),
        label="",
        )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = create_username(self.cleaned_data.get('first_name'))
        user.is_active = False
        if commit:
            user.save()
        return user


class UpdatePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control form-control-solid'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control form-control-solid'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control form-control-solid'


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="",
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-solid', 'placeholder': 'Email'}
        ) 
        )

    class Meta:
        model = User
        fields = ['email']
    
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)


class UpdateProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control form-control-solid'}))
    last_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control form-control-solid'}))
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="",
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-solid', 'placeholder': 'Email'}
        ) 
        )
    password = forms.CharField(
        label="",
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-solid', 'placeholder': 'Password'}
        )
    )
