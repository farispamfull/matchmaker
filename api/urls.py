from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from authentication.views import user_logout, LoginView
from users.views import UserViewSet, user_create
from .views import MatchView

app_name = 'api'
router_v1 = DefaultRouter()
router_v1.register('clients', UserViewSet, basename='client')

auth_patterns = [
    path('token/logout/',
         user_logout,
         name='user_logout/'),
    path('token/login/',
         LoginView.as_view(),
         name='login_user'), ]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('clients/create/', user_create, name='user_create'),
    path('clients/<int:user_id>/match/', MatchView.as_view()),
    path('', include(router_v1.urls))
]
