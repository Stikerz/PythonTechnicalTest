from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bonds.models import Bond
from bonds.serializers import BondSerializer, UserSerializer


class UserAPIView(ListCreateAPIView):
    """view for listing a queryset or creating a model instance."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class UserDetailView(RetrieveUpdateDestroyAPIView):
    """view for retrieving, updating or deleting a model instance."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class BondAPIView(ListCreateAPIView):
    """view for listing a queryset or creating a model instance."""

    serializer_class = BondSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filters the returned bonds to a given legal name,
        by filtering against a `legal_name` query parameter in the URL.
        """
        legal_name = self.request.query_params.get("legal_name", None)
        if legal_name is not None:
            queryset = Bond.objects.all().filter(
                user=self.request.user, legal_name=legal_name
            )
        else:
            queryset = Bond.objects.all().filter(user=self.request.user)

        return queryset


class CustomAuthToken(ObtainAuthToken):  # pragma: no cover
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
            }
        )
