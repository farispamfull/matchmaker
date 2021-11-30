from django.contrib.auth import logout as django_logout
from django.contrib.auth import user_logged_out
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserLoginSerializer


class LoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    token = None

    def get_response(self):
        data = {'auth_token': self.token}
        return Response(data, status=status.HTTP_201_CREATED)

    def login(self, user):
        self.token = Token.objects.get_or_create(user=user)[0].key

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        self.login(user)
        return self.get_response()



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.user.auth_token.delete()
    user_logged_out.send(
        sender=request.user.__class__, request=request, user=request.user
    )
    django_logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)
