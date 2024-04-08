from rest_framework.permissions import BasePermission
from .models import Visitor,User

class IsAuthenticatedOrVisitorWithUUID(BasePermission):
    def has_permission(self, request, view):
        # Autoriser les utilisateurs authentifiés
        if request.user.is_authenticated:
            return True

        # Autoriser les visiteurs avec un UUID valide
        visitor_uuid = request.GET.get('visitor_uuid') or request.data.get('visitor_uuid')
        if visitor_uuid:
            return Visitor.objects.filter(uuid=visitor_uuid).exists()

        return False

class CreateOrReadOnly(BasePermission):
    """
    Permission personnalisée pour permettre l'accès non authentifié aux requêtes POST et GET,
    mais exiger l'authentification pour les autres méthodes.
    """

    def has_permission(self, request, view):
        # Autoriser POST et GET sans authentification
        if request.method in ['POST']:
            return True

        # Pour les autres requêtes, exiger l'authentification
        return request.user and request.user.is_authenticated