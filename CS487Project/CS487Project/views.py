from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from forms import UserCreateForm
from django.core.mail import send_mail

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

def contact(request):
        errors = []
        if request.method == 'POST':
                if not request.POST.get('subject', ''):
                        errors.append('Enter a subject.')
                if not request.POST.get('message', ''):
                        errors.append('Enter a message.')
                if request.POST.get('email') and '@' not in request.POST['email']:
                        errors.append('Enter a valid e-mail address.')
                if not errors:
                        send_mail(
                                request.POST['subject'],
                                request.POST['message'],
                                request.POST.get('email', 'noreply@example.com'),
                                ['jzhu42@hawk.iit.edu'],
                        )
                        return HttpResponseRedirect('/accounts/contact/thanks/')
        return render_to_response('contact/contact_form.html',
                {'errors': errors})

def thanks(request):
        return render(request, 'contact/thanks.html')
