from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.serializers import UserSerializer, UserInfoSerializer


class CreateUserViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = User.objects.all()
    model = get_user_model()
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    @action(methods=['GET'], detail=False, permission_classes=(IsAuthenticated, ))
    def users_info(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserInfoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserInfoSerializer(queryset, many=True)
        return Response(serializer.data)
