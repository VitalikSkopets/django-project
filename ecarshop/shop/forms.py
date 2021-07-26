from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50,
                                 label='First name',
                                 help_text='required field',
                                 )
    last_name = forms.CharField(required=False,
                                max_length=50,
                                label='Last name',
                                )
    email = forms.EmailField(max_length=150,
                             label='email address',
                             help_text='required field',
                             )
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
                              max_length=2000,
                              label='Text message',
                              initial='Please, enter your message...',
                              help_text='required field',
                              )
    captcha = CaptchaField()


class NewUserForm(UserCreationForm):
    username = forms.CharField(label='Login')
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(),
                                help_text=f"Password must be a minimum of 8 characters and contain a combination of "
                                          f"upper- and lower-case alphabetic characters, numeric characters, and "
                                          f"special characters."
                                )
    password2 = forms.CharField(widget=forms.PasswordInput(),
                                label='Password confirmation',
                                help_text="Enter the same password as before, for verification.")
    captcha = CaptchaField(generator='captcha.helpers.math_challenge')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
