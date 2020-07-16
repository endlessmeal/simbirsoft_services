from rest_framework import generics
from goods.serializers import *
from goods.models import Ad, Tags
from django.db.models import F
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
import django_filters
from django_filters import rest_framework as filters

# creating a new ad (POST)
class AdCreateView(generics.CreateAPIView):
    serializer_class = AdDetailSerializer


# get all ads by id, title, price, (GET)
class AdListView(generics.ListAPIView):
    serializer_class = AdListSerializerCut
    queryset = Ad.objects.all()


# update an ad or delete (PUT, DELETE)
class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdDetailSerializer
    queryset = Ad.objects.all()


# get a fast look at ad without increment view counter
class AdFastLook(generics.RetrieveAPIView):
    serializer_class = AdListSerializerCut
    queryset = Ad.objects.all()


# get an entire look at ad with increment view counter
class AdEntireLook(APIView):
    def get_object(self, pk):
        try:
            ad_current = Ad.objects.get(pk=pk)
            ad_current.views = F('views') + 1
            ad_current.save()
            return Ad.objects.get(pk=pk)
        except Ad.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ad = self.get_object(pk)
        serializer = AdDetailSerializer(ad)
        return Response(serializer.data)


# get an entire list of tags
class TagAllLook(generics.ListAPIView):
    serializer_class = TagDetailSerializer
    queryset = Tags.objects.all()


class AdFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Ad
        fields = ['min_price', 'max_price']


# filter ads by price
class FindByTag(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AdFilter
