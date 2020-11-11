from bonds.models import Bond
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer, DateField


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "username": {"required": False},
        }
        fields = ["username", "first_name", "last_name", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user_instance = User(**validated_data)
        user_instance.set_password(password)
        user_instance.save()
        return user_instance

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.save()
        return instance


class BondSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=CurrentUserDefault()
    )
    maturity = DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])

    class Meta:
        model = Bond
        fields = ["user", "isin", "size", "currency", "maturity", "lei", "legal_name"]
        extra_kwargs = {
            "legal_name": {"read_only": True},
        }

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        bond_instance = Bond(**validated_data)
        bond_instance.user = user
        bond_instance.save()
        return bond_instance
