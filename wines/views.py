from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import generics
from wines.models import Country, Vendor, Rater, Wine
from wines.serializers import (UserSerializer, GroupSerializer,
                               CountrySerializer,
                               VendorSerializer,
                               RaterSerializer,
                               WineSerializer,
                               )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class VendorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class RaterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Rater.objects.all()
    serializer_class = RaterSerializer


class WineViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Wine.objects.all()
    serializer_class = WineSerializer


#class WineDetail(generics.RetrieveUpdateDestroyAPIView):
#    """
#    API endpoint that allows groups to be viewed or edited.
#    """
#    queryset = Wine.objects.all()
#    serializer_class = WineSerializer
