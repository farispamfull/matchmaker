from rest_framework import serializers
from users.serializers import UserSerializer
class MatchSerializer(serializers.ModelSerializer):
    swiper=UserSerializer()

