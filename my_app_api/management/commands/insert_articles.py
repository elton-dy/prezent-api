import os
from django.core.management.base import BaseCommand
from django.conf import settings
from my_app_api.models import Article

class Command(BaseCommand):
    help = 'Insert articles into the database'

    def handle(self, *args, **options):
        article = Article.objects.create(
            title='Pourquoi l\'IA est une bonne aide pour trouver un cadeau à offrir',
            subtitle='Comment l\'intelligence artificielle peut faciliter la recherche de cadeaux',
            content = """
                L'intelligence artificielle (IA) est de plus en plus présente dans notre quotidien, et elle peut être d'une grande aide lorsqu'il s'agit de trouver un cadeau à offrir.

                En effet, grâce à l'analyse des données et à l'apprentissage automatique, l'IA peut aider à déterminer les préférences et les goûts de la personne à qui l'on souhaite offrir un cadeau. Elle peut également prendre en compte les tendances actuelles et les avis des autres clients pour recommander des produits pertinents.<br> <br>

                De plus, l'IA peut aider à trouver des cadeaux originaux et personnalisés, en fonction des centres d'intérêt et des habitudes de la personne concernée. Elle peut également aider à trouver des cadeaux pour des occasions spéciales, comme des anniversaires ou des fêtes de fin d'année.

                En utilisant l'IA pour trouver un cadeau, on peut gagner du temps et éviter les erreurs. En effet, l'IA peut analyser rapidement de grandes quantités de données et recommander des produits pertinents en fonction des critères sélectionnés. De plus, elle peut aider à éviter les cadeaux en double ou les cadeaux qui ne plaisent pas à la personne concernée.

                En somme, l'IA peut être une aide précieuse pour trouver un cadeau à offrir. Grâce à sa capacité à analyser les données et à recommander des produits pertinents, elle peut aider à trouver des cadeaux originaux et personnalisés qui feront plaisir à coup sûr.
                """,
            author = "Lou")