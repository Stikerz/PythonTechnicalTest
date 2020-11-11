
from django.urls import path
from bonds.views import UserAPIView, UserDetailView, BondAPIView

urlpatterns = [
    path("users/", UserAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("bonds/", BondAPIView.as_view(), name="bonds_list"),
]
