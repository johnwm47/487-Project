from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
        email = forms.EmailField(required=True)

        class Meta:
                model = User
                fields = ("username", "email", "password1", "password2")

        def save(self, commit=True):
                user = super(UserCreateForm, self).save(commit=False)
                user.email = self.cleaned_data["email"]
                if commit:
                        user.save()
                        if user.email[-4:] == '.edu':
                                Group.objects.get(name='uploaders').user_set.add(user)
                return user
