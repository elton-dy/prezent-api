import csv
from my_app_api.models import (Product, Gender, AgeRange, Occasion, Relationship,
                               ActivityInterest, PersonalityPreference)
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Load a list of products from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Créer ou récupérer les objets liés
                gender, _ = Gender.objects.get_or_create(name=row['Genre'])
                age_range, _ = AgeRange.objects.get_or_create(age_range=row["Tranche d'âge"])
                occasion, _ = Occasion.objects.get_or_create(occasion_name=row['Occasion'])
                relationship, _ = Relationship.objects.get_or_create(relationship_type=row['Relation'])
                activity_interest, _ = ActivityInterest.objects.get_or_create(activity=row["activités / centres d'intérêts"])
                personality_preference, _ = PersonalityPreference.objects.get_or_create(personality=row["Personnalité / Préférences"])

                # Créer l'objet Product
                product = Product.objects.create(
                    name=row['Cadeau'],
#                     description="Description si disponible",
                    typology=row['Typologie cadeau'],
                    link=row['Lien'],
                    target_budget=row['Budget cible'],
#                     fixed_price="Prix si disponible",
#                     image_url="URL de l'image si disponible",
                    gender=gender
                )

                # Associer l'objet Product avec les autres objets liés
                product.age_ranges.add(age_range)
                product.occasions.add(occasion)
                product.relationships.add(relationship)
                product.activities_interests.add(activity_interest)
                product.personalities_preferences.add(personality_preference)

                product.save()
        self.stdout.write(self.style.SUCCESS('The command completed successfully.'))

