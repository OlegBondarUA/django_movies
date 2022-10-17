from django.views.generic import FormView
from django.contrib import messages

from .forms import ContactForm
from .models import Contact


class ContactView(FormView):
    template_name = 'contact.html'
    model = Contact
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        Contact.objects.create(**form.cleaned_data)
        messages.add_message(
            self.request, messages.SUCCESS,
            f"{form.cleaned_data.get('name').title()} дякую за повідомлення!"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS,
            'Будь ласка, надсилайте коректні дані!'
        )
        return super().form_invalid(form)

