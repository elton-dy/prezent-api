from rest_framework import serializers
from .models import User, Conversation, Message, Product, Favori, Visitor , Gender,Article, PasswordReset
from .models import AgeRange, Occasion, Relationship, ActivityInterest, PersonalityPreference
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.forms import PasswordChangeForm
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


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'user', 'visitor', 'timestamp', 'messages']
        
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
        fields = '__all__'

    def create(self, validated_data):
        # Extraire les données relatives aux relations plusieurs-à-plusieurs
        print(f"Validated data: {validated_data}")
        age_ranges = validated_data.pop('age_ranges', [])
        occasions = validated_data.pop('occasions', [])
        relationships = validated_data.pop('relationships', [])
        activities_interests = validated_data.pop('activities_interests', [])
        personalities_preferences = validated_data.pop('personalities_preferences', [])

        # Créer l'instance Product
        product = Product.objects.create(**validated_data)

        # Ajouter les relations
        product.age_ranges.set(age_ranges)
        product.occasions.set(occasions)
        product.relationships.set(relationships)
        product.activities_interests.set(activities_interests)
        product.personalities_preferences.set(personalities_preferences)

        return product

    def update(self, instance, validated_data):
        # Extraire les données relatives aux relations plusieurs-à-plusieurs
        age_ranges = validated_data.pop('age_ranges', [])
        occasions = validated_data.pop('occasions', [])
        relationships = validated_data.pop('relationships', [])
        activities_interests = validated_data.pop('activities_interests', [])
        personalities_preferences = validated_data.pop('personalities_preferences', [])

        # Mettre à jour les attributs de l'instance Product
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Mettre à jour les relations
        instance.age_ranges.set(age_ranges)
        instance.occasions.set(occasions)
        instance.relationships.set(relationships)
        instance.activities_interests.set(activities_interests)
        instance.personalities_preferences.set(personalities_preferences)

        return instance

    def _set_relations(self, instance, model, related_data, field_name):
        # Supprimer toutes les relations existantes
        getattr(instance, field_name).clear()

        # Ajouter les nouvelles relations
        for item_data in related_data:
            item, created = model.objects.get_or_create(**item_data)
            getattr(instance, field_name).add(item)

class FavoriSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = ProductSerializer()

    class Meta:
        model = Favori
        fields = '__all__'

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Ajoutez les informations utilisateur au jeton
        token['email'] = user.email
        token['id'] = user.id

        return token
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        user = self.context['user']
        form = PasswordChangeForm(user, {'new_password1': attrs['new_password'], 'new_password2': attrs['new_password']})
        if not form.is_valid():
            raise serializers.ValidationError(form.errors)
        return attrs