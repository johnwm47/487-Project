from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, RequestContext
from forms import UserCreateForm, ContactForm
from django.core.mail import send_mail
import smtplib

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
        #errors = []
        if request.method == 'POST':
                #if not request.POST.get('subject', ''):
                #        errors.append('Enter a subject.')
                #if not request.POST.get('message', ''):
                #        errors.append('Enter a message.')
                #if request.POST.get('email') and '@' not in request.POST['email']:
                #        errors.append('Enter a valid e-mail address.')
                #if not errors:
                form = ContactForm(request.POST)
                if form.is_valid():
                        cd = form.cleaned_data
                        s = smtplib.SMTP("smtp.gmail.com","25")
                        s.ehlo()
                        s.starttls()
                        s.login("testdjango487@gmail.com", "su123456")
                        send_mail(
                                cd['subject'],
                                cd['message'],
                                cd.get('email', 'testdjango487@gmail.com'),
                                ['testdjango487@gmail.com'],
                        )
                        s.quit()
                        return HttpResponseRedirect('/accounts/contact/thanks/')
        else:
                form = ContactForm(
                        initial = {'subject':'I love this one!'}
                        )
        c = RequestContext(request, {
                'form':form,
                })
        return render_to_response('contact/contact_form.html', context_instance=c)

def thanks(request):
        return render(request, 'contact/thanks.html')
