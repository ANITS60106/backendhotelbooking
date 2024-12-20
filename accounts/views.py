from django.urls import reverse
from django.core.mail import send_mail  # Добавьте этот импорт
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import UserSerializer
from .utils import confirmation_token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

class MyTokenObtainSerilizer(TokenObtainPairSerializer):
    permission_classes = [AllowAny]

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        # Добавьте другие необходимые параметры
        data['username'] = self.user.username
        data['user_id'] = self.user.pk
        data['is_admin'] = self.user.is_staff
        data['message'] = "login successful"

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainSerilizer


class UserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        token = confirmation_token.make_token(user)

        confirmation_register_url = self.request.build_absolute_uri(
            reverse('accounts_app:register_confirm', kwargs={'pk': user.pk, 'token': token})
        )

        send_mail(
            subject="Регистрация подтверждение!",
            message=f"Привет, {user.username}! Перейди по этой ссылке {confirmation_register_url}",
            from_email="Bicos-Abricos@yandex.ru",
            recipient_list=[user.email, ]
        )


class RegisterConfirmView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, token):
        user = get_object_or_404(User, pk=pk)  # Если это CustomUser, замените на CustomUser и да пишу так

        if confirmation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email successfully verified!"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
