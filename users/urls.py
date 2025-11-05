from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from users.views import (
    PaymentListAPIView,
    PaymentDestroyAPIView,
    CustomUserCreateAPIView,
    CustomUserListAPIView,
    CustomUserUpdateAPIView,
    CustomUserDestroyAPIView,
    CustomUserRetrieveAPIView,
)
from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path("register/", CustomUserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("", CustomUserListAPIView.as_view(), name="user_list"),
    path("<int:pk>/", CustomUserRetrieveAPIView.as_view(), name="user_retrieve"),
    path("delete/<int:pk>/", CustomUserDestroyAPIView.as_view(), name="user_delete"),
    path("update/<int:pk>/", CustomUserUpdateAPIView.as_view(), name="user_update"),
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path(
        "payment/delete/<int:pk>/",
        PaymentDestroyAPIView.as_view(),
        name="payment_delete",
    ),
]
