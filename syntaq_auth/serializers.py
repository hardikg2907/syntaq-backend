from rest_framework.serializers import ModelSerializer
from rest_flex_fields import FlexFieldsModelSerializer

from .models import CustomUserModel
from django.conf import settings


class CustomUserModelSerializer(ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = ["userId", "email", "username", "password", "first_name", "last_name"]

    def create(self, validated_data):
        print(validated_data)
        user = CustomUserModel.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        return user


class PublicUserDetailSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = ["email", "username", "first_name", "last_name"]
