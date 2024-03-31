from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import loader
from django.template.exceptions import TemplateDoesNotExist
from django.utils.html import strip_tags
from django.conf import settings

class Command(BaseCommand):
    help = 'Test l\'envoi d\'un e-mail'

    def handle(self, *args, **options):
        subject = 'Test d\'envoi d\'e-mail'
        text_content = 'Contenu du texte alternatif.'
        html_content = render_to_string('email_template.html', {'first_name': 'Test'})
        
        # body = strip_tags(html_content)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['prezent.cadeau@gmail.com']
        print('HTML content:\n', html_content)
        # Créer l'objet e-mail et envoyer
        message = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        message.attach_alternative(html_content, "text/html")
        message.send()

        self.stdout.write(self.style.SUCCESS('E-mail envoyé avec succès !'))