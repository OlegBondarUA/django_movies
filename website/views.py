from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse


from .forms import ContactForm
from .models import Contact
from utils.email import send_html_email


class ContactView(FormView):
    template_name = 'contact.html'
    model = Contact
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        Contact.objects.create(**form.cleaned_data)
        to_email = form.cleaned_data.get('email')
        send_html_email(
            subject='Welcome to our website.',
            to_email=[to_email],
            context={
                'name': form.cleaned_data.get('name'),
                'link': self.request.build_absolute_uri(reverse('index')),
            },
            template_name='emails/email.html'
        )
        messages.add_message(
            self.request, messages.SUCCESS,
            f"{form.cleaned_data.get('name').title()} дякую за повідомлення!"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.WARNING,
            'Будь ласка, надсилайте коректні дані!'
        )
        return super().form_invalid(form)

