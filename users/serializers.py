from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(allow_null=True, allow_blank=True)
    telegram = serializers.CharField(allow_null=True, allow_blank=True)
    instagram = serializers.CharField(allow_null=True, allow_blank=True)
    phone = serializers.CharField(allow_null=True, allow_blank=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            login=validated_data['login'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = (
            "id",
            "login",
            "password",
            "email",
            "telegram",
            "instagram",
            "phone"
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_null=True, allow_blank=True)
    telegram = serializers.CharField(allow_null=True, allow_blank=True)
    instagram = serializers.CharField(allow_null=True, allow_blank=True)
    phone = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "telegram",
            "instagram",
            "phone"
        )
