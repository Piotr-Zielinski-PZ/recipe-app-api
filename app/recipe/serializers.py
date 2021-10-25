from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""

    class Meta:
        """Meta class for TagSerializer."""

        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id', )


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects."""

    class Meta:
        """Meta class for IngredientSerializer."""

        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id', )


class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """PrimaryKeyRelatedField which filters items by user."""

    def get_queryset(self):
        """Limit queryset to authenticated users items."""
        request = self.context.get('request')
        queryset = super().get_queryset()

        return queryset.filter(user=request.user)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize Recipe."""

    ingredients = UserFilteredPrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = UserFilteredPrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        """Meta class for RecipeSerializer."""

        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags', 'time_minutes',
                  'price', 'link')
        read_only_fields = ('id', )


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail."""

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes."""

    class Meta:
        """Meta class for RecipeImageSerializer."""
        model = Recipe
        fields = ('id', 'images')
        read_only_fields = ('id', )
