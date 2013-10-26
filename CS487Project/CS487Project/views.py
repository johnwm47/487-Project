from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms import UserCreateForm

def register(request):
        if request.method == 'POST':
                form = UserCreateForm(request.POST)
                if form.is_valid():
                        new_user = form.save()
                        return HttpResponseRedirect("/videos/")
        else:
                form = UserCreateForm()
        return render(request, "registration/register.html", {
                'form': form,
        })
