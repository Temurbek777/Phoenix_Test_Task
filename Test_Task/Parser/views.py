from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserRegistrationSerializer

from .parser import getNews
from .models import News

'''
API представления для регистрации и 
Получения новостей
'''
#=======================API представление для Регистрации пользователей============
class RegisterUserApi(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Регистрация пользователей",
        request_body=UserRegistrationSerializer,
        responses={
            201: "User registered successfully!",
            400: "Invalid data"
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь зарегистрировано успешно!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#====================API Представление для отправки 10 новостей=============
class GetNewsApi(APIView):
    authentication_classes = [JWTAuthentication]  # Use your preferred authentication method
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить 10 последних новостей для авторизованных пользователей",
        responses={
            200: openapi.Response(
                description="Список новостей",
                examples={
                    "application/json": [
                        {
                            "title": "Заголовок новостя",
                            "description": "Описание новостя",
                            "image": "http://example.com/image.jpg",
                            "views_count": 123,
                            "publish_date": "2024-11-16",
                            "category": "Спорт"
                        }
                    ]
                },
            ),
            401: "Unauthorized",
            500: "Internal Server Error"
        }
    )

    def get(self, request):
        news_list = []
        latest_news = getNews()
        if latest_news['res']:
            for news in latest_news['data']:
                NEWS = News.objects.create(
                    title = news['title'],
                    description = news['description'],
                    image = news['image'],
                    views_count = news['views_count'],
                    publish_date = news['created_at'],
                    category = news['category']
                )

                news_list.append({
                    "title": NEWS.title,
                    "description": NEWS.description,
                    "image": NEWS.image,
                    "views_count": NEWS.views_count,
                    "publish_date": NEWS.publish_date,
                    "category": NEWS.category
                })
                print(news_list)
            return Response(news_list, status=200)
        else:
            return Response({"error": f"Failed to get news. Status code: {latest_news['status']}"})
