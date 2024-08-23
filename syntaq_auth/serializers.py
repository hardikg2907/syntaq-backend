from rest_framework.serializers import ModelSerializer
from .models import CustomUserModel
from django.conf import settings


class CustomUserModelSerializer(ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = ["userId", "email", "username", "password"]

    def create(self, validated_data):

        user = CustomUserModel.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )

        return user


class PublicUserDetailSerializer(ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = ["userId", "email", "username", "firstName", "lastName"]
