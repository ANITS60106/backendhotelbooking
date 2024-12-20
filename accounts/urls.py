from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import UserView, MyTokenObtainPairView, RegisterConfirmView

app_name = 'accounts_app'

urlpatterns = [
    path('register/', UserView.as_view()),
    path('register-confirm/<int:pk>/<str:token>/', RegisterConfirmView.as_view(), name='register_confirm'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
