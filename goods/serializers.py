from rest_framework import serializers
from goods.models import Ad


class AdListSerializerCut(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('id', 'title', 'price')


class AdDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'
