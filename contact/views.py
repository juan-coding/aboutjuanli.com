from django.shortcuts import render
# from django.http import HttpResponse
from contact.forms import ContactForm
# from django.core.mail import send_mail


def index(request):
    form_class = ContactForm

    # if request.method == "POST":
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         subject = form.cleaned_data["subject"]
    #         message = form.cleaned_data["message"]
    #         sender = form.cleaned_data["sender"]
    #         cc_myself = form.cleaned_data["cc_myselft"]
    #
    #         recipients = ['juanli.work@gmail.com']
    #         if cc_myself:
    #             recipients.append(sender)
    #
    #         send_mail(subject, message, sender, recipients)
    #         return HttpResponse('/THANKS/')
    return render(request, "contact/index.html",
                  {"form": form_class})



