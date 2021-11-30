from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Match
from api.serializers import UserSerializer
from users.utils import Util
from .models import User


class MatchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        swiper = request.user
        swiped = get_object_or_404(User, id=user_id)
        obj, create = Match.objects.get_or_create(swiper=swiper, swiped=swiped)

        if create:
            if swiper.is_swiped(swiped):
                Util.send_match_for_email(request, from_user=swiper,
                                          match_user=swiped)
                Util.send_match_for_email(request, from_user=swiped,
                                          match_user=swiper)

            serializer = UserSerializer(swiped, context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errors = {'errors': 'Вы уже поставили симпатию этому человеку'}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        swiped = get_object_or_404(User, id=user_id)
        user = request.user
        match_obj = user.swiped.filter(swiped=swiped)
        if match_obj:
            match_obj.first().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        error = {'errors': 'Вы еще не поставили симпатию на этого человека'}
        return Response(data=error, status=status.HTTP_400_BAD_REQUEST)
