from django.contrib.auth.models import User, Group
from rest_framework import serializers
from wines.models import Country, Vendor, Rater, Wine, WineRating, VendorWine


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'code_iso2', 'code_iso3')


class VendorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            'name', 'url', 'is_active', 'plugin', 'page', 'max_pages',
            'product', 'stopwords')


class RaterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rater
        fields = ('name', 'url', 'is_active', 'plugin', 'page', 'limit')


class RatingSerializer(serializers.ModelSerializer):
    rater = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
     )

    class Meta:
        model = WineRating
        fields = ('rater', 'url', 'rating', 'num_ratings', 'modified')


class VendorWineSerializer(serializers.ModelSerializer):
    vendor = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
     )

    class Meta:
        model = VendorWine
        fields = ('vendor', 'url', 'volume', 'quantity', 'price', 'modified')


class WineSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=False, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    vendors = VendorWineSerializer(many=True, read_only=True)

    class Meta:
        model = Wine
        fields = (
            'id', 'name', 'winetype', 'color', 'winery', 'region', 'country',
            'ratings', 'vendors')
