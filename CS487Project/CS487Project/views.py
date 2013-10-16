from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

def register(request):
        if request.method == 'POST':
                form = UserCreationForm(request.POST)
                if form.is_valid():
                        new_user = form.save()
                        return HttpResponseRedirect("/videos/")
        else:
                form = UserCreationForm()
        return render(request, "registration/register.html", {
                'form': form,
        })
