from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

'''
Машруты для регистрации,
получения новостей, 
логин, 
обновление токена 
'''
urlpatterns = [
    path('register/', RegisterUserApi.as_view()),
    path('get_news/', GetNewsApi.as_view(), name='get_news'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

