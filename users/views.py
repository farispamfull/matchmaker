from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import User
from .serializers import (UserSerializer, ChangePasswordSerializer,
                          )


class UserViewSet(ReadOnlyModelViewSet, DestroyModelMixin):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'set_password':
            return ChangePasswordSerializer
        else:
            return UserSerializer

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'],
            permission_classes=[IsAuthenticated])
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        user.set_password(serializer.data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
