import graphene
from graphene_django.types import DjangoObjectType
from .models import User, Interaction, Product, Preference  # Import Product and Preference models

class UserType(DjangoObjectType):
    class Meta:
        model = User

class InteractionType(DjangoObjectType):
    class Meta:
        model = Interaction

class ProductType(DjangoObjectType):  # Define ProductType for Product model
    class Meta:
        model = Product

class PreferenceType(DjangoObjectType):  # Define PreferenceType for Preference model
    class Meta:
        model = Preference

# UserProfileType to combine user, preferences, and interactions
class UserProfileType(graphene.ObjectType):
    user = graphene.Field(UserType)
    preferences = graphene.List(PreferenceType)
    interactions = graphene.List(InteractionType)

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())
    preferences = graphene.List(PreferenceType, userId=graphene.Int())
    interactions = graphene.List(InteractionType, userId=graphene.Int())
    all_products = graphene.List(ProductType)
    product = graphene.Field(ProductType, itemId=graphene.Int())
    product = graphene.Field(ProductType, itemId=graphene.Int())
    user_profile = graphene.Field(UserProfileType, id=graphene.Int())

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(id=id)

    def resolve_preferences(self, info, userId):
        return Preference.objects.filter(user_id=userId)

    def resolve_interactions(self, info, userId):
        return Interaction.objects.filter(user_id=userId)

    # Resolver for user profile, combining user, preferences, and interactions
    def resolve_user_profile(self, info, id):
        try:
            user = User.objects.get(id=id)
            preferences = Preference.objects.filter(user=user)
            interactions = Interaction.objects.filter(user=user)
            return UserProfileType(user=user, preferences=preferences, interactions=interactions)
        except User.DoesNotExist:
            return None

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_product(self, info, itemId):
        return Product.objects.get(item_id=itemId)

schema = graphene.Schema(query=Query)
