from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            login=validated_data['login'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = ("id", "login", "password",)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'login'
        )
