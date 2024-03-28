import os
from django.core.management.base import BaseCommand
from django.conf import settings
from my_app_api.models import Article

class Command(BaseCommand):
    help = 'Insert articles into the database'

    def handle(self, *args, **options):
        # Supprimer tous les articles existants
        Article.objects.all().delete()

        # Insérer de nouveaux articles
        Article.objects.create(
            title='Trouvez le cadeau parfait grâce à l\'IA : Découvrez notre plateforme innovante',
            subtitle='Comment l\'intelligence artificielle peut faciliter la recherche de cadeaux',
            content = """
                <p>À l'ère numérique, nous sommes constamment bombardés de choix, ce qui peut rendre la recherche du cadeau idéal pour nos proches une tâche ardue. C'est là que notre plateforme entre en jeu. Nous utilisons la puissance de l'intelligence artificielle (IA) pour simplifier la recherche de cadeaux, en faisant correspondre vos besoins et les préférences de vos destinataires, pour des cadeaux toujours plus significatifs.</p>

                <h3>L’IA au service du cadeau parfait</h3>

                <p>Notre plateforme repose sur une technologie d'IA sophistiquée qui prend en compte une multitude de facteurs pour vous proposer des suggestions de cadeaux personnalisées. Plus besoin de parcourir d'innombrables sites Web ou de passer des heures dans les magasins. Notre IA fait tout le travail pour vous, en un clin d'œil.</p>

                <h3>Les enjeux de la recherche de cadeaux</h3>

                <p>La recherche de cadeaux peut s'avérer stressante et chronophage. Les enjeux sont multiples :</p>
                <p>Connaissance limitée du destinataire : Il est parfois difficile de connaître parfaitement les goûts et les besoins de quelqu'un, en particulier pour les connaissances plus récentes ou les collègues.</p>
                <p>Surcharge d'informations : L'abondance d'options disponibles en ligne peut être écrasante, conduisant à des choix impulsifs ou à la procrastination.</p>
                <p>Pression sociale : L'attente de trouver le cadeau parfait peut entraîner du stress et de la pression, en particulier lors d'occasions spéciales.</p>

                <h3>Notre solution : Des cadeaux personnalisés en un clic</h3>
                <p>Notre plateforme utilise l'IA pour aborder ces défis. Comment cela fonctionne-t-il ? Voici les étapes clés :</p>
                <p>1. Créez un profil : Commencez par créer un profil pour le destinataire du cadeau. Plus vous fournirez d'informations, meilleures seront les suggestions.</p>
                <p>2. Analyse en profondeur : Notre IA analyse les données de votre profil, prenant en compte les goûts, les intérêts, les besoins et même les occasions spéciales.</p>
                <p>3. Suggestions personnalisées : En quelques secondes, notre IA génère une liste de cadeaux soigneusement sélectionnés, en fonction des données recueillies.</p>

                <h3>Les avantages de notre plateforme</h3>
                <p>1. Économie de temps : Notre plateforme vous fait gagner un temps précieux en éliminant la recherche fastidieuse de cadeaux.</p>
                <p>2. Cadeaux plus significatifs : En se basant sur les préférences personnelles du destinataire, nos suggestions conduisent à des cadeaux plus appréciés.</p>
                <p>3. Réduction du stress : Fini le stress de dernière minute pour trouver un cadeau. Notre IA vous offre des options rapides et efficaces.</p>

                <h3>Expérience utilisateur optimale</h3>
                <p>Nous avons conçu notre plateforme pour garantir une expérience utilisateur optimale. Notre interface conviviale rend la création de profils et la sélection de cadeaux un jeu d'enfant. De plus, nous veillons à ce que chaque suggestion de cadeau soit accompagnée de détails, d'avis et de liens pour faciliter votre décision.</p>

                <h3>Sécurité et confidentialité</h3>
                <p>Nous comprenons l'importance de la sécurité et de la confidentialité de vos données. Notre plateforme est sécurisée et conforme aux réglementations en vigueur pour garantir la protection de vos informations personnelles.</p>
                <p>Rejoignez-nous pour une expérience de shopping inédite</p>
                <p>Ne laissez plus la recherche de cadeaux vous stresser. Faites confiance à notre IA pour vous guider vers le cadeau parfait. Que ce soit pour un anniversaire, une fête des mères, Noël ou toute autre occasion spéciale, notre plateforme est là pour vous simplifier la vie.</p>

                <h3>Optimisé pour le SEO</h3>
                <p>Nous sommes conscients de l'importance du référencement pour faciliter la découverte de notre plateforme. En utilisant des mots-clés pertinents tels que "cadeau personnalisé", "IA pour les cadeaux" et d'autres termes connexes, notre site est conçu pour être facilement trouvé par les utilisateurs à la recherche d'une solution de recherche de cadeaux innovante et efficace.</p>

                <h3>Conclusion</h3>
                <p>Notre plateforme révolutionnaire basée sur l'IA change la donne en matière de recherche de cadeaux. Oubliez les tracas et les incertitudes, et optez pour une expérience de shopping plus intelligente et plus efficace. Rejoignez-nous dès aujourd'hui pour découvrir le futur de la recherche de cadeaux.</p>
                """,
                author = "Marie-claire")
        
        Article.objects.create(
            title='Découvrez l\'Art du Cadeau : Des Trésors Uniques d\'Artisans pour Toutes les Occasions',
            subtitle='Pourquoi choisir un cadeau artisanal ?',
            content="""
                <p>À une époque où la production de masse est la norme, il y a quelque chose d'exceptionnel dans un cadeau artisanal. Les artisans du monde entier investissent leur temps, leur créativité et leur savoir-faire dans la création d'objets uniques et authentiques. Chez nous, nous avons fait de la mission de mettre en avant ces trésors artisanaux. Découvrez notre collection soigneusement sélectionnée d'idées de cadeaux provenant d'artisans passionnés et talentueux.</p>

                <h3>Unicité et Authenticité</h3>
                <p>Chaque pièce artisanale est unique, ce qui signifie que votre cadeau ne ressemblera à aucun autre. Il porte l'empreinte digitale de son créateur.</p>

                <h3>Qualité Exceptionnelle</h3>
                <p>Les artisans sont fiers de leur travail et utilisent souvent des matériaux de haute qualité pour créer des pièces durables et belles.</p>

                <h3>Soutien aux Artisans</h3>
                <p>En choisissant un cadeau artisanal, vous soutenez directement un artisan et sa communauté, contribuant ainsi à préserver des traditions et des compétences uniques.</p>

                <h3>Histoire et Signification</h3>
                <p>Chaque objet artisanal a une histoire à raconter. Il peut être le fruit d'une tradition séculaire, d'un métier rare ou d'une inspiration personnelle profonde.</p>

                <p>Conclusion : Offrez du Sens avec un Cadeau Artisanal</p>
                <p>Lorsque vous offrez un cadeau artisanal, vous offrez bien plus qu'un simple objet. Vous offrez une part de la passion, de la créativité et de l'âme d'un artisan. Vous offrez une expérience inoubliable pour celui qui reçoit le cadeau. Rejoignez-nous dans notre mission de célébrer l'artisanat et de créer des liens significatifs grâce au pouvoir des cadeaux uniques et authentiques. Explorez notre collection dès aujourd'hui et trouvez le cadeau parfait pour votre prochaine occasion spéciale.</p>

                <p>Que ce soit pour célébrer l'amour, l'amitié, la famille ou simplement pour faire plaisir, les cadeaux artisanaux sont une manière extraordinaire de dire "je t'aime" ou "je pense à toi". L'art du cadeau n'a jamais été aussi personnel et significatif. Rejoignez-nous pour soutenir les artisans du monde entier et rendre chaque occasion spéciale encore plus mémorable grâce à l'authenticité de l'artisanat.</p>
            """,
            author="Marie-claire"
        )