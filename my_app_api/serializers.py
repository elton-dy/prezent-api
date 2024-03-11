from rest_framework import serializers
from .models import User, Conversation, Message, Product, Favori, Visitor , Gender
from .models import AgeRange, Occasion, Relationship, ActivityInterest, PersonalityPreference
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        # Utilisez la méthode set_password pour hacher le mot de passe
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'  # Sérialise tous les champs du modèle Conversation

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class AgeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeRange
        fields = '__all__'

class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = '__all__'

class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'

class ActivityInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityInterest
        fields = '__all__'

class PersonalityPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityPreference
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    gender = GenderSerializer()
    age_ranges = AgeRangeSerializer(many=True)
    occasions = OccasionSerializer(many=True)
    relationships = RelationshipSerializer(many=True)
    activities_interests = ActivityInterestSerializer(many=True)
    personalities_preferences = PersonalityPreferenceSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'  # Incluez les champs associés comme des sous-objets sérialisés
    def create(self, validated_data):
        # Extraire les données relatives aux relations plusieurs-à-plusieurs
        age_ranges_data = validated_data.pop('age_ranges', [])
        occasions_data = validated_data.pop('occasions', [])
        relationships_data = validated_data.pop('relationships', [])
        activities_interests_data = validated_data.pop('activities_interests', [])
        personalities_preferences_data = validated_data.pop('personalities_preferences', [])

        # Créer l'instance Product
        product = Product.objects.create(**validated_data)

        # Ajouter les relations
        self._set_relations(product, AgeRange, age_ranges_data)
        self._set_relations(product, Occasion, occasions_data)
        self._set_relations(product, Relationship, relationships_data)
        self._set_relations(product, ActivityInterest, activities_interests_data)
        self._set_relations(product, PersonalityPreference, personalities_preferences_data)

        return product

    def update(self, instance, validated_data):
        # Extraire les données relatives aux relations plusieurs-à-plusieurs
        age_ranges_data = validated_data.pop('age_ranges', [])
        occasions_data = validated_data.pop('occasions', [])
        relationships_data = validated_data.pop('relationships', [])
        activities_interests_data = validated_data.pop('activities_interests', [])
        personalities_preferences_data = validated_data.pop('personalities_preferences', [])

        # Mettre à jour les attributs de l'instance Product
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Mettre à jour les relations
        self._set_relations(instance, AgeRange, age_ranges_data)
        self._set_relations(instance, Occasion, occasions_data)
        self._set_relations(instance, Relationship, relationships_data)
        self._set_relations(instance, ActivityInterest, activities_interests_data)
        self._set_relations(instance, PersonalityPreference, personalities_preferences_data)

        return instance

    def _set_relations(self, instance, model, related_data):
        # Supprimer toutes les relations existantes
        getattr(instance, model.__name__.lower() + 's').clear()

        # Ajouter les nouvelles relations
        for item_data in related_data:
            item, created = model.objects.get_or_create(**item_data)
            getattr(instance, model.__name__.lower() + 's').add(item)

class FavoriSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = ProductSerializer()

    class Meta:
        model = Favori
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        User = get_user_model()

        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.check_password(attrs['password']):
            raise serializers.ValidationError("Invalid credentials.")

        # Appelez la méthode get_token pour générer le jeton avec les informations utilisateur
        token = self.get_token(user)

        # Retournez le jeton et les informations utilisateur dans la réponse
        return {
            'access': str(token),
            'user': UserSerializer(user).data,
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Ajoutez les informations utilisateur au jeton
        token['email'] = user.email
        token['id'] = user.id

        return token